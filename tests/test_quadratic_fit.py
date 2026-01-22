import numpy as np
from hqcb_hhh.theory import fit_quadratic_sigma

def test_quadratic_fit_reproduces_points():
    pts = [(0.0, 71.01), (1.0, 43.00), (2.0, 15.85)]
    model = fit_quadratic_sigma(pts)
    for k, s in pts:
        assert abs(float(model.sigma(k)) - s) < 1e-10

def test_sigma_decreases_between_0_and_2_for_this_tabulation():
    pts = [(0.0, 71.01), (1.0, 43.00), (2.0, 15.85)]
    model = fit_quadratic_sigma(pts)
    ks = np.linspace(0, 2, 101)
    sig = model.sigma(ks)
    assert np.all(np.diff(sig) < 0)
