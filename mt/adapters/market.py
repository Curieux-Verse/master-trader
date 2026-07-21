"""mt.adapters.market — the client side of the isolated market workers.

`MarketAdapter.build_panel` spawns `_market_worker.py` inside the market's stack root
and reads back a NormPanel. The mt process never imports a market's `core` directly
(that would reintroduce the namespace clash); it only ever talks to the workers.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from mt.config import LAKE_DIR, MARKETS, Market, DEFAULT_SEED, DATA_SNAPSHOT_ID
from mt.data.panel import NormPanel, load_norm_panel

_WORKER = Path(__file__).resolve().parent / "_market_worker.py"


class MarketWorkerError(RuntimeError):
    pass


class MarketAdapter:
    def __init__(self, market: str):
        if market not in MARKETS:
            raise KeyError(f"unknown market {market!r}; known: {list(MARKETS)}")
        self.market: Market = MARKETS[market]

    @property
    def name(self) -> str:
        return self.market.name

    def _timeframes(self) -> Dict[str, str]:
        return {"htf": self.market.htf, "mtf": self.market.mtf, "ltf": self.market.ltf}

    def build_panel(self, *, bars: int = 400, seed: int = DEFAULT_SEED,
                    snapshot_id: str = DATA_SNAPSHOT_ID, symbols: Optional[list] = None,
                    timeout: float = 120.0) -> NormPanel:
        """Run the isolated worker and load the resulting NormPanel from the lake."""
        tfs = self._timeframes()
        out_dir = LAKE_DIR / snapshot_id / self.market.name
        task = {
            "op": "build_panel",
            "market": self.market.name,
            "kind": self.market.kind,
            "symbols": symbols or self.market.universe,
            "timeframes": tfs,
            "bars": bars,
            "seed": seed,
            "snapshot_id": snapshot_id,
            "has_funding": self.market.has_funding,
            "out_dir": str(out_dir),
        }
        manifest = self._run_worker(task, timeout)
        panel = load_norm_panel(manifest, tfs)
        return panel

    def _run_worker(self, task: dict, timeout: float) -> dict:
        root = self.market.root
        if not root.exists():
            raise MarketWorkerError(f"market root does not exist: {root}")

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump(task, tf)
            task_path = tf.name

        env = dict(os.environ)
        # Prepend the market root so `import core...` resolves to THIS stack; nothing
        # from mt is on the path, so the worker cannot accidentally import mt.
        env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTHONIOENCODING"] = "utf-8"

        try:
            proc = subprocess.run(
                [sys.executable, str(_WORKER), task_path],
                cwd=str(root), env=env, capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            raise MarketWorkerError(f"{self.name} worker timed out after {timeout}s") from e
        finally:
            try:
                os.unlink(task_path)
            except OSError:
                pass

        manifest_path = Path(task["out_dir"]) / "_manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.setdefault("asof", datetime.now(timezone.utc).isoformat())
            return manifest

        raise MarketWorkerError(
            f"{self.name} worker produced no manifest (rc={proc.returncode}).\n"
            f"STDOUT: {proc.stdout[-800:]}\nSTDERR: {proc.stderr[-800:]}"
        )


def build_all_panels(markets: Optional[list] = None, *, bars: int = 400,
                     seed: int = DEFAULT_SEED, snapshot_id: str = DATA_SNAPSHOT_ID) -> Dict[str, NormPanel]:
    """Build one NormPanel per market, each in its own isolated worker process."""
    names = markets or list(MARKETS)
    out: Dict[str, NormPanel] = {}
    for name in names:
        out[name] = MarketAdapter(name).build_panel(bars=bars, seed=seed, snapshot_id=snapshot_id)
    return out
