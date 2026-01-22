from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class BAOMockDataset:
    # Observables típicos de BAO (mock): DV/rd en distintos z
    z: np.ndarray            # shape (N,)
    dv_over_rd: np.ndarray   # shape (N,)
    cov: np.ndarray          # shape (N,N)


def load_bao_mock_csv(csv_path: str, cov_path: str) -> BAOMockDataset:
    csvp = Path(csv_path)
    covp = Path(cov_path)
    if not csvp.exists():
        raise FileNotFoundError(f"BAO CSV not found: {csvp}")
    if not covp.exists():
        raise FileNotFoundError(f"BAO cov not found: {covp}")

    rows = []
    for line in csvp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if parts[0].lower() == "z":
            continue
        z = float(parts[0])
        dvrd = float(parts[1])
        rows.append((z, dvrd))

    if len(rows) < 2:
        raise ValueError("BAO mock needs at least 2 points")

    z = np.array([r[0] for r in rows], dtype=float)
    dvrd = np.array([r[1] for r in rows], dtype=float)

    cov = np.loadtxt(str(covp), dtype=float)
    if cov.ndim != 2 or cov.shape[0] != cov.shape[1]:
        raise ValueError("Covariance must be square")
    if cov.shape[0] != z.shape[0]:
        raise ValueError("Covariance dimension does not match data length")

    # Chequeo básico: simétrica y definida positiva (o al menos invertible)
    if not np.allclose(cov, cov.T, atol=1e-10, rtol=1e-10):
        raise ValueError("Covariance matrix must be symmetric")

    # Invertibilidad
    _ = np.linalg.inv(cov)

    return BAOMockDataset(z=z, dv_over_rd=dvrd, cov=cov)


def chi2_gaussian_cov(residual: np.ndarray, cov: np.ndarray) -> float:
    inv = np.linalg.inv(cov)
    return float(residual.T @ inv @ residual)


def loglike_gaussian_cov(residual: np.ndarray, cov: np.ndarray) -> float:
    # log L ~ -1/2 * chi2 - 1/2 * ln|2πC|
    n = residual.shape[0]
    sign, logdet = np.linalg.slogdet(cov)
    if sign <= 0:
        raise ValueError("Covariance not positive definite (slogdet sign <= 0)")
    chi2 = chi2_gaussian_cov(residual, cov)
    return float(-0.5 * chi2 - 0.5 * (n * np.log(2.0 * np.pi) + logdet))


def hqcb_predict_dv_over_rd_ratio(z: np.ndarray, alpha: float, p_sens: float) -> np.ndarray:
    """
    Modelo efectivo mínimo (mock) para BAO:
      DV/rd |HQCB  ≈ (DV/rd)|LCDM * [ (1+z)^alpha ]^p_sens

    En un paper real, aquí enchufas: H(z), DA(z), rd(z_rec) desde tu cierre HQCB.
    """
    return (1.0 + z) ** (alpha * p_sens)


def alpha_from_gamma(gamma: float, gamma_ref: float, kappa_b: float) -> float:
    # cierre bootstrap toy (igual al que ya vienes usando):
    return -kappa_b * (gamma - gamma_ref)


def bao_loglike_hqcb(
    dataset: BAOMockDataset,
    gamma: float,
    gamma_ref: float,
    kappa_b: float,
    p_sens: float,
    dvrd_lcdm_fid: np.ndarray | None = None,
) -> float:
    """
    Likelihood BAO (mock):
      y_obs = DV/rd (mock)
      y_pred = y_lcdm_fid * ratio_HQCB(z; alpha,p)

    dvrd_lcdm_fid: si None, usa y_obs como "fiducial" (mock) para aislar el efecto ratio.
    """
    a = alpha_from_gamma(gamma, gamma_ref, kappa_b)
    ratio = hqcb_predict_dv_over_rd_ratio(dataset.z, a, p_sens)

    if dvrd_lcdm_fid is None:
        y_pred = dataset.dv_over_rd * ratio
    else:
        if dvrd_lcdm_fid.shape != dataset.dv_over_rd.shape:
            raise ValueError("dvrd_lcdm_fid shape mismatch")
        y_pred = dvrd_lcdm_fid * ratio

    residual = dataset.dv_over_rd - y_pred
    return loglike_gaussian_cov(residual, dataset.cov)