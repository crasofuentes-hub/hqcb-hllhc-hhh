from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yaml

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from hqcb_hhh.inference import (
    HQCBInferenceConfig,
    grid_posterior,
    load_bao_mock_csv,
    bao_loglike_hqcb,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="HQCB inference with BAO mock likelihood (cov) + H0 toy")
    p.add_argument("--config", required=True, help="YAML config path")
    p.add_argument("--out", default="data/results/hqcb_infer_data_results.json", help="Output JSON path")
    p.add_argument("--figdir", default="docs/figures", help="Directory for figures")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cfg_path = Path(args.config)
    if not cfg_path.exists():
        raise SystemExit(f"Config not found: {cfg_path}")

    y = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    # Reusa tu bloque H0-toy (mismo config base)
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

    # BAO dataset mock (cov)
    bao = load_bao_mock_csv(
        csv_path=str(y["bao_csv"]),
        cov_path=str(y["bao_cov"]),
    )
    p_sens = float(y["bao_p_sensitivity"])

    # 1) Posterior H0-toy (ya normalizado)
    res = grid_posterior(cfg)

    gammas = np.array(res["grid"]["gamma"], dtype=float)
    p_gamma = np.array(res["posterior"]["p_gamma"], dtype=float)

    # 2) Repondera p(gamma) por likelihood BAO (marginal: BAO depende de gamma, no de H0_local en este mock)
    logw_bao = np.array([
        bao_loglike_hqcb(bao, g, cfg.gamma_ref, cfg.kappa_b, p_sens) for g in gammas
    ], dtype=float)

    # Estabiliza y combina
    m = np.max(logw_bao)
    w = np.exp(logw_bao - m)
    p_gamma_joint = p_gamma * w
    Z = np.sum(p_gamma_joint)
    if not np.isfinite(Z) or Z <= 0:
        raise RuntimeError("Joint normalization failed")
    p_gamma_joint /= Z

    gamma_mean_joint = float(np.sum(gammas * p_gamma_joint))
    gamma_map_joint = float(gammas[int(np.argmax(p_gamma_joint))])

    # Fig: posterior gamma (H0-only) vs joint(H0+BAO)
    figdir = Path(args.figdir)
    figdir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(gammas, p_gamma, label="H0-only")
    plt.plot(gammas, p_gamma_joint, label="H0 + BAO(cov)")
    plt.axvline(cfg.gamma_ref, linestyle="--", label="gamma_ref")
    plt.xlabel("gamma")
    plt.ylabel("posterior")
    plt.title("HQCB: gamma posterior update with BAO mock")
    plt.grid(True)
    plt.legend()
    f1 = figdir / "hqcb_infer_joint_gamma.png"
    plt.tight_layout()
    plt.savefig(f1, dpi=160)
    plt.close()

    out = {
        "base_H0_results": res,
        "bao_mock": {
            "N": int(bao.z.shape[0]),
            "z": bao.z.tolist(),
            "dv_over_rd": bao.dv_over_rd.tolist(),
            "bao_p_sensitivity": p_sens,
        },
        "joint": {
            "p_gamma_joint": p_gamma_joint.tolist(),
            "gamma_mean_joint": gamma_mean_joint,
            "gamma_map_joint": gamma_map_joint,
        }
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    # ASCII-safe prints
    print("=== HQCB infer-data (H0 toy + BAO mock cov) ===")
    print(f"Config: {str(cfg_path)}")
    print(f"gamma_ref: {cfg.gamma_ref:.6f}")
    print(f"gamma_mean_joint: {gamma_mean_joint:.6f}")
    print(f"gamma_map_joint: {gamma_map_joint:.6f}")
    print(f"wrote: {str(out_path)}")
    print(f"figure: {str(f1)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())