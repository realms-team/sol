import pytest
import json
import pprint

from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial

#============================ defines ===============================

MACMANAGER = [3,3,3,3,3,3,3,3]
TIMESTAMP   = "2016-04-19T01:54:16Z"

#============================ fixtures ==============================

SOL_CHAIN_EXAMPLE = [
    # SOL_TYPE_DUST_NOTIF_HRNEIGHBORS
    {
        "json":
            [{
                "timestamp"  : TIMESTAMP,
                "mac"        : "00-17-0d-00-00-58-32-36",
                "type"       : "SOL_TYPE_DUST_NOTIF_HRNEIGHBORS",
                "value"      : {
                    "latitude"  : "-33.11464",
                    "longitude" : "-68.48015",
                    "site"      : "ARG_junin",
                    "neighbors" : [
                        {
                            'neighborId':       1,
                            'neighborFlag':     0,
                            'rssi':             -33,
                            'numTxPackets':     0,
                            'numTxFailures':    0,
                            'numRxPackets':     47,
                        },
                        {
                            'neighborId':       2,
                            'neighborFlag':     0,
                            'rssi':             -47,
                            'numTxPackets':     76,
                            'numTxFailures':    1,
                            'numRxPackets':     2,
                        },
                    ]
                },
            }],
        "influxdb_dump" : {
            "series" : [{
                "name" : 'SOL_TYPE_DUST_NOTIF_HRNEIGHBORS',
                "columns" : [
                    "time",
                    "1:neighborFlag",
                    "1:neighborId",
                    "1:numRxPackets",
                    "1:numTxFailures",
                    "1:numTxPackets",
                    "1:rssi",
                    "2:neighborFlag",
                    "2:neighborId",
                    "2:numRxPackets",
                    "2:numTxFailures",
                    "2:numTxPackets",
                    "2:rssi",
                    "latitude",
                    "longitude",
                    "mac",
                    "site"
                    ],
                "values"    : [[
                    TIMESTAMP,                      # time
                    0,                              # neighborFlag
                    1,                              # neighborId
                    47,                             # numRxPackets
                    0,                              # numTxFailures
                    0,                              # numTxPackets
                    -33,                            # rssi
                    0,                              # neighborFlag
                    2,                              # neighborId
                    2,                              # numRxPackets
                    1,                              # numTxFailures
                    76,                             # numTxPackets
                    -47,                            # rssi
                    "-33.11464",                    # latitude
                    "-68.48015",                    # longitude
                    "00-17-0d-00-00-58-32-36",      # mac
                    "ARG_junin",                    # site
                ]]
            }],
        }
    },
    # SOL_TYPE_DUST_EVENTMOTECREATE
    {
        "json":
            [{
                "timestamp"  : TIMESTAMP,
                "mac"        : "00-17-0d-00-00-58-32-36",
                "type"       : "SOL_TYPE_DUST_EVENTMOTECREATE",
                "value"      : {
                    "latitude"  : "-33.11464",
                    "longitude" : "-68.48015",
                    "site"      : "ARG_junin",
                    "macAddress": "00-17-0d-00-00-58-32-36",
                    "moteId"    : 17
                },
            }],
        "influxdb_dump" : {
            "series" : [{
                "name" : 'SOL_TYPE_DUST_EVENTMOTECREATE',
                "columns" : [
                    "time",
                    "latitude",
                    "longitude",
                    "site",
                    "mac",
                    "macAddress",
                    "moteId"
                    ],
                "values"    : [[
                    TIMESTAMP,                      # time
                    "-33.11464",                    # lat
                    "-68.48015",                    # long
                    "ARG_junin",                    # site
                    "00-17-0d-00-00-58-32-36",      # mac
                    "00-17-0d-00-00-58-32-36",      # macAddress
                    17                              # moteId
                ]]
            }],
        }
    },
]

@pytest.fixture(params=SOL_CHAIN_EXAMPLE)
def sol_chain_example(request):
    return json.dumps(request.param)

#============================ tests =================================

def test_chain(sol_chain_example):
    sol_chain_example = json.loads(sol_chain_example)

    import Sol
    sol = Sol.Sol()

    # influxdb->json
    sol_json  = sol.influxdb_to_json(sol_chain_example["influxdb_dump"])
    print '=====\ninfluxdb->json'
    print sol_chain_example["json"]
    assert sol_json==sol_chain_example["json"]
