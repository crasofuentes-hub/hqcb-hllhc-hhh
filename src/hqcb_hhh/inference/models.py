from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class HQCBInferenceConfig:
    # Observables (toy, pero con incertidumbres reales en el pipeline)
    z_rec: float
    rd0_mpc: float

    H0_local_obs: float
    H0_local_sigma: float

    H0_early_obs: float
    H0_early_sigma: float

    # Cierre bootstrap (toy formal):
    #   alpha(gamma) = -kappa_b * (gamma - gamma_ref)
    # y el "puente" cosmológico (toy) hace:
    #   rd_true/rd0 = v_ratio^beta
    #   v_ratio(z_rec) = (1+z_rec)^alpha
    gamma_ref: float
    kappa_b: float
    beta_rd_sensitivity: float

    # Priors (rangos)
    gamma_min: float
    gamma_max: float
    H0_min: float
    H0_max: float

    # Resolución del grid
    grid_gamma: int
    grid_H0: int


def alpha_from_gamma(gamma: float, gamma_ref: float, kappa_b: float) -> float:
    return -kappa_b * (gamma - gamma_ref)


def v_ratio_at_rec(z_rec: float, alpha: float) -> float:
    return (1.0 + z_rec) ** alpha


def rd_ratio_from_vratio(v_ratio: float, beta_rd_sensitivity: float) -> float:
    # rd_true/rd0 = v_ratio^beta
    return v_ratio ** beta_rd_sensitivity


def predict_H0_early(H0_local: float, z_rec: float, gamma: float, gamma_ref: float, kappa_b: float, beta: float) -> float:
    a = alpha_from_gamma(gamma, gamma_ref, kappa_b)
    vratio = v_ratio_at_rec(z_rec, a)
    rd_ratio = rd_ratio_from_vratio(vratio, beta)
    # H0_early_inferred = H0_local * (rd_true/rd0)
    return H0_local * rd_ratio


def loglike_gaussian(x: float, mu: float, sigma: float) -> float:
    # log N(x | mu, sigma)
    if sigma <= 0:
        raise ValueError("sigma must be > 0")
    z = (x - mu) / sigma
    return -0.5 * (z * z) - math.log(sigma * math.sqrt(2.0 * math.pi))


