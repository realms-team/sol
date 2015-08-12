import pytest
import json

#============================ defines ===============================

#============================ fixtures ==============================

SOL_EXAMPLE = [
    {
        'bin':
            [
                0<<6 | 0<<5 | 0<<4 | 0<<3 | 0<<0,    # header
                0x11,0x22,0x33,0x44,                 # timestamp
                0x55,                                # type
                0x66,0x77                            # value
            ],
        'dict':
            {
                'mac':       [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08],
                'timestamp': 0x11223344,
                'type':      0x55,
                'value':     [0x66,0x77],
            },
        'json minimal': None,
        'json verbose': None,
    },
]

@pytest.fixture(params=SOL_EXAMPLE)
def sol_example(request):
    return json.dumps(request.param)

#============================ helpers ===============================

#============================ tests =================================

def test_dict_to_bin(sol_example):
    sol_example = json.loads(sol_example)
    
    import sol
    sol = sol.Sol()
    
    assert sol.dict_to_bin(sol_example['dict'])==sol_example['bin']