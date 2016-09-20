import pytest
import ctypes
import context
import pdb

Sol = ctypes.CDLL(context.CLIB_PATH+'/libsol.so')

sol_type = ctypes.c_ubyte.in_dll(Sol, "SOL_TYPE_TEMPRH_SHT31").value

def test_sol_object_create():
    assert sol_type == 0x40
