import pytest
import ctypes
import context

Sol = ctypes.CDLL(context.CLIB_PATH+'/libsol.so')
