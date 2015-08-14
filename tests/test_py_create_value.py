import pytest
import json

#============================ defines ===============================

#============================ fixtures ==============================

#============================ helpers ===============================

#============================ tests =================================

def test_create_value_NOTIF_EVENT():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_NOTIF_EVENT(0x11223344,0x55,[0x66,0x77])==[0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_NOTIF_DATA_RAW():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_NOTIF_DATA_RAW(0x1122,0x3344,[0x55,0x66])==[0x11,0x22,0x33,0x44,0x55,0x66]