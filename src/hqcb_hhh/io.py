# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import yaml

@dataclass(frozen=True)
class Config:
    rel_uncert_rate: float
    sigma_points: List[Tuple[float, float]]
    kappa_min: float
    kappa_max: float
    n_grid: int
    cl68_delta_nll: float
    cl95_delta_nll: float

def load_config(path: str | Path) -> Config:
    p = Path(path)
    data: Dict[str, Any] = yaml.safe_load(p.read_text(encoding="utf-8"))

    rel_unc = float(data["assumptions"]["rel_uncert_rate"])
    pts = [(float(r["kappa_lambda"]), float(r["sigma_fb"])) for r in data["sigma_points_fb"]]

    scan = data["scan"]
    intervals = data["intervals"]

    return Config(
        rel_uncert_rate=rel_unc,
        sigma_points=pts,
        kappa_min=float(scan["kappa_min"]),
        kappa_max=float(scan["kappa_max"]),
        n_grid=int(scan["n_grid"]),
        cl68_delta_nll=float(intervals["cl68_delta_nll"]),
        cl95_delta_nll=float(intervals["cl95_delta_nll"]),
    )
