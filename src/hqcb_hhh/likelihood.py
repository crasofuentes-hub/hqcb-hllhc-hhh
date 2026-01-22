# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from .theory import QuadraticSigmaModel

@dataclass(frozen=True)
class RateGaussianLikelihood:
    """"Asimov Gaussian likelihood on the inclusive HH rate.""" ""
    model: QuadraticSigmaModel
    sigma_asimov: float
    sigma_err: float

    def nll(self, kappa_lambda: np.ndarray | float) -> np.ndarray:
        s = self.model.sigma(kappa_lambda)
        return 0.5 * ((s - self.sigma_asimov) / self.sigma_err) ** 2

def find_interval_1d(grid_k: np.ndarray, nll: np.ndarray, delta: float) -> tuple[float, float]:
    idx_min = int(np.argmin(nll))
    nll0 = float(nll[idx_min])
    mask = (nll - nll0) <= delta
    if not np.any(mask):
        raise RuntimeError("No points satisfy the interval condition. Check scan range.")
    k_in = grid_k[mask]
    return float(k_in.min()), float(k_in.max())
