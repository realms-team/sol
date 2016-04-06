import pytest
import json

#============================ defines ===============================

EXAMPLE_MAC = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08]

#============================ fixtures ==============================

SOL_EXAMPLE = [
    {
        "dust": {
            "utcSecs":        1025665262,
            "utcUsecs":       139750,
            "macAddress":     [1, 2, 3, 4, 5, 6, 7, 8],
            "srcPort":        61625,
            "dstPort":        61625,
            "data":           [0, 0, 5, 0, 255, 1, 5, 0, 0, 0, 0, 61, 34, 104, 238, 0, 2, 56, 160, 0, 0, 117, 48, 1, 16, 9, 25]
        },
        "json":
            {
                "timestamp"     : 1459833262,
                "mac"           : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"          : 39,
                "value"         : [0, 0, 5, 0, 255, 1, 5, 0, 0, 0, 0, 61, 34, 104, 238, 0, 2, 56, 160, 0, 0, 117, 48, 1, 16, 9, 25]
            },
        'bin macYES':
            [
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<0,          # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x57,0x03,0x49,0xae,                       # timestamp
                0x27,                                      # type
                0x00, 0x00, 0x05, 0x00, 0xff, 0x01, 0x05,
                0x00, 0x00, 0x00, 0x00, 0x3d, 0x22, 0x68,
                0xee, 0x00, 0x02, 0x38, 0xa0, 0x00, 0x00,
                0x75, 0x30, 0x01, 0x10, 0x09, 0x19         # value
            ],
        'bin macNO':
            [
                0<<6 | 0<<5 | 0<<4 | 0<<3 | 0<<0,          # header
                0x11,0x22,0x33,0x44,                       # timestamp
                0x55,                                      # type
                0x66,0x77                                  # value
            ],
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

def test_dust_to_json(sol_example):
    sol_example = json.loads(sol_example)

    import Sol
    sol = Sol.Sol()

    # convert dust object
    conv_obj = sol.dust_to_json(sol_example["dust"])

    # update timestamp from JSON reference
    json_obj = sol_example["json"]
    json_obj['timestamp'] = conv_obj['timestamp']

    # compare objects
    assert conv_obj==json_obj

def test_json_to_bin(sol_example):
    sol_example = json.loads(sol_example)
    import Sol
    sol = Sol.Sol()

    assert sol.json_to_bin([sol_example["json"]])==sol_example["bin macYES"]

def test_bin_to_json(sol_example):
    sol_example = json.loads(sol_example)
    import Sol
    sol = Sol.Sol()

    assert sol.bin_to_json(sol_example["bin macYES"])==[sol_example["json"]]
