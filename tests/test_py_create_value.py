import pytest
import json

#============================ defines ===============================

#============================ fixtures ==============================

#============================ helpers ===============================

#============================ tests =================================

def test_create_value_SOL_TYPE_DUST_NOTIF_DATA_RAW():
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_DATA_RAW(
        srcPort    = 0x1122,
        dstPort    = 0x3344,
        payload    = [0x55,0x66],
    )==[0x11,0x22,0x33,0x44,0x55,0x66]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_COMMANDFINISHED():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_COMMANDFINISHED(
        callbackId = 0x11223344,
        rc         = 0x55
    )==[0x11,0x22,0x33,0x44,0x55]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PATHCREATE():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_PATHCREATE(
        source     = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77],
        dest       = [0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff],
        direction  = 0x12,
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,0x12]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PATHDELETE():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_PATHDELETE(
        source     = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77],
        dest       = [0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff],
        direction  = 0x12,
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,0x12]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PING():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_PING(
        callbackId = 0x00112233,
        macAddress = [0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb],
        delay      = 0xccddeeff,
        voltage    = 0x1011,
        temperature= 0x12,
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
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEJOIN(
        macAddress = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEDELETE():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEDELETE(
        macAddress = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77],
        moteId     = 0x8899,
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTELOST():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTELOST(
        macAddress = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEOPERATIONAL():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTEOPERATIONAL(
        macAddress = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTERESET():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_MOTERESET(
        macAddress = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]
    )==[0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77]

def test_create_value_SOL_TYPE_DUST_NOTIF_EVENT_PACKETSENT():    
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_EVENT_PACKETSENT(
        callbackId = 0x11223344,
        rc         = 0x55
    )==[0x11,0x22,0x33,0x44,0x55]

def test_create_value_SOL_TYPE_DUST_NOTIF_HR_DEVICE():
    import Sol
    sol = Sol.Sol()
    
    assert sol.create_value_SOL_TYPE_DUST_NOTIF_HR_DEVICE(
        macAddress = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08],
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
        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08, # macAddress
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
        macAddress = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08],
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
        0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08, # macAddress
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
    
    # TODO