def grid_posterior(cfg: HQCBInferenceConfig) -> Dict[str, object]:
    gammas = np.linspace(cfg.gamma_min, cfg.gamma_max, cfg.grid_gamma, dtype=float)
    H0s    = np.linspace(cfg.H0_min, cfg.H0_max, cfg.grid_H0, dtype=float)

    logpost = np.empty((cfg.grid_gamma, cfg.grid_H0), dtype=float)

    # Likelihood:
    #   L = N(H0_local_obs | H0_local, sigma_local) * N(H0_early_obs | H0_early_pred(gamma,H0_local), sigma_early)
    for i, g in enumerate(gammas):
        for j, h0 in enumerate(H0s):
            h0_early_pred = predict_H0_early(
                H0_local=h0,
                z_rec=cfg.z_rec,
                gamma=g,
                gamma_ref=cfg.gamma_ref,
                kappa_b=cfg.kappa_b,
                beta=cfg.beta_rd_sensitivity,
            )
            ll = 0.0
            ll += loglike_gaussian(cfg.H0_local_obs, h0, cfg.H0_local_sigma)
            ll += loglike_gaussian(cfg.H0_early_obs, h0_early_pred, cfg.H0_early_sigma)
            # Priors uniformes dentro de rangos (0 fuera)
            logpost[i, j] = ll

    # Normalización numérica estable
    m = np.max(logpost)
    w = np.exp(logpost - m)
    Z = np.sum(w)
    if not np.isfinite(Z) or Z <= 0:
        raise RuntimeError("Posterior normalization failed")

    post = w / Z

    # Marginales
    p_gamma = np.sum(post, axis=1)
    p_H0    = np.sum(post, axis=0)

    # Estadísticos
    gamma_mean = float(np.sum(gammas * p_gamma))
    H0_mean    = float(np.sum(H0s * p_H0))

    def credible_interval_1d(x: np.ndarray, p: np.ndarray, level: float) -> Tuple[float, float]:
        # HPD aproximado por cuantiles (suficiente en toy unimodal)
        cdf = np.cumsum(p)
        cdf = cdf / cdf[-1]
        lo_q = (1.0 - level) / 2.0
        hi_q = 1.0 - lo_q
        lo = float(np.interp(lo_q, cdf, x))
        hi = float(np.interp(hi_q, cdf, x))
        return lo, hi

    gamma_68 = credible_interval_1d(gammas, p_gamma, 0.68)
    gamma_95 = credible_interval_1d(gammas, p_gamma, 0.95)

    # Best-fit (MAP en grid)
    idx = np.unravel_index(np.argmax(post), post.shape)
    gamma_map = float(gammas[idx[0]])
    H0_map    = float(H0s[idx[1]])
    H0_early_map = float(predict_H0_early(H0_map, cfg.z_rec, gamma_map, cfg.gamma_ref, cfg.kappa_b, cfg.beta_rd_sensitivity))

    # Métricas de comparación de modelo (AIC/BIC) con máxima verosimilitud en grid
    # k = número de parámetros del modelo; n = número de observaciones efectivas (aquí 2: H0_local y H0_early)
    # logLmax aproximada: usando logpost (priors uniformes no aportan constante dentro del rango).
    logL_max = float(np.max(logpost))
    n = 2
    k = 2
    AIC = float(2*k - 2*logL_max)
    BIC = float(k*math.log(n) - 2*logL_max)

    # Modelo competidor LCDM-toy: fija gamma = gamma_ref, solo H0_local libre
    # => H0_early_pred = H0_local (porque alpha=0 => rd_ratio=1)
    # k=1
    logL_lcdm = []
    for h0 in H0s:
        ll = 0.0
        ll += loglike_gaussian(cfg.H0_local_obs, float(h0), cfg.H0_local_sigma)
        ll += loglike_gaussian(cfg.H0_early_obs, float(h0), cfg.H0_early_sigma)
        logL_lcdm.append(ll)
    logL_lcdm_max = float(np.max(np.array(logL_lcdm)))
    k_lcdm = 1
    AIC_lcdm = float(2*k_lcdm - 2*logL_lcdm_max)
    BIC_lcdm = float(k_lcdm*math.log(n) - 2*logL_lcdm_max)

    return {
        "grid": {
            "gamma": gammas.tolist(),
            "H0_local": H0s.tolist(),
        },
        "posterior": {
            "p_gamma": p_gamma.tolist(),
            "p_H0_local": p_H0.tolist(),
        },
        "summary": {
            "gamma_mean": gamma_mean,
            "gamma_map": gamma_map,
            "gamma_68": [gamma_68[0], gamma_68[1]],
            "gamma_95": [gamma_95[0], gamma_95[1]],
            "H0_local_mean": H0_mean,
            "H0_local_map": H0_map,
            "H0_early_pred_map": H0_early_map,
        },
        "model_comparison": {
            "HQCB": {"k": k, "n": n, "logL_max": logL_max, "AIC": AIC, "BIC": BIC},
            "LCDM_toy": {"k": k_lcdm, "n": n, "logL_max": logL_lcdm_max, "AIC": AIC_lcdm, "BIC": BIC_lcdm},
            "delta_AIC": AIC_lcdm - AIC,
            "delta_BIC": BIC_lcdm - BIC,
        },
        "config_echo": {
            "z_rec": cfg.z_rec,
            "rd0_mpc": cfg.rd0_mpc,
            "H0_local_obs": cfg.H0_local_obs,
            "H0_local_sigma": cfg.H0_local_sigma,
            "H0_early_obs": cfg.H0_early_obs,
            "H0_early_sigma": cfg.H0_early_sigma,
            "gamma_ref": cfg.gamma_ref,
            "kappa_b": cfg.kappa_b,
            "beta_rd_sensitivity": cfg.beta_rd_sensitivity,
        }
    }