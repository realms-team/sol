import pytest
import json

#============================ defines ===============================

#============================ fixtures ==============================

#============================ helpers ===============================

#============================ tests =================================

def test_create_value_SOL_TYPE_DUST_NOTIF_DATA_RAW():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_DATA_RAW,
        0x1122,                                                 # srcPort
        0x3344,                                                 # dstPort
        [0x55,0x66],                                            # payload
    )==[0x11,0x22,0x33,0x44,0x55,0x66]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_COMMANDFINISHED():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_COMMANDFINISHED,
        0x11223344,     # callbackId
        0x55            # rc
    )==[0x11,0x22,0x33,0x44,0x55]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PATHCREATE():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_PATHCREATE,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77],              # source
        [0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff],              # dest
        0x12,                                                   # direction
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,0x12]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PATHDELETE():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_PATHDELETE,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77],              # source
        [0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff],              # dest
        0x12,                                                   # direction
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,0x12]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PING():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_PING,
        0x00112233,                                             # callbackId
        [0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb],              # macAddress
        0xccddeeff,                                             # delay
        0x1011,                                                 # voltage
        0x12,                                                   # temperature
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,
        0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,
        0x10,0x11,0x12]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_NETWORKTIME():
    import Sol
    sol = Sol.Sol()

    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_NETWORKTIME(
        uptime     = 0x00112233,
        utcSecs    = 0x44556677,
        utcUsecs   = 0x8899aabb,
        asn        = [0xcc,0xdd,0xee,0xff,0x10],
        asnOffset  = 0x1112
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,
        0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,
        0x10,0x11,0x12]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_NETWORKRESET():
    import Sol
    sol = Sol.Sol()

    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_NETWORKRESET()==[]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEJOIN():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_MOTEJOIN,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]               # macAddress
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEDELETE():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_MOTEDELETE,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77],              # macAddress
        0x8899,                                                 # modeId
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTELOST():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_MOTELOST,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]               # macAddress
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEOPERATIONAL():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_MOTEOPERATIONAL,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]               # macAdress
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTERESET():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_MOTERESET,
        [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]               # macAddress
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PACKETSENT():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    assert sol.create_value(
        SolDefines.SOL_TYPE_DUST_NOTIF_EVENT_PACKETSENT,
        0x11223344,                                             # callbackId
        0x55                                                    # rc
    )==[0x11,0x22,0x33,0x44,0x55]

def test_create_value_SOL_TYPE_DUST_NOTIF_HR_DEVICE():
    import Sol
    sol = Sol.Sol()

    assert sol.create_value_SOL_TYPE_DUST_NOTIF_HR_DEVICE(
        hr         = {
            'charge':             0x090a0b0c,    # INT32U
            'queueOcc':           0x0d,          # INT8U
            'temperature':        -1,            # INT8
            'batteryVoltage':     0x0e0f,        # INT16U
            'numTxOk':            0x1011,        # INT16U
            'numTxFail':          0x1213,        # INT16U
            'numRxOk':            0x1415,        # INT16U
            'numRxLost':          0x1617,        # INT16U
            'numMacDropped':      0x18,          # INT8U
            'numTxBad':           0x19,          # INT8U
            'badLinkFrameId':     0x1a,          # INT8U
            'badLinkSlot':        0x1b1c1d1e,    # INT32U
            'badLinkOffset':      0x1f,          # INT8U
        }
    )==[
        0x09,0x0a,0x0b,0x0c,                     # charge
        0x0d,                                    # queueOcc
        0xff,                                    # temperature
        0x0e,0x0f,                               # batteryVoltage
        0x10,0x11,                               # numTxOk
        0x12,0x13,                               # numTxFail
        0x14,0x15,                               # numRxOk
        0x16,0x17,                               # numRxLost
        0x18,                                    # numMacDropped
        0x19,                                    # numTxBad
        0x1a,                                    # badLinkFrameId
        0x1b,0x1c,0x1d,0x1e,                     # badLinkSlot
        0x1f,                                    # badLinkOffset
    ]

def test_create_value_SOL_TYPE_DUST_NOTIF_HR_NEIGHBORS():
    import Sol
    sol = Sol.Sol()

    assert sol.create_value_SOL_TYPE_DUST_NOTIF_HR_NEIGHBORS(
        hr         = {
            'numItems': 2,
            'neighbors': [
                {
                    'neighborId':         0x0102,     # INT16U
                    'neighborFlag':       0x03,       # INT8U
                    'rssi':               -1,         # INT8
                    'numTxPackets':       0x0405,     # INT16U
                    'numTxFailures':      0x0607,     # INT16U
                    'numRxPackets':       0x0809,     # INT16U
                },
                {
                    'neighborId':         0x1112,     # INT16U
                    'neighborFlag':       0x13,       # INT8U
                    'rssi':               -1,         # INT8
                    'numTxPackets':       0x1415,     # INT16U
                    'numTxFailures':      0x1617,     # INT16U
                    'numRxPackets':       0x1819,     # INT16U
                },
            ],
        }
    )==[
        0x02,                                    # num_neighbors
        # neighbor 0
        0x01,0x02,                               # neighborId
        0x03,                                    # neighborFlag
        0xff,                                    # rssi
        0x04,0x05,                               # numTxPackets
        0x06,0x07,                               # numTxFailures
        0x08,0x09,                               # numRxPackets
        # neighbor 1
        0x11,0x12,                               # neighborId
        0x13,                                    # neighborFlag
        0xff,                                    # rssi
        0x14,0x15,                               # numTxPackets
        0x16,0x17,                               # numTxFailures
        0x18,0x19,                               # numRxPackets
    ]

def test_create_value_SOL_TYPE_DUST_NOTIF_HR_DISCOVERED():
    import Sol
    sol = Sol.Sol()

    assert sol.create_value_SOL_TYPE_DUST_NOTIF_HR_DISCOVERED(
        hr         = {
            'numJoinParents': 0x55,              # INT8U
            'numItems':       2,
            'discoveredNeighbors': [
                {
                    'neighborId':     0x0102,    # INT16U
                    'rssi':           -1,        # INT8
                    'numRx':          0x03,      # INT8U
                },
                {
                    'neighborId':     0x1112,    # INT16U
                    'rssi':           -1,        # INT8
                    'numRx':          0x13,      # INT8U
                },
            ],
        }
    )==[
        0x55,                                    # numJoinParents
        0x02,                                    # num_neighbors
        # discoveredNeighbor 0
        0x01,0x02,                               # neighborId
        0xff,                                    # rssi
        0x03,                                    # numRx
        # discoveredNeighbor 1
        0x11,0x12,                               # neighborId
        0xff,                                    # rssi
        0x13,                                    # numRx
    ]

