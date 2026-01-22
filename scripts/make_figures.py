# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from hqcb_hhh.io import load_config
from hqcb_hhh.theory import fit_quadratic_sigma
from hqcb_hhh.likelihood import RateGaussianLikelihood

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--outdir", default="docs/figures")
    args = ap.parse_args()

    cfg = load_config(args.config)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    model = fit_quadratic_sigma(cfg.sigma_points)
    sigma_sm = float(model.sigma(1.0))
    sigma_err = cfg.rel_uncert_rate * sigma_sm
    like = RateGaussianLikelihood(model=model, sigma_asimov=sigma_sm, sigma_err=sigma_err)

    grid = np.linspace(cfg.kappa_min, cfg.kappa_max, cfg.n_grid)
    sig = model.sigma(grid)
    dnll = like.nll(grid)
    dnll = dnll - dnll.min()

    plt.figure()
    plt.plot(grid, sig)
    plt.scatter([k for k,_ in cfg.sigma_points], [s for _,s in cfg.sigma_points])
    plt.xlabel(r"$\kappa_\lambda$")
    plt.ylabel(r"$\sigma(gg\to HH)$ [fb] (14 TeV)")
    plt.title("Quadratic parametrization of HH rate vs κλ")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "sigma_vs_kappa.png", dpi=160)
    plt.close()

    plt.figure()
    plt.plot(grid, dnll)
    plt.axhline(cfg.cl68_delta_nll, linestyle="--")
    plt.axhline(cfg.cl95_delta_nll, linestyle="--")
    plt.xlabel(r"$\kappa_\lambda$")
    plt.ylabel(r"$\Delta \mathrm{NLL}$")
    plt.title("Asimov (SM) ΔNLL scan for κλ")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outdir / "deltaNLL_scan.png", dpi=160)
    plt.close()

    print("Wrote figures to: " + str(outdir))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
