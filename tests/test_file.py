from .context import Sol
import os
import random

import pytest

from   SmartMeshSDK.utils    import FormatUtils

# ============================ defines ===============================

FILENAME = 'temp_test_file.sol'
EXAMPLE_MAC = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]


# ============================ fixtures ==============================

def removeFileFunc():
    os.remove(FILENAME)


@pytest.fixture(scope='function')
def removeFile(request):
    # request.addfinalizer(removeFileFunc)
    try:
        os.remove(FILENAME)
    except OSError:
        # if file does not exist. NOT an error.
        pass


EXPECTEDRANGE = [
    (
        100,  # start_timestamp
        300,  # end_timestamp
        100,  # idxMin
        301,  # idxMax
    ),
    (
        -5,  # start_timestamp
        300,  # end_timestamp
        0,  # idxMin
        301,  # idxMax
    ),
    (
        100,  # start_timestamp
        1100,  # end_timestamp
        100,  # idxMin
        1000,  # idxMax
    ),
    (
        -5,  # start_timestamp
        1100,  # end_timestamp
        0,  # idxMin
        1000,  # idxMax
    ),
    (
        -500,  # start_timestamp
        -100,  # end_timestamp
        0,  # idxMin
        0,  # idxMax
    ),
    (
        1100,  # start_timestamp
        1500,  # end_timestamp
        0,  # idxMin
        0,  # idxMax
    ),
]


@pytest.fixture(params=EXPECTEDRANGE)
def expectedRange(request):
    return request.param


# ============================ helpers ===============================

def random_sol_json(timestamp=0):
    returnVal = {
        "timestamp": timestamp,
        "mac": FormatUtils.formatBuffer([random.randint(0x00, 0xff)] * 8),
        "type": 0x0e,
        "value": {
            'srcPort': random.randint(0x0000, 0xffff),
            'dstPort': random.randint(0x0000, 0xffff),
            'data': [random.randint(0x00, 0xff)] * random.randint(10, 30),
        },
    }

    return returnVal


# ============================ tests =================================

def test_dump_load(removeFile):
    sol = Sol.Sol()

    # prepare dicts to dump
    sol_jsonl_toDump = [random_sol_json() for _ in range(1000)]

    # dump
    sol.dumpToFile(sol_jsonl_toDump, FILENAME)

    # load
    sol_jsonl_loaded = sol.loadFromFile(FILENAME)

    # compare
    print sol_jsonl_loaded
    print sol_jsonl_toDump
    assert sol_jsonl_loaded == sol_jsonl_toDump


def test_dump_corrupt_load(removeFile):
    sol = Sol.Sol()

    # prepare dicts to dump
    sol_jsonl_toDump1 = [random_sol_json() for _ in range(500)]
    sol_jsonl_toDump2 = [random_sol_json() for _ in range(500)]

    # write first set of valid data
    sol.dumpToFile(sol_jsonl_toDump1, FILENAME)
    # write HDLC frame with corrupt CRC
    with open(FILENAME, 'ab') as f:
        bin_data = ''.join([chr(b) for b in
                            [0x7E, 0x10, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x00, 0x00, 0x00, 0x00, 0x75,
                             0x94, 0xE8, 0x0B, 0x6B, 0xAE, 0xE1, 0x19, 0x54, 0x74, 0xF3, 0x00, 0x00, 0x7E]])
        f.write(bin_data)
    # write some garbage
    with open(FILENAME, 'ab') as f:
        f.write("############################## garbage ##############################")
    # write second set of valid data
    sol.dumpToFile(sol_jsonl_toDump2, FILENAME)

    # load
    sol_jsonl_loaded = sol.loadFromFile(FILENAME)

    # compare
    assert sol_jsonl_loaded == sol_jsonl_toDump1 + sol_jsonl_toDump2


def test_retrieve_range(removeFile):
    sol = Sol.Sol()

    # prepare dicts to dump
    sol_jsonl_toDump = [random_sol_json(timestamp=ts) for ts in range(1000)]

    # dump
    sol.dumpToFile(sol_jsonl_toDump, FILENAME)

    # load
    sol_jsonl_loaded = sol.loadFromFile(
        FILENAME,
        start_timestamp=100,
        end_timestamp=1900,
    )

    # compare
    assert sol_jsonl_loaded == sol_jsonl_toDump[100:]


def test_retrieve_range_corrupt_beginning(removeFile):
    sol = Sol.Sol()

    # prepare dicts to dump
    sol_jsonl_toDump = [random_sol_json(timestamp=ts) for ts in range(1000)]

    # dump
    with open(FILENAME, 'ab') as f:
        f.write("garbage")
    sol.dumpToFile(sol_jsonl_toDump, FILENAME)

    # load
    sol_jsonl_loaded = sol.loadFromFile(
        FILENAME,
        start_timestamp=100,
        end_timestamp=800
    )

    # compare
    assert sol_jsonl_loaded == sol_jsonl_toDump[100:801]


def test_retrieve_range_corrupt_middle(removeFile):
    sol = Sol.Sol()

    # prepare dicts to dump
    sol_jsonl_toDump1 = [random_sol_json(timestamp=ts) for ts in range(500)]
    sol_jsonl_toDump2 = [random_sol_json(timestamp=500 + ts) for ts in range(500)]

    # dump
    sol.dumpToFile(sol_jsonl_toDump1, FILENAME)
    with open(FILENAME, 'ab') as f:
        f.write("garbage")
    sol.dumpToFile(sol_jsonl_toDump2, FILENAME)

    # load
    sol_jsonl_loaded = sol.loadFromFile(
        FILENAME,
        start_timestamp=100,
        end_timestamp=800,
    )

    # compare
    assert sol_jsonl_loaded == (sol_jsonl_toDump1 + sol_jsonl_toDump2)[100:801]


def test_retrieve_range_corrupt_end(removeFile):
    sol = Sol.Sol()

    # prepare dicts to dump
    sol_jsonl_toDump = [random_sol_json(timestamp=ts) for ts in range(1000)]

    # dump
    sol.dumpToFile(sol_jsonl_toDump, FILENAME)
    with open(FILENAME, 'ab') as f:
        f.write("garbage")

    # load
    sol_jsonl_loaded = sol.loadFromFile(
        FILENAME,
        start_timestamp=100,
        end_timestamp=800
    )

    # compare
    assert sol_jsonl_loaded == sol_jsonl_toDump[100:801]


def test_retrieve_range_corrupt_all(removeFile):
    sol = Sol.Sol()

    # dump
    with open(FILENAME, 'ab') as f:
        for _ in range(100):
            f.write("garbage")

    # load
    sol_jsonl_loaded = sol.loadFromFile(
        FILENAME,
        start_timestamp=100,
        end_timestamp=800,
    )

    # compare
    assert sol_jsonl_loaded == []
