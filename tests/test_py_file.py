import os
import random

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

def getRandomObjects(num):
    returnVal = []
    for i in range(num):
        returnVal += [
            {
                'mac':       EXAMPLE_MAC,
                'timestamp': i,
                'type':      random.randint(0x00,0xff),
                'value':     [random.randint(0x00,0xff) for _ in range(random.randint(0,25))],
            }
        ]
    return returnVal

#============================ tests =================================

def test_dump_load(removeFile):
    import Sol
    sol = Sol.Sol()
    
    # prepare dicts to dump
    dictsToDump = getRandomObjects(1000)
    
    # dump
    sol.dumpToFile(dictsToDump,FILENAME)
    
    # load
    dictsLoaded = sol.loadFromFile(FILENAME)
    
    # compare
    assert dictsLoaded==dictsToDump

def test_dump_corrupt_load(removeFile):
    
    import Sol
    sol = Sol.Sol()
    
    # prepare dicts to dump
    dictsToDump1 = getRandomObjects(500)
    dictsToDump2 = getRandomObjects(500)
    
    # dump two sets of data with one corrupted record in the middle
    sol.dumpToFile(dictsToDump1,FILENAME)
    with open(FILENAME,'ab') as f:
        bin = ''.join([chr(b) for b in [0x7E,0x10,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x00,0x00,0x00,0x00,0x75,0x94,0xE8,0x0B,0x6B,0xAE,0xE1,0x19,0x54,0x74,0xF3,0x00,0x00,0x7E]])
        f.write(bin) 
    sol.dumpToFile(dictsToDump2,FILENAME)
    
    # load
    dictsLoaded = sol.loadFromFile(FILENAME)
    
    # compare
    assert dictsLoaded==dictsToDump1+dictsToDump2