def test_create_value_SOL_TYPE_DUST_SNAPSHOT():
    import Sol
    sol = Sol.Sol()

    assert sol.create_value_SOL_TYPE_DUST_SNAPSHOT(
        summary         = [
            {
                'macAddress':          (0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08),
                'moteId':              0x090a,        # INT16U  H
                'isAP':                0x0b,          # BOOL    B
                'state':               0x0c,          # INT8U   B
                'isRouting':           0x0d,          # BOOL    B
                'numNbrs':             0x0e,          # INT8U   B
                'numGoodNbrs':         0x0f,          # INT8U   B
                'requestedBw':         0x10111213,    # INT32U  I
                'totalNeededBw':       0x14151617,    # INT32U  I
                'assignedBw':          0x18191a1b,    # INT32U  I
                'packetsReceived':     0x1c1d1e1f,    # INT32U  I
                'packetsLost':         0x20212223,    # INT32U  I
                'avgLatency':          0x24252627,    # INT32U  I
                'paths': [
                    {
                        'dest':        (0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18),
                        'direction':   0x2c,          # INT8U   B
                        'numLinks':    0x2d,          # INT8U   B
                        'quality':     0x2e,          # INT8U   B
                        'rssiSrcDest': -1,            # INT8    b
                        'rssiDestSrc': -2,            # INT8    b
                    },
                    {
                        'dest':        (0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28),
                        'direction':   0x2c,          # INT8U  B
                        'numLinks':    0x2d,          # INT8U  B
                        'quality':     0x2e,          # INT8U  B
                        'rssiSrcDest': -1,            # INT8   b
                        'rssiDestSrc': -2,            # INT8   b
                    },
                ],
            },
            {
                'macAddress':          (0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38),
                'moteId':              0x090a,        # INT16U
                'isAP':                0x0b,          # BOOL
                'state':               0x0c,          # INT8U
                'isRouting':           0x0d,          # BOOL
                'numNbrs':             0x0e,          # INT8U
                'numGoodNbrs':         0x0f,          # INT8U
                'requestedBw':         0x10111213,    # INT32U
                'totalNeededBw':       0x14151617,    # INT32U
                'assignedBw':          0x18191a1b,    # INT32U
                'packetsReceived':     0x1c1d1e1f,    # INT32U
                'packetsLost':         0x20212223,    # INT32U
                'avgLatency':          0x24252627,    # INT32U
                'paths': [
                    {
                        'dest':        (0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48),
                        'direction':   0x2c,          # INT8U
                        'numLinks':    0x2d,          # INT8U
                        'quality':     0x2e,          # INT8U
                        'rssiSrcDest': -1,            # INT8
                        'rssiDestSrc': -2,            # INT8
                    },
                ],
            },
        ]
    )==[
        0x02,                                    # num_motes
        # mote 0
        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08, # macAddress
        0x09,0x0a,                               # moteId
        0x0b,                                    # isAP
        0x0c,                                    # state
        0x0d,                                    # isRouting
        0x0e,                                    # numNbrs
        0x0f,                                    # numGoodNbrs
        0x10,0x11,0x12,0x13,                     # requestedBw
        0x14,0x15,0x16,0x17,                     # totalNeededBw
        0x18,0x19,0x1a,0x1b,                     # assignedBw
        0x1c,0x1d,0x1e,0x1f,                     # packetsReceived
        0x20,0x21,0x22,0x23,                     # packetsLost
        0x24,0x25,0x26,0x27,                     # avgLatency
        0x02,                                    # num_paths
        #== path 0
        0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18, # macAddress
        0x2c,                                    # direction
        0x2d,                                    # numLinks
        0x2e,                                    # quality
        0xff,                                    # rssiSrcDest
        0xfe,                                    # rssiDestSrc
        #== path 1
        0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28, # macAddress
        0x2c,                                    # direction
        0x2d,                                    # numLinks
        0x2e,                                    # quality
        0xff,                                    # rssiSrcDest
        0xfe,                                    # rssiDestSrc
        # mote 1
        0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38, # macAddress
        0x09,0x0a,                               # moteId
        0x0b,                                    # isAP
        0x0c,                                    # state
        0x0d,                                    # isRouting
        0x0e,                                    # numNbrs
        0x0f,                                    # numGoodNbrs
        0x10,0x11,0x12,0x13,                     # requestedBw
        0x14,0x15,0x16,0x17,                     # totalNeededBw
        0x18,0x19,0x1a,0x1b,                     # assignedBw
        0x1c,0x1d,0x1e,0x1f,                     # packetsReceived
        0x20,0x21,0x22,0x23,                     # packetsLost
        0x24,0x25,0x26,0x27,                     # avgLatency
        0x01,                                    # num_paths
        #== path 0
        0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48, # macAddress
        0x2c,                                    # direction
        0x2d,                                    # numLinks
        0x2e,                                    # quality
        0xff,                                    # rssiSrcDest
        0xfe,                                    # rssiDestSrc
    ]

def test_create_value():
    import Sol
    import SolDefines
    sol = Sol.Sol()

    #----- FALSE ASSERTIONS -----#
    WRONG_SOL_TYPE = 0xff
    random_data = 666
    with pytest.raises(ValueError):
        sol.create_value(WRONG_SOL_TYPE, random_data)

