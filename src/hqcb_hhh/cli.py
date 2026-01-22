# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import argparse
import numpy as np
from .io import load_config
from .theory import fit_quadratic_sigma
from .likelihood import RateGaussianLikelihood, find_interval_1d

def cmd_asimov(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    model = fit_quadratic_sigma(cfg.sigma_points)

    # Asimov truth: SM (kappa_lambda = 1)
    sigma_sm = float(model.sigma(1.0))
    sigma_err = cfg.rel_uncert_rate * sigma_sm

    like = RateGaussianLikelihood(model=model, sigma_asimov=sigma_sm, sigma_err=sigma_err)
    grid = np.linspace(cfg.kappa_min, cfg.kappa_max, cfg.n_grid)
    nll = like.nll(grid)

    i68 = find_interval_1d(grid, nll, cfg.cl68_delta_nll)
    i95 = find_interval_1d(grid, nll, cfg.cl95_delta_nll)

    print("=== HQCB-HL-LHC κλ forecast (Asimov, SM truth) ===")
    print("Author: Oscar Fuentes Fernández")
    print(f"Config: {args.config}")
    print(f"Quadratic fit: a={model.a:.6g}, b={model.b:.6g}, c={model.c:.6g}")
    print(f"sigma_SM(k=1): {sigma_sm:.4f} fb")
    print(f"rel_uncert_rate: {cfg.rel_uncert_rate:.3f} -> sigma_err={sigma_err:.4f} fb")
    print(f"68% interval (ΔNLL={cfg.cl68_delta_nll}): [{i68[0]:.3f}, {i68[1]:.3f}]")
    print(f"95% interval (ΔNLL={cfg.cl95_delta_nll}): [{i95[0]:.3f}, {i95[1]:.3f}]")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(prog="hqcb_hhh")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_as = sub.add_parser("asimov", help="Run an Asimov SM-truth forecast for κλ.")
    p_as.add_argument("--config", required=True)
    p_as.set_defaults(fn=cmd_asimov)

    args = parser.parse_args()
    return int(args.fn(args))

if __name__ == "__main__":
    raise SystemExit(main())
