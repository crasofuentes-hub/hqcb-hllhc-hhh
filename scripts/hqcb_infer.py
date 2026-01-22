from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np
import yaml

# Backend no interactivo para CI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from hqcb_hhh.inference import HQCBInferenceConfig, grid_posterior


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="HQCB inference (toy) with uncertainties + model comparison")
    p.add_argument("--config", required=True, help="YAML config path")
    p.add_argument("--out", default="data/results/hqcb_infer_results.json", help="Output JSON path")
    p.add_argument("--figdir", default="docs/figures", help="Directory for figures")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cfg_path = Path(args.config)
    if not cfg_path.exists():
        raise SystemExit(f"Config not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        y = yaml.safe_load(f)

    cfg = HQCBInferenceConfig(
        z_rec=float(y["z_rec"]),
        rd0_mpc=float(y["rd0_mpc"]),
        H0_local_obs=float(y["H0_local_obs"]),
        H0_local_sigma=float(y["H0_local_sigma"]),
        H0_early_obs=float(y["H0_early_obs"]),
        H0_early_sigma=float(y["H0_early_sigma"]),
        gamma_ref=float(y["gamma_ref"]),
        kappa_b=float(y["kappa_b"]),
        beta_rd_sensitivity=float(y["beta_rd_sensitivity"]),
        gamma_min=float(y["gamma_min"]),
        gamma_max=float(y["gamma_max"]),
        H0_min=float(y["H0_min"]),
        H0_max=float(y["H0_max"]),
        grid_gamma=int(y["grid_gamma"]),
        grid_H0=int(y["grid_H0"]),
    )

    res = grid_posterior(cfg)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(res, indent=2), encoding="utf-8")

    # Figuras
    figdir = Path(args.figdir)
    figdir.mkdir(parents=True, exist_ok=True)

    gammas = np.array(res["grid"]["gamma"], dtype=float)
    p_gamma = np.array(res["posterior"]["p_gamma"], dtype=float)
    gamma_ref = float(res["config_echo"]["gamma_ref"])
    gmean = float(res["summary"]["gamma_mean"])
    gmap = float(res["summary"]["gamma_map"])

    # 1) Posterior de gamma
    plt.figure(figsize=(10, 4))
    plt.plot(gammas, p_gamma)
    plt.axvline(gamma_ref, linestyle="--")
    plt.axvline(gmean, linestyle=":")
    plt.axvline(gmap, linestyle="-")
    plt.xlabel("gamma (exponente en rho_Lambda ~ (v^2/Mpl^2)^gamma)")
    plt.ylabel("Posterior p(gamma)")
    plt.title("HQCB toy: posterior of gamma")
    plt.grid(True)
    f1 = figdir / "hqcb_infer_gamma_posterior.png"
    plt.tight_layout()
    plt.savefig(f1, dpi=160)
    plt.close()

    # 2) Ratio H0_early_pred/H0_local en MAP vs dato
    H0_local_map = float(res["summary"]["H0_local_map"])
    H0_early_pred_map = float(res["summary"]["H0_early_pred_map"])
    ratio_map = H0_early_pred_map / H0_local_map if H0_local_map != 0 else float("nan")
    ratio_obs = float(res["config_echo"]["H0_early_obs"]) / float(res["config_echo"]["H0_local_obs"])

    plt.figure(figsize=(10, 4))
    plt.bar([0, 1], [ratio_obs, ratio_map])
    plt.xticks([0, 1], ["observed H0_early/H0_local", "HQCB MAP pred"])
    plt.ylabel("ratio")
    plt.title("HQCB toy: H0 ratio check")
    plt.grid(True, axis="y")
    f2 = figdir / "hqcb_infer_H0_ratio.png"
    plt.tight_layout()
    plt.savefig(f2, dpi=160)
    plt.close()

    # Salida ASCII-safe (evita Unicode en runners Windows)
    mc = res["model_comparison"]
    print("=== HQCB inference (toy) ===")
    print(f"Config: {str(cfg_path)}")
    print(f"gamma_ref: {gamma_ref:.6f}")
    print(f"gamma_map: {gmap:.6f} ; gamma_mean: {gmean:.6f}")
    print(f"H0_local_map: {H0_local_map:.3f} ; H0_early_pred_map: {H0_early_pred_map:.3f}")
    print(f"delta_AIC (LCDM - HQCB): {mc['delta_AIC']:.3f}")
    print(f"delta_BIC (LCDM - HQCB): {mc['delta_BIC']:.3f}")
    print(f"wrote: {str(out_path)}")
    print(f"figures: {str(f1)} ; {str(f2)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())