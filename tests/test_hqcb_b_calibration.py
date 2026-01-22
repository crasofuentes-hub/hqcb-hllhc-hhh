# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later

import math

def alpha_for_target_ratio(z_rec: float, p: float, target_ratio: float) -> float:
    if p == 0:
        raise ValueError("p cannot be zero")
    return math.log(target_ratio) / (p * math.log(1.0 + z_rec))

def test_alpha_zero_means_no_tension():
    # If target_ratio = 1 => alpha must be 0
    a = alpha_for_target_ratio(z_rec=1100.0, p=0.25, target_ratio=1.0)
    assert abs(a) < 1e-12

def test_sign_for_lower_early_h0():
    # If early is smaller than local => target_ratio < 1 => alpha must be negative when p>0
    ratio = 67.4 / 73.0
    a = alpha_for_target_ratio(z_rec=1100.0, p=0.25, target_ratio=ratio)
    assert a < 0.0