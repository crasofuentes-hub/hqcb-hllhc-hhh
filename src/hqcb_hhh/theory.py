# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple
import numpy as np

@dataclass(frozen=True)
class QuadraticSigmaModel:
    """"Quadratic parametrization: sigma(k) = a k^2 + b k + c.""" ""
    a: float
    b: float
    c: float

    def sigma(self, kappa_lambda: np.ndarray | float) -> np.ndarray:
        k = np.asarray(kappa_lambda, dtype=float)
        return self.a * k**2 + self.b * k + self.c

def fit_quadratic_sigma(points: Iterable[Tuple[float, float]]) -> QuadraticSigmaModel:
    """"Least-squares fit of a quadratic to (kappa_lambda, sigma_fb) points.""" ""
    pts = list(points)
    if len(pts) < 3:
        raise ValueError("Need at least 3 points to fit a quadratic model.")

    ks = np.array([p[0] for p in pts], dtype=float)
    ys = np.array([p[1] for p in pts], dtype=float)

    X = np.vstack([ks**2, ks, np.ones_like(ks)]).T
    coeff, *_ = np.linalg.lstsq(X, ys, rcond=None)
    a, b, c = coeff.tolist()
    return QuadraticSigmaModel(a=a, b=b, c=c)
