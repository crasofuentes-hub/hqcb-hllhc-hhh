# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

try:
    import yaml  # pyyaml
except Exception:
    yaml = None


@dataclass(frozen=True)
class ToyConfig:
    v0_gev: float
    z_rec: float
    rd0_mpc: float
    p_sensitivity: float
    H0_local: float
    H0_early_target: float
    z_max: float
    n_z: int
    figures_dir: str
    basename: str


def load_config(path: str) -> ToyConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    if yaml is None:
        raise RuntimeError("pyyaml is required for this script. Install with: python -m pip install pyyaml")

    raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    m = raw["model"]
    t = raw["targets"]
    s = raw["scan"]
    o = raw["output"]

    return ToyConfig(
        v0_gev=float(m["v0_gev"]),
        z_rec=float(m["z_rec"]),
        rd0_mpc=float(m["rd0_mpc"]),
        p_sensitivity=float(m["p_sensitivity"]),
        H0_local=float(t["H0_local"]),
        H0_early_target=float(t["H0_early_target"]),
        z_max=float(s["z_max"]),
        n_z=int(s["n_z"]),
        figures_dir=str(o["figures_dir"]),
        basename=str(o["basename"]),
    )


def v_eff(z: np.ndarray, v0: float, alpha: float) -> np.ndarray:
    # Toy law: slow cosmological running
    return v0 * (1.0 + z) ** alpha


def rd_true(v_ratio_at_rec: float, rd0: float, p: float) -> float:
    # Toy mapping: standard ruler depends on effective Higgs vacuum
    return rd0 * (v_ratio_at_rec ** p)


def alpha_for_target_ratio(z_rec: float, p: float, target_ratio: float) -> float:
    """
    We want: H0_early / H0_local ≈ rd_true/rd0 = [(v_eff(z_rec)/v0)^p]
    with v_eff(z)=v0*(1+z)^alpha -> ratio = (1+z_rec)^(alpha*p)
    => alpha = ln(target_ratio) / (p * ln(1+z_rec))
    """
    if p == 0:
        raise ValueError("p_sensitivity cannot be 0 for solving alpha.")
    return math.log(target_ratio) / (p * math.log(1.0 + z_rec))


def main() -> int:
    ap = argparse.ArgumentParser(description="HQCB-B toy: calibration-driven H0 tension via v_eff(z) affecting r_d.")
    ap.add_argument("--config", required=True, help="YAML config, e.g. data/cosmology/hqcb_b_toy.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)

    # Desired ratio from targets (early inferred vs local)
    target_ratio = cfg.H0_early_target / cfg.H0_local

    # Solve alpha so that rd_true/rd0 matches target_ratio
    alpha = alpha_for_target_ratio(cfg.z_rec, cfg.p_sensitivity, target_ratio)

    # Build curves
    z = np.linspace(0.0, cfg.z_max, cfg.n_z)
    v = v_eff(z, cfg.v0_gev, alpha)
    v_ratio_rec = (1.0 + cfg.z_rec) ** alpha  # v_eff(z_rec)/v0
    rd = rd_true(v_ratio_rec, cfg.rd0_mpc, cfg.p_sensitivity)

    H0_early_inferred = cfg.H0_local * (rd / cfg.rd0_mpc)

    # Print results (human-readable)
    print("=== HQCB-B toy: calibration-driven H0 tension ===")
    print("Author: Oscar Fuentes Fernández")
    print(f"Config: {args.config}")
    print(f"Targets: H0_local={cfg.H0_local:.3f}, H0_early_target={cfg.H0_early_target:.3f}")
    print(f"Solved alpha={alpha:.6e}  (v_eff ~ (1+z)^alpha)")
    print(f"p_sensitivity={cfg.p_sensitivity:.4f}")
    print(f"v_ratio(z_rec)=(1+z_rec)^alpha = {v_ratio_rec:.6f}")
    print(f"rd_true(z_rec) = {rd:.4f} Mpc  (rd0={cfg.rd0_mpc:.4f})")
    print(f"H0_early_inferred ≈ H0_local*(rd_true/rd0) = {H0_early_inferred:.3f} km/s/Mpc")

    # Figures
    figdir = Path(cfg.figures_dir)
    figdir.mkdir(parents=True, exist_ok=True)

    # 1) v_eff(z)/v0
    plt.figure(figsize=(8, 5))
    plt.plot(z, v / cfg.v0_gev)
    plt.xlabel("Redshift z")
    plt.ylabel("v_eff(z) / v0")
    plt.title("HQCB-B toy: slow running of v_eff(z)")
    plt.grid(True)
    out1 = figdir / f"{cfg.basename}_v_ratio.png"
    plt.tight_layout()
    plt.savefig(out1, dpi=160)

    # 2) implied bias ratio H0_early/H0_local (constant in this toy once fixed at recombination)
    plt.figure(figsize=(8, 5))
    plt.plot(z, np.full_like(z, H0_early_inferred / cfg.H0_local))
    plt.xlabel("Redshift z")
    plt.ylabel("H0_early_inferred / H0_local")
    plt.title("HQCB-B toy: calibration bias (constant once set by z_rec)")
    plt.grid(True)
    out2 = figdir / f"{cfg.basename}_H0_ratio.png"
    plt.tight_layout()
    plt.savefig(out2, dpi=160)

    print(f"Saved figures:\n- {out1.as_posix()}\n- {out2.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())