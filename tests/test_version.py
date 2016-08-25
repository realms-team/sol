from .context import Sol

#============================ defines ===============================

#============================ fixtures ==============================

#============================ helpers ===============================

#============================ tests =================================

def test_version():
    sol = Sol.Sol()
    
    assert type(sol.version)==tuple
    assert len(sol.version)==4
