import pytest
import json

#============================ defines ===============================

EXAMPLE_MAC_1 = [0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18]
EXAMPLE_MAC_2 = [0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28]

#============================ fixtures ==============================

SOL_EXAMPLE = [
    {
        'json':
            [
                {
                    'mac':       EXAMPLE_MAC_1,
                    'timestamp': 0x11111111,
                    'type':      0x07,
                    'value':     [0x33,0x33,0x33,0x33,0x33,0x33,0x33,0x33],
                },
                {
                    'mac':       EXAMPLE_MAC_2,
                    'timestamp': 0x55555555,
                    'type':      0x07,
                    'value':     [0x77,0x77,0x77,0x77,0x77,0x77,0x77,0x77],
                },
            ],
        'bin':
            [
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<0,                # header
                0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,         # mac
                0x11,0x11,0x11,0x11,                             # timestamp
                0x07,                                            # type
                0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33,  # value
                0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,         # mac
                0x55,0x55,0x55,0x55,                             # timestamp
                0x07,                                            # type
                0x77, 0x77, 0x77, 0x77, 0x77, 0x77, 0x77, 0x77,  # value
            ],
    },
]

@pytest.fixture(params=SOL_EXAMPLE)
def sol_example(request):
    return json.dumps(request.param)

#============================ helpers ===============================

#============================ tests =================================

def test_json_to_bin(sol_example):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()

    assert sol.json_to_bin(sol_example['json'])==sol_example['bin']

def test_json_to_dicts(sol_example):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()

    assert sol.bin_to_json(sol_example['bin'])==sol_example['json']
