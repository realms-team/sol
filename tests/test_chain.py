import pytest
import json
import pprint
import os

from SmartMeshSDK.IpMgrConnectorSerial  import IpMgrConnectorSerial

#============================ defines ===============================

MACMANAGER = [3,3,3,3,3,3,3,3]
TIMESTAMP   = 0x05050505

#============================ fixtures ==============================

SOL_CHAIN_EXAMPLE = [
    # SOL_TYPE_DUST_NOTIF_DATA_RAW
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(    \
                utcSecs      = 1111,                                 \
                utcUsecs     = 222,                                  \
                macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],             \
                srcPort      = 0x0102,                               \
                dstPort      = 0x0304,                               \
                data         = (0x05,0x06,0x07,0x08),                \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x0e,
                "value"      : {
                    'srcPort': 0x0102,
                    'dstPort': 0x0304,
                    'data'   : [0x05,0x06,0x07,0x08],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x0e,                                      # type
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIBQUFBQ4BAgMEBQYHCA=="     \
                ]                                          \
            }',
        "influxdb":
            {
                "time"          : TIMESTAMP*1000000000,
                "tags"          : {
                    'mac'       : '01-02-03-04-05-06-07-08',
                    'site'      : 'test2',
                    'latitude'  : '-55.5555',
                    'longitude' : '-44.4444',
                },
                "measurement"   : 'SOL_TYPE_DUST_NOTIFDATA',
                "fields"        : {
                    'srcPort'   : 0x0102,
                    'dstPort'   : 0x0304,
                    'data'      : '05-06-07-08',
                },
            },
    },
    # SOL_TYPE_DUST_NOTIF_HRDEVICE
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifHealthReport( \
                macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                payload      = [128, 24, 0, 0, 0, 40, 49, 25, 11,119, 0, 26, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],            \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x10,
                "value"      : {
                    'charge':             40,
                    'queueOcc':           49,
                    'temperature':        25,
                    'batteryVoltage':     2935,
                    'numTxOk':            26,
                    'numTxFail':          0,
                    'numRxOk':            9,
                    'numRxLost':          0,
                    'numMacDropped':      0,
                    'numTxBad':           0,
                    'badLinkFrameId':     0,
                    'badLinkSlot':        0,
                    'badLinkOffset':      0,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x10,                                      # type
                0, 0, 0, 40, 49, 25, 11,119, 0, 26, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,   # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIBQUFBRAAAAAoMRkLdwAaAAAACQAAAAAAAAAAAAA="     \
                ]                                          \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '01-02-03-04-05-06-07-08',
                    'site'      : 'test2',
                    'latitude'  : '-55.5555',
                    'longitude' : '-44.4444',
                },
                "measurement": 'SOL_TYPE_DUST_NOTIF_HRDEVICE',
                "fields"     : {
                    'charge':             40,
                    'queueOcc':           49,
                    'temperature':        25,
                    'batteryVoltage':     2935,
                    'numTxOk':            26,
                    'numTxFail':          0,
                    'numRxOk':            9,
                    'numRxLost':          0,
                    'numMacDropped':      0,
                    'numTxBad':           0,
                    'badLinkFrameId':     0,
                    'badLinkSlot':        0,
                    'badLinkOffset':      0,
                },
            },
    },
    # SOL_TYPE_DUST_NOTIF_HRNEIGHBORS
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifHealthReport( \
                macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                payload      = [129, 31, 3, 0, 3, 0, 223, 0, 0, 0, 0, 0, 47, 0, 1, 0, 209, 0, 76, 0, 1, 0, 2, 0, 4, 0, 211, 0, 30, 0, 0, 0, 1],            \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x11,
                "value"      : {
                    'numItems': 3,
                    'neighbors': [
                        {
                            'neighborId':       3,
                            'neighborFlag':     0,
                            'rssi':             -33,
                            'numTxPackets':     0,
                            'numTxFailures':    0,
                            'numRxPackets':     47,
                        },
                        {
                            'neighborId':       1,
                            'neighborFlag':     0,
                            'rssi':             -47,
                            'numTxPackets':     76,
                            'numTxFailures':    1,
                            'numRxPackets':     2,
                        },
                        {
                            'neighborId':      4,
                            'neighborFlag':    0,
                            'rssi':            -45,
                            'numTxPackets':    30,
                            'numTxFailures':   0,
                            'numRxPackets':    1,
                        },
                    ]
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x11,                                      # type
                3, 0, 3, 0, 223, 0, 0, 0, 0, 0, 47, 0, 1, 0, 209, 0, 76, 0, 1, 0, 2, 0, 4, 0, 211, 0, 30, 0, 0, 0, 1,   # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIBQUFBREDAAMA3wAAAAAALwABANEATAABAAIABADTAB4AAAAB"     \
                ]                                          \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '01-02-03-04-05-06-07-08',
                    'site'      : 'test2',
                    'latitude'  : '-55.5555',
                    'longitude' : '-44.4444',
                },
                "measurement": 'SOL_TYPE_DUST_NOTIF_HRNEIGHBORS',
                "fields"     : {
                    '3:neighborId':         3,
                    '3:neighborFlag':       0,
                    '3:rssi':               -33,
                    '3:numTxPackets':       0,
                    '3:numTxFailures':      0,
                    '3:numRxPackets':       47,
                    '1:neighborId':         1,
                    '1:neighborFlag':       0,
                    '1:rssi':               -47,
                    '1:numTxPackets':       76,
                    '1:numTxFailures':      1,
                    '1:numRxPackets':       2,
                    '4:neighborId':         4,
                    '4:neighborFlag':       0,
                    '4:rssi':               -45,
                    '4:numTxPackets':       30,
                    '4:numTxFailures':      0,
                    '4:numRxPackets':       1,
                    'numItems':             3,
                },
            },
    },
    # SOL_TYPE_DUST_NOTIF_HRDISCOVERED
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifHealthReport( \
                macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                payload      = [130, 14, 3, 3, 0, 6, 178, 2, 0, 5, 169, 1, 0, 7, 185, 1],            \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x12,
                "value"      : {
                    'numJoinParents': 3,
                    'numItems': 3,
                    'discoveredNeighbors': [
                        {
                            'neighborId': 6,
                            'rssi': -78,
                            'numRx': 2,
                        },
                        {
                            'neighborId': 5,
                            'rssi': -87,
                            'numRx': 1,
                        },
                        {
                            'neighborId': 7,
                            'rssi': -71,
                            'numRx': 1,
                        },
                    ]
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x12,                                      # type
                3, 3, 0, 6, 178, 2, 0, 5, 169, 1, 0, 7, 185, 1,   # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIBQUFBRIDAwAGsgIABakBAAe5AQ=="     \
                ]                                          \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '01-02-03-04-05-06-07-08',
                    'site'      : 'test2',
                    'latitude'  : '-55.5555',
                    'longitude' : '-44.4444',
                },
                "measurement": 'SOL_TYPE_DUST_NOTIF_HRDISCOVERED',
                "fields"     : {
                    'discoveredNeighbors:0:neighborId':    6,
                    'discoveredNeighbors:0:numRx':         2,
                    'discoveredNeighbors:0:rssi':          -78,
                    'discoveredNeighbors:1:neighborId':    5,
                    'discoveredNeighbors:1:numRx':         1,
                    'discoveredNeighbors:1:rssi':          -87,
                    'discoveredNeighbors:2:neighborId':    7,
                    'discoveredNeighbors:2:numRx':         1,
                    'discoveredNeighbors:2:rssi':          -71,
                    'numItems':                            3,
                    'numJoinParents':                      3,
                },
            },
    },
    # SOL_TYPE_DUST_NOTIF_HRDEVICE + SOL_TYPE_DUST_NOTIF_HRDISCOVERED
    # TODO [128, 24, 0, 0, 0, 71, 49, 16, 10, 56, 1, 96, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 130, 14, 3, 3, 0, 6, 178, 2, 0, 5, 169, 1, 0, 7, 185, 1]
    # SOL_TYPE_DUST_EVENTPATHCREATE
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventPathCreate(   \
                eventId      = 0x11223344,                                \
                source       = [1,1,1,1,1,1,1,1],                         \
                dest         = [2,2,2,2,2,2,2,2],                         \
                direction    = 3,                                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x14,
                "value"      : {
                    'source'      : [1,1,1,1,1,1,1,1],
                    'dest'        : [2,2,2,2,2,2,2,2],
                    'direction'   : 3,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x14,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
                0x03,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRQBAQEBAQEBAQICAgICAgICAw=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTPATHCREATE',
                "fields"     : {
                    'source'      : '01-01-01-01-01-01-01-01',
                    'dest'        : '02-02-02-02-02-02-02-02',
                    'direction'   : 3,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTPATHDELETE
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventPathDelete(   \
                eventId      = 0x11223344,                                \
                source       = [1,1,1,1,1,1,1,1],                         \
                dest         = [2,2,2,2,2,2,2,2],                         \
                direction    = 3,                                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x15,
                "value"      : {
                    'source'      : [1,1,1,1,1,1,1,1],
                    'dest'        : [2,2,2,2,2,2,2,2],
                    'direction'   : 3,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x15,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,
                0x03,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRUBAQEBAQEBAQICAgICAgICAw=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTPATHDELETE',
                "fields"     : {
                    'source'      : '01-01-01-01-01-01-01-01',
                    'dest'        : '02-02-02-02-02-02-02-02',
                    'direction'   : 3,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTEJOIN
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteJoin(     \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x19,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x19,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRkBAQEBAQEBAQ=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTEJOIN',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTECREATE
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteCreate(   \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
                moteId       = 0x0202,                                    \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1a,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                    'moteId'      : 0x0202,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1a,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRoBAQEBAQEBAQIC"   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTECREATE',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                    'moteId'      : 0x0202,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTEDELETE
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteDelete(   \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
                moteId       = 0x0202,                                    \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1b,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                    'moteId'      : 0x0202,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1b,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
                0x02,0x02,
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRsBAQEBAQEBAQIC"   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTEDELETE',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                    'moteId'      : 0x0202,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTELOST
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteLost(     \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1c,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1c,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBRwBAQEBAQEBAQ=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTELOST',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                },
            },
    },
    # SOL_TYPE_DUST_EVENTMOTEOPERATIONAL
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventMoteOperational(     \
                eventId      = 0x11223344,                                \
                macAddress   = [1,1,1,1,1,1,1,1],                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x1d,
                "value"      : {
                    'macAddress'  : [1,1,1,1,1,1,1,1],
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x1d,                                      # type
                0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,   # value
            ],
        "http":
            '{                                                       \
                "v" : 0,                                             \
                "o" : [                                              \
                    "EwMDAwMDAwMDBQUFBR0BAQEBAQEBAQ=="   \
                ]                                                    \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTMOTEOPERATIONAL',
                "fields"     : {
                    'macAddress'  : '01-01-01-01-01-01-01-01',
                },
            },
    },
    # SOL_TYPE_DUST_OAP_TEMPSAMPLE
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_notifData(         \
                utcSecs      = 1111,                                      \
                utcUsecs     = 222,                                       \
                macAddress   = [1, 2, 3, 4, 5, 6, 7, 8],                  \
                srcPort      = 0xf0b9,                                    \
                dstPort      = 0xf0b9,                                    \
                data         = (  0,   0,   5,   0, 255,   1,   5,   0,   \
                                  0,   0,   0,  61,  34, 107,  74,   0,   \
                                 13, 104, 164,   0,   0, 117,  48,   1,   \
                                 16,0xff,0xff                             \
                               ),                                         \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : [1, 2, 3, 4, 5, 6, 7, 8],
                "type"       : 0x27,
                "value"      : {
                    'temperature': -1,
                },
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x27,                                      # type
                0xff,0xff,                                 # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwECAwQFBgcIBQUFBSf//w=="             \
                ]                                          \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '01-02-03-04-05-06-07-08',
                    'site'      : 'test2',
                    'latitude'  : '-55.5555',
                    'longitude' : '-44.4444',
                },
                "measurement": 'SOL_TYPE_DUST_OAP_TEMPSAMPLE',
                "fields"     : {
                    'temperature': -1,
                },
            },
    },
    # SOL_TYPE_DUST_EVENTNETWORKRESET
    {
        "dust":
            "IpMgrConnectorSerial.IpMgrConnectorSerial.Tuple_eventNetworkReset(         \
                eventId      = 0x11223344,                                \
            )",
        "json":
            {
                "timestamp"  : TIMESTAMP,
                "mac"        : MACMANAGER,
                "type"       : 0x18,
                "value"      : {},
            },
        "bin":
            [
                #ver   type   MAC    ts    typelen length
                0<<6 | 0<<5 | 1<<4 | 0<<3 | 0<<2 | 3<<0,   # header
                0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,   # mac
                0x05,0x05,0x05,0x05,                       # timestamp
                0x18,                                      # type
                                                           # value
            ],
        "http":
            '{                                             \
                "v" : 0,                                   \
                "o" : [                                    \
                    "EwMDAwMDAwMDBQUFBRg="                 \
                ]                                          \
            }',
        "influxdb":
            {
                "time"       : TIMESTAMP*1000000000,
                "tags"       : {
                    'mac'    : '03-03-03-03-03-03-03-03',
                    'site'      : 'test1',
                    'latitude'  : '-11.1111',
                    'longitude' : '-22.2222',
                },
                "measurement": 'SOL_TYPE_DUST_EVENTNETWORKRESET',
                "fields"     : {'value': 'dummy'},
            },
    },
]

@pytest.fixture(params=SOL_CHAIN_EXAMPLE)
def sol_chain_example(request):
    return json.dumps(request.param)

FILES = [
    {
        "file_name"     : "sites/test1.csv",
        "file_content"  : (
                        "03-03-03-03-03-03-03-03,-11.1111,-22.2222\n"
                        "00-11-22-33-44-55-66-77,-33.3333,-44.4444\n"
                    ),
    },
    {
        "file_name"     : "sites/test2.csv",
        "file_content"  : (
                        "11-11-11-11-11-11-11-11,-11.1111,-22.2222\n"
                        "01-02-03-04-05-06-07-08,-55.5555,-44.4444\n"
                    ),
    }
]

@pytest.fixture()
def write_test_file(request):
    for param in FILES:
        test_file = open(param['file_name'], 'w')
        test_file.write(param['file_content'])
        test_file.close()

    def remove_file():
        for param in FILES:
            os.remove(param['file_name'])

    request.addfinalizer(remove_file)

#============================ helpers ===============================

pp = pprint.PrettyPrinter(indent=4)

#============================ tests =================================

def test_chain(sol_chain_example, write_test_file):
    sol_chain_example = json.loads(sol_chain_example)

    import Sol
    sol = Sol.Sol()

    # dust->json
    sol_json  = sol.dust_to_json(
       eval(sol_chain_example["dust"]),
       macManager  = MACMANAGER,
       timestamp   = TIMESTAMP,
    )
    print '=====\ndust->json'
    print sol_json
    print sol_chain_example["json"]
    assert sol_json==sol_chain_example["json"]
    
    # json->bin
    sol_bin   = sol.json_to_bin(sol_json)
    print '=====\njson->bin'
    print sol_bin
    print sol_chain_example["bin"]
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->http
    sol_http  = sol.bin_to_http([sol_bin])
    print '=====\nbin->http'
    print sol_http
    print sol_chain_example["http"]
    assert json.loads(sol_http)==json.loads(sol_chain_example["http"])
    
    # http->bin
    sol_binl  = sol.http_to_bin(sol_http)
    assert len(sol_binl)==1
    sol_bin = sol_binl[0]
    print '=====\nhttp->bin'
    print sol_bin
    print sol_chain_example["bin"]
    assert sol_bin==sol_chain_example["bin"]
    
    # bin->json
    sol_json  = sol.bin_to_json(sol_bin)
    print '=====\nbin->json'
    print sol_json
    print sol_chain_example["json"]
    assert sol_json==sol_chain_example["json"]
    
    # json->influxdb
    sol_influxdb  = sol.json_to_influxdb(sol_json)
    print '=====\njson->influxdb'
    pp.pprint(sol_influxdb)
    print sol_chain_example["influxdb"]
    assert sol_influxdb==sol_chain_example["influxdb"]
