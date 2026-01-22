from __future__ import annotations

import numpy as np

from hqcb_hhh.inference.likelihoods import chi2_gaussian_cov, loglike_gaussian_cov


def test_cov_gaussian_loglike_matches_chi2_for_identity() -> None:
    r = np.array([1.0, -2.0, 0.5])
    cov = np.eye(3)
    chi2 = chi2_gaussian_cov(r, cov)
    ll = loglike_gaussian_cov(r, cov)
    # ll = -0.5 chi2 - 0.5(n ln(2pi) + ln|I|)
    expected = -0.5 * chi2 - 0.5 * (3 * np.log(2.0 * np.pi) + 0.0)
    assert abs(ll - expected) < 1e-10


def test_chi2_positive() -> None:
    r = np.array([0.1, 0.2])
    cov = np.array([[0.04, 0.0],[0.0, 0.09]])
    chi2 = chi2_gaussian_cov(r, cov)
    assert chi2 >= 0.0