import pytest
import json

#============================ defines ===============================

EXAMPLE_MAC = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08]

#============================ fixtures ==============================

SOL_EXAMPLE = [
    {
        'bin macYES':
            [
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<0,          # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x11,0x22,0x33,0x44,                       # timestamp
                0x55,                                      # type
                0x66,0x77                                  # value
            ],
        'bin macNO':
            [
                0<<6 | 0<<5 | 0<<4 | 0<<3 | 0<<0,          # header
                0x11,0x22,0x33,0x44,                       # timestamp
                0x55,                                      # type
                0x66,0x77                                  # value
            ],
        'dict':
            {
                'mac':       EXAMPLE_MAC,
                'timestamp': 0x11223344,
                'type':      0x55,
                'value':     [0x66,0x77],
            },
        'json minimal':
            json.dumps(
                {
                    'v':         0,
                    'o':         [
                        "EAECAwQFBgcIESIzRFVmdw==",
                    ],
                }
            ),
        'json verbose':
            json.dumps(
                {
                    'v':         0,
                    'o':         [
                        {
                            "mac":       "01-02-03-04-05-06-07-08",
                            "timestamp": 0x11223344,
                            "type":      0x55,
                            "value":     "Znc=",
                        },
                    ],
                }
            ),
    },
]

@pytest.fixture(params=SOL_EXAMPLE)
def sol_example(request):
    return json.dumps(request.param)

JSON_MODE = ['minimal','verbose']

@pytest.fixture(params=JSON_MODE)
def json_mode(request):
    return request.param

#============================ helpers ===============================

#============================ tests =================================

def test_dict_to_bin(sol_example):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()
    
    assert sol.dict_to_bin(sol_example['dict'])==sol_example['bin macYES']

def test_bin_to_dict(sol_example):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()
    
    assert sol.bin_to_dict(sol_example['bin macNO'],mac=EXAMPLE_MAC)==sol_example['dict']

def test_dicts_to_json(sol_example,json_mode):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()
    
    assert sol.dicts_to_json([sol_example['dict']],mode=json_mode)==sol_example['json {0}'.format(json_mode)]

def test_json_to_dicts(sol_example,json_mode):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()
    
    assert sol.json_to_dicts(sol_example['json {0}'.format(json_mode)])==[sol_example['dict']]
