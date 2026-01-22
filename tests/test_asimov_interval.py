import numpy as np
from hqcb_hhh.theory import fit_quadratic_sigma
from hqcb_hhh.likelihood import RateGaussianLikelihood, find_interval_1d

def test_interval_shrinks_when_uncertainty_decreases():
    pts = [(0.0, 71.01), (1.0, 43.00), (2.0, 15.85)]
    model = fit_quadratic_sigma(pts)
    sigma_sm = float(model.sigma(1.0))
    grid = np.linspace(-5, 10, 3001)

    like_lo = RateGaussianLikelihood(model, sigma_sm, 0.15 * sigma_sm)
    like_hi = RateGaussianLikelihood(model, sigma_sm, 0.30 * sigma_sm)

    nll_lo = like_lo.nll(grid)
    nll_hi = like_hi.nll(grid)

    i95_lo = find_interval_1d(grid, nll_lo, 1.92)
    i95_hi = find_interval_1d(grid, nll_hi, 1.92)

    assert (i95_lo[1] - i95_lo[0]) < (i95_hi[1] - i95_hi[0])
