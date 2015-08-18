import pytest
import json

#============================ defines ===============================

EXAMPLE_MAC_1 = [0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18]
EXAMPLE_MAC_2 = [0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28]

#============================ fixtures ==============================

SOL_EXAMPLE = [
    {
        'dicts':
            [
                {
                    'mac':       EXAMPLE_MAC_1,
                    'timestamp': 0x11111111,
                    'type':      0x22,
                    'value':     [0x33,0x44],
                },
                {
                    'mac':       EXAMPLE_MAC_2,
                    'timestamp': 0x55555555,
                    'type':      0x66,
                    'value':     [0x77,0x88],
                },
            ],
        'json minimal':
            json.dumps(
                {
                    'v':         0,
                    'o':         [
                        "EBESExQVFhcYERERESIzRA==",
                        "ECEiIyQlJicoVVVVVWZ3iA==",
                    ],
                }
            ),
        'json verbose':
            json.dumps(
                {
                    'v':         0,
                    'o':         [
                        {
                            "mac":       "11-12-13-14-15-16-17-18",
                            "timestamp": 0x11111111,
                            "type":      0x22,
                            "value":     "M0Q=",
                        },
                        {
                            "mac":       "21-22-23-24-25-26-27-28",
                            "timestamp": 0x55555555,
                            "type":      0x66,
                            "value":     "d4g=",
                        },
                    ]
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

def test_dicts_to_json(sol_example,json_mode):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()
    
    assert sol.dicts_to_json(sol_example['dicts'],mode=json_mode)==sol_example['json {0}'.format(json_mode)]

def test_json_to_dicts(sol_example,json_mode):
    sol_example = json.loads(sol_example)
    
    import Sol
    sol = Sol.Sol()
    
    assert sol.json_to_dicts(sol_example['json {0}'.format(json_mode)])==sol_example['dicts']
