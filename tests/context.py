# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))
here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(here, '..', 'smartmeshsdk', 'libs'))

from solobjectlib import Sol as sol

# =========================== defines =========================================

# C implementation PATH
CLIB_PATH = os.path.join(here, '..', 'sol_c')
