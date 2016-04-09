
#============================ defines ===============================

#============================ fixtures ==============================

#============================ helpers ===============================

#============================ tests =================================

def test_version():
    import Sol
    sol = Sol.Sol()
    
    assert type(sol.version)==dict
    assert len(sol.version)==4
    for (k,v) in sol.version.items():
        assert type(v)==int
