from .context import Sol
import pytest
import json
import pprint

from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial

#============================ defines ===============================

MACMANAGER = [3,3,3,3,3,3,3,3]
TIMESTAMP   = "2016-04-19T01:54:16Z"

#============================ fixtures ==============================

SOL_INFLUXJSON_EXAMPLE = [
    # SOL_TYPE_DUST_NOTIF_HRNEIGHBORS (old json_to_influx format)
    {
        "json":
            [{
                "timestamp"  : TIMESTAMP,
                "mac"        : "00-17-0d-00-00-58-32-36",
                "type"       : "SOL_TYPE_DUST_NOTIF_HRNEIGHBORS",
                "value"      : {
                    "numItems"  : "1",
                    "latitude"  : "-33.11464",
                    "longitude" : "-68.48015",
                    "site"      : "ARG_junin",
                    "neighbors" : {
                        "1" :
                            {
                                'neighborId':       1,
                                'neighborFlag':     0,
                                'rssi':             -33,
                                'numTxPackets':     0,
                                'numTxFailures':    0,
                                'numRxPackets':     47,
                            },
                    },
                },
            }],
        "influxdb_dump" : {
            "series" : [{
                "name" : 'SOL_TYPE_DUST_NOTIF_HRNEIGHBORS',
                "tags" : {
                        "mac" : "00-17-0d-00-00-58-32-36",
                    },
                "columns" : [
                    "time",
                    "1:neighborFlag",
                    "1:neighborId",
                    "1:numRxPackets",
                    "1:numTxFailures",
                    "1:numTxPackets",
                    "1:rssi",
                    "neighbors:1:neighborFlag",
                    "neighbors:1:neighborId",
                    "neighbors:1:numRxPackets",
                    "neighbors:1:numTxFailures",
                    "neighbors:1:numTxPackets",
                    "neighbors:1:rssi",
                    "neighbors:2:neighborFlag",
                    "neighbors:2:neighborId",
                    "neighbors:2:numRxPackets",
                    "neighbors:2:numTxFailures",
                    "neighbors:2:numTxPackets",
                    "neighbors:2:rssi",
                    "numItems",
                    "latitude",
                    "longitude",
                    "site",
                    "neighbors",
                    ],
                "values"    : [[
                    TIMESTAMP,                      # time
                    0,                              # neighborFlag
                    1,                              # neighborId
                    47,                             # numRxPackets
                    0,                              # numTxFailures
                    0,                              # numTxPackets
                    -33,                            # rssi
                    None,                           # neighborFlag
                    None,                           # neighborId
                    None,                           # numRxPackets
                    None,                           # numTxFailures
                    None,                           # numTxPackets
                    None,                           # rssi
                    None,                           # neighborFlag
                    None,                           # neighborId
                    None,                           # numRxPackets
                    None,                           # numTxFailures
                    None,                           # numTxPackets
                    None,                           # rssi
                    "1",                            # numItems
                    "-33.11464",                    # latitude
                    "-68.48015",                    # longitude
                    "ARG_junin",                    # site
                ]]
            }],
        }
    },
    # SOL_TYPE_DUST_NOTIF_HRNEIGHBORS
    {
        "json":
            [{
                "timestamp"  : TIMESTAMP,
                "mac"        : "00-17-0d-00-00-58-32-36",
                "type"       : "SOL_TYPE_DUST_NOTIF_HRNEIGHBORS",
                "value"      : {
                    "numItems"  : "2",
                    "latitude"  : "-33.11464",
                    "longitude" : "-68.48015",
                    "site"      : "ARG_junin",
                    "neighbors" : {
                        "1" :
                            {
                                'neighborId':       1,
                                'neighborFlag':     0,
                                'rssi':             -33,
                                'numTxPackets':     0,
                                'numTxFailures':    0,
                                'numRxPackets':     47,
                            },
                        "2" :
                            {
                                'neighborId':       2,
                                'neighborFlag':     0,
                                'rssi':             -47,
                                'numTxPackets':     76,
                                'numTxFailures':    1,
                                'numRxPackets':     2,
                            },
                    },
                },
            }],
        "influxdb_dump" : {
            "series" : [{
                "name" : 'SOL_TYPE_DUST_NOTIF_HRNEIGHBORS',
                "tags" : {
                        "mac" : "00-17-0d-00-00-58-32-36",
                    },
                "columns" : [
                    "time",
                    "neighbors:1:neighborFlag",
                    "neighbors:1:neighborId",
                    "neighbors:1:numRxPackets",
                    "neighbors:1:numTxFailures",
                    "neighbors:1:numTxPackets",
                    "neighbors:1:rssi",
                    "neighbors:2:neighborFlag",
                    "neighbors:2:neighborId",
                    "neighbors:2:numRxPackets",
                    "neighbors:2:numTxFailures",
                    "neighbors:2:numTxPackets",
                    "neighbors:2:rssi",
                    "numItems",
                    "latitude",
                    "longitude",
                    "site",
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
                    "2",                            # numItems
                    "-33.11464",                    # latitude
                    "-68.48015",                    # longitude
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
                "tags" : {
                        "mac" : "00-17-0d-00-00-58-32-36",
                    },
                "columns" : [
                    "time",
                    "latitude",
                    "longitude",
                    "site",
                    "macAddress",
                    "moteId"
                    ],
                "values"    : [[
                    TIMESTAMP,                      # time
                    "-33.11464",                    # lat
                    "-68.48015",                    # long
                    "ARG_junin",                    # site
                    "00-17-0d-00-00-58-32-36",      # macAddress
                    17                              # moteId
                ]]
            }],
        }
    },
]

@pytest.fixture(params=SOL_INFLUXJSON_EXAMPLE)
def sol_influxjson_example(request):
    return json.dumps(request.param)

#============================ tests =================================

def test_influx_to_json(sol_influxjson_example):
    sol_influxjson_example = json.loads(sol_influxjson_example)

    sol = Sol.Sol()

    # influxdb->json
    sol_json  = sol.influxdb_to_json(sol_influxjson_example["influxdb_dump"])
    print '=====\ninfluxdb->json'
    print sol_influxjson_example["json"]
    assert sol_json==sol_influxjson_example["json"]
