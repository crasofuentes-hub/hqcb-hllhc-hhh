# Copyright (c) 2026 Oscar Fuentes Fernández
# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Asegura que 'src' esté primero en sys.path (layout src/)
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))