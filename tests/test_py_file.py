import os

import pytest

#============================ defines ===============================

FILENAME    = 'temp_test_file.sol'
EXAMPLE_MAC = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08]

#============================ fixtures ==============================

def removeFileFunc():
    os.remove(FILENAME)

@pytest.fixture(scope='function')
def removeFile(request):
    #request.addfinalizer(removeFileFunc)
    try:
        os.remove(FILENAME)
    except WindowsError:
        # if file does not exist. NOT an error.
        pass

#============================ helpers ===============================

#============================ tests =================================

def test_dump_load(removeFile):
    import Sol
    sol = Sol.Sol()
    
    # prepare dicts to dump
    dictsToDump = []
    for i in range(10):
        dictsToDump += [
            {
                'mac':       EXAMPLE_MAC,
                'timestamp': i,
                'type':      0x55,
                'value':     [0x66,0x77],
            }
        ]
    
    # dump
    sol.dumpToFile(dictsToDump,FILENAME)
    
    # load
    dictsLoaded = sol.loadFromFile(FILENAME)
    
    # compare
    assert dictsLoaded==dictsToDump