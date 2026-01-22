from __future__ import annotations

import json
from pathlib import Path

import yaml

from hqcb_hhh.inference import HQCBInferenceConfig, grid_posterior


def test_inference_grid_runs_and_returns_keys(tmp_path: Path) -> None:
    cfg = HQCBInferenceConfig(
        z_rec=1100.0,
        rd0_mpc=147.0,
        H0_local_obs=73.0,
        H0_local_sigma=1.0,
        H0_early_obs=67.4,
        H0_early_sigma=0.6,
        gamma_ref=11.0/3.0,
        kappa_b=1.0,
        beta_rd_sensitivity=0.25,
        gamma_min=3.0,
        gamma_max=4.5,
        H0_min=60.0,
        H0_max=80.0,
        grid_gamma=101,
        grid_H0=81,
    )
    res = grid_posterior(cfg)
    assert "summary" in res
    assert "model_comparison" in res
    assert "posterior" in res
    assert "grid" in res

    # sanity: MAP gamma debe caer dentro del prior
    gmap = res["summary"]["gamma_map"]
    assert cfg.gamma_min <= gmap <= cfg.gamma_max


def test_script_config_can_be_loaded(tmp_path: Path) -> None:
    y = {
        "z_rec": 1100.0,
        "rd0_mpc": 147.0,
        "H0_local_obs": 73.0,
        "H0_local_sigma": 1.0,
        "H0_early_obs": 67.4,
        "H0_early_sigma": 0.6,
        "gamma_ref": 11.0/3.0,
        "kappa_b": 1.0,
        "beta_rd_sensitivity": 0.25,
        "gamma_min": 3.0,
        "gamma_max": 4.5,
        "H0_min": 60.0,
        "H0_max": 80.0,
        "grid_gamma": 51,
        "grid_H0": 41,
    }
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml.safe_dump(y), encoding="utf-8")
    loaded = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert loaded["gamma_ref"] > 3.0