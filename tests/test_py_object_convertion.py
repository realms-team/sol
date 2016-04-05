import pytest
import json

#============================ defines ===============================

EXAMPLE_MAC = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08]

#============================ fixtures ==============================

SOL_EXAMPLE = [
    {
        "DUST_OBJ": {
            "utcSecs":        1025665262,
            "utcUsecs":       139750,
            "macAddress":     [0, 23, 13, 0, 0, 56, 3, 221],
            "srcPort":        61625,
            "dstPort":        61625,
            "data":           [0, 0, 5, 0, 255, 1, 5, 0, 0, 0, 0, 61, 34, 104, 238, 0, 2, 56, 160, 0, 0, 117, 48, 1, 16, 9, 25]
        },
        "MIN_JSON_OBJ":       "EAAXDQAAOAPdVwNJricAAAUA/wEFAAAAAD0iaO4AAjigAAB1MAEQCRk=",
        "VERB_JSON_OBJ":
            {
                "timestamp"     : 1459833262,
                "mac"           : [0, 23, 13, 0, 0, 56, 3, 221],
                "type"          : 39,
                "value"         : [0, 0, 5, 0, 255, 1, 5, 0, 0, 0, 0, 61, 34, 104, 238, 0, 2, 56, 160, 0, 0, 117, 48, 1, 16, 9, 25]
            },
        "COMP_JSON": {
            "v"             : 0,
            "o"             : [
                {
                    "timestamp"     : 1459833262,
                    "mac"           : [0, 23, 13, 0, 0, 56, 3, 221],
                    "type"          : 39,
                    "value"         : [0, 0, 5, 0, 255, 1, 5, 0, 0, 0, 0, 61, 34, 104, 238, 0, 2, 56, 160, 0, 0, 117, 48, 1, 16, 9, 25]
                },
            ],
        },
        "COMP_BIN": [],
    },
]

# {"o": ["EAAXDQAAOABjVubEbBECAAIA9ABBAAIAAgABANsAZwABAAg=", "EAAXDQAAOAPdVubEbicAAAUA/wEFAAAAAD0ibHIAAjYFAAB1MAEQCNk="], "v": 0}

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
    dust_obj = sol.dust_to_json(sol_example["DUST_OBJ"])

    # update timestamp from JSON reference
    json_obj = sol_example["VERB_JSON_OBJ"]
    json_obj['timestamp'] = dust_obj['timestamp']

    # compare objects
    assert dust_obj==sol_example["VERB_JSON_OBJ"]

def test_list_to_compound(sol_example):
    sol_example = json.loads(sol_example)

    import Sol
    sol = Sol.Sol()

    assert sol.list_to_compound([sol_example["VERB_JSON_OBJ"]])==sol_example["COMP_JSON"]

def test_compound_to_list(sol_example):
    sol_example = json.loads(sol_example)
    import Sol
    sol = Sol.Sol()

    assert sol.compound_to_list(sol_example["COMP_JSON"])==[sol_example["VERB_JSON_OBJ"]]

def test_json_verb_to_min(sol_example):
    sol_example = json.loads(sol_example)
    import Sol
    sol = Sol.Sol()

    assert sol.json_verb_to_min(sol_example["VERB_JSON_OBJ"])==sol_example["MIN_JSON_OBJ"]

def test_json_min_to_verb(sol_example):
    sol_example = json.loads(sol_example)
    import Sol
    sol = Sol.Sol()

    assert sol.json_min_to_verb(sol_example["MIN_JSON_OBJ"])==sol_example["VERB_JSON_OBJ"]
