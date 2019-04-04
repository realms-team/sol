from math import sqrt as sqrt
import sys

SOL_PORT                                    = 0xf0ba

# type names

SOL_TYPE_DISTANCE_JUDD_RS232_RAW            = 0x01
SOL_TYPE_DISTANCE_JUDD_RS232_STATS          = 0x02
SOL_TYPE_SNOW_MAXBOTIX_MB7554_RS232_RAW     = 0x03
SOL_TYPE_SNOW_MAXBOTIX_MB7554_RS232_STATS   = 0x04
SOL_TYPE_TEMPRH_SENSERION_SHT15_RS232_RAW   = 0x05
SOL_TYPE_TEMPRH_SENSERION_SHT15_RS232_STATS = 0x06
SOL_TYPE_TEMPRH_SENSERION_SHT25_RS232_RAW   = 0x07
SOL_TYPE_TEMPRH_SENSERION_SHT25_RS232_STATS = 0x08
SOL_TYPE_SOLAR_HUKSEFLUX_LP25_AV_RAW        = 0x09
SOL_TYPE_SOLAR_HUKSEFLUX_LP25_AV_STATS      = 0x0a
SOL_TYPE_SOIL_DECAGON_GS3_RS232_RAW         = 0x0b
SOL_TYPE_SOIL_DECAGON_GS3_RS232_STATS       = 0x0c
SOL_TYPE_DUST_NOTIFLOG                      = 0x0d
SOL_TYPE_DUST_NOTIFDATA                     = 0x0e
SOL_TYPE_DUST_NOTIFIPDATA                   = 0x0f
SOL_TYPE_DUST_NOTIF_HRDEVICE                = 0x10
SOL_TYPE_DUST_NOTIF_HRNEIGHBORS             = 0x11
SOL_TYPE_DUST_NOTIF_HRDISCOVERED            = 0x12
SOL_TYPE_DUST_EVENTCOMMANDFINISHED          = 0x13
SOL_TYPE_DUST_EVENTPATHCREATE               = 0x14
SOL_TYPE_DUST_EVENTPATHDELETE               = 0x15
SOL_TYPE_DUST_EVENTPING                     = 0x16
SOL_TYPE_DUST_EVENTNETWORKTIME              = 0x17
SOL_TYPE_DUST_EVENTNETWORKRESET             = 0x18
SOL_TYPE_DUST_EVENTMOTEJOIN                 = 0x19
SOL_TYPE_DUST_EVENTMOTECREATE               = 0x1a
SOL_TYPE_DUST_EVENTMOTEDELETE               = 0x1b
SOL_TYPE_DUST_EVENTMOTELOST                 = 0x1c
SOL_TYPE_DUST_EVENTMOTEOPERATIONAL          = 0x1d
SOL_TYPE_DUST_EVENTMOTERESET                = 0x1e
SOL_TYPE_DUST_EVENTPACKETSENT               = 0x1f
SOL_TYPE_DUST_SNAPSHOT                      = 0x20
SOL_TYPE_DUST_SNAPSHOT_2                    = 0x21
SOL_TYPE_JUDD_T2D2R1N1                      = 0x22
SOL_TYPE_MB7554_DTYPE_D2SD2N1NL1NG1         = 0x24
SOL_TYPE_SHT15_T4RH4N1                      = 0x25
SOL_TYPE_DUST_OAP_TEMPSAMPLE                = 0x27
SOL_TYPE_SOLMANAGER_STATS                   = 0x28
SOL_TYPE_SENS_MB7363_D2S2N1L1G1             = 0x29
SOL_TYPE_SENS_GS3_I1D4T4E4N1                = 0x30
SOL_TYPE_SENS_SHT25_T2N1H2N1                = 0x31
SOL_TYPE_SENS_NEOVBAT_V2N1                  = 0x32
SOL_TYPE_SENS_GS3_I1D4T4E4N1_0              = 0x33
SOL_TYPE_SENS_GS3_I1D4T4E4N1_1              = 0x34
SOL_TYPE_SENS_GS3_I1D4T4E4N1_2              = 0x35
SOL_TYPE_SENS_LP02_R4N1                     = 0x36
SOL_TYPE_SENS_ECTM                          = 0x37
SOL_TYPE_SENS_MPS1                          = 0x38
SOL_TYPE_ADXL362_FFT_Z                      = 0x39
SOL_TYPE_DUST_EVENTJOINFAILED               = 0x3a
SOL_TYPE_SOLMANAGER_STATS_2                 = 0x3b
SOL_TYPE_TEMPRH_SHT31                       = 0x40
SOL_TYPE_DUST_OAP_ANALOG                    = 0x41
SOL_TYPE_DUST_OAP_DIGITAL_IN                = 0x42
SOL_TYPE_TEMPRH_SHT3X                       = 0x43
SOL_TYPE_DUST_NOTIF_HREXTENDED              = 0x44
SOL_TYPE_SENS_MPS6_ID1P4T4N1                = 0x45
SOL_TYPE_SENS_GS1_I1MV2                     = 0x46
SOL_TYPE_SENS_MICROWAVE_MOTION              = 0x47
SOL_TYPE_SENS_INDUCTION_CURRENT_C_SOURCE    = 0x48
SOL_TYPE_SENS_INDUCTION_CURRENT_V_SOURCE    = 0x49

def sol_type_to_type_name(type_id):
    SolDefines = sys.modules[__name__]
    for n in dir(SolDefines):
        if n.startswith('SOL_TYPE_') and getattr(SolDefines, n) == type_id:
            return n
    raise ValueError("SOL type %s does not exist" % type_id)

def sol_name_to_type(type_name):
    SolDefines = sys.modules[__name__]
    if type_name in dir(SolDefines):
        return getattr(SolDefines, type_name)
    raise ValueError("SOL object name %s does not exist" % type_name)

def solStructure(type_id):
    """
    Return the SOL structure according to the given type id
    If the element is not found, it raises a ValueError.

    :param int|str type_id:
    :return: a dictionary that contains the following keys:
        type, description, structure, fields
    """
    if isinstance(type_id, str):
        type_id = sol_name_to_type(type_id)

    sol_item = {}
    for item in sol_types:
        if item['type'] == type_id:
            sol_item = item
    if any(sol_item):
        return sol_item
    else:
        raise ValueError("SOL structure not found for given id:%s" % type_id)

### Dust Constants
MAX_NUM_NEIGHBORS       = 100

### Header

# version

SOL_HDR_V_OFFSET        = 6
SOL_HDR_V               = 0

# Type: single or multi MTtlv

SOL_HDR_T_OFFSET        = 5
SOL_HDR_T_SINGLE        = 0
SOL_HDR_T_MULTI         = 1

# MAC

SOL_HDR_M_OFFSET        = 4
SOL_HDR_M_NOMAC         = 0
SOL_HDR_M_8BMAC         = 1

# timestamp encoding

SOL_HDR_S_OFFSET        = 3
SOL_HDR_S_EPOCH         = 0
SOL_HDR_S_ELIDED        = 1
SOL_HDR_S_SIZE          = 1

# Type encoding

SOL_HDR_Y_OFFSET        = 2
SOL_HDR_Y_1B            = 0
SOL_HDR_Y_2B            = 1

# Length encoding

SOL_HDR_L_OFFSET        = 0
SOL_HDR_L_WK            = 0
SOL_HDR_L_1B            = 1
SOL_HDR_L_2B            = 2
SOL_HDR_L_ELIDED        = 3

### SOL Object

SOL_HEADER_SIZE         = 1
SOL_HEADER_OFFSET       = 0
SOL_TIMESTAMP_SIZE      = 4
SOL_TIMESTAMP_OFFSET    = 1
SOL_OBJNUMBER_SIZE      = 1

### type definitions

sol_types = [
    {
        'type':         SOL_TYPE_DISTANCE_JUDD_RS232_RAW,
        'description':  '',
        'structure':    '>HHHB',
        'fields':       ['airtemp', 'travel_time', 'distance', 'retries'],
    },
    {
        'type':         SOL_TYPE_DISTANCE_JUDD_RS232_STATS,
        'description':  '',
        'structure':    '>HHHBBI',
        'fields':       ['airtemp', 'travel_time', 'distance', 'retries', 'count', 'std'],
    },
    {
        'type':         SOL_TYPE_SNOW_MAXBOTIX_MB7554_RS232_RAW,
        'description':  '',
        'structure':    '>H',
        'fields':       ['distance'],
    },
    {
        'type':         SOL_TYPE_SNOW_MAXBOTIX_MB7554_RS232_STATS,
        'description':  '',
        'structure':    '>HBI',
        'fields':       ['distance', 'count', 'std'],
    },
    {
        'type':         SOL_TYPE_TEMPRH_SENSERION_SHT15_RS232_RAW,
        'description':  '',
        'structure':    '>II',
        'fields':       ['temp', 'rH'],
    },
    {
        'type':         SOL_TYPE_TEMPRH_SENSERION_SHT15_RS232_STATS,
        'description':  '',
        'structure':    '>IIBBII',
        'fields':       ['temp', 'rH', 'count', 'std_temp', 'std_rH'],
    },
    {
        'type':         SOL_TYPE_TEMPRH_SENSERION_SHT25_RS232_RAW,
        'description':  '',
        'structure':    '>II',
        'fields':       ['temp', 'rH'],
    },
    {
        'type':         SOL_TYPE_TEMPRH_SENSERION_SHT25_RS232_STATS,
        'description':  '',
        'structure':    '>IIBII',
        'fields':       ['temp', 'rH', 'count', 'std_temp', 'std_rH'],
    },
    {
        'type':         SOL_TYPE_SOLAR_HUKSEFLUX_LP25_AV_RAW,
        'description':  '',
        'structure':    '>I',
        'fields':       ['Vout'],
    },
    {
        'type':         SOL_TYPE_SOLAR_HUKSEFLUX_LP25_AV_STATS,
        'description':  '',
        'structure':    '>IBI',
        'fields':       ['Vout', 'count', 'std'],
    },
    {
        'type':         SOL_TYPE_SOIL_DECAGON_GS3_RS232_RAW,
        'description':  '',
        'structure':    '>III',
        'fields':       ['moisture', 'soil_temp', 'soil_ec'],
    },
    {
        'type':         SOL_TYPE_SOIL_DECAGON_GS3_RS232_STATS,
        'description':  '',
        'structure':    '>IIIBI',
        'fields':       ['moisture', 'soil_temp', 'soil_ec', 'count', 'std'],
    },
    {
        'type':         SOL_TYPE_DUST_NOTIFDATA,
        'description':  '',
        'structure':    '>HH',
        'fields':       ['srcPort', 'dstPort'],
        'extrafields':  'data',
    },
    {
        'type':         SOL_TYPE_DUST_NOTIF_HRDEVICE,
        'description':  '',
        'structure':    '>IBbHHHHHBBBIBBBB',
        'fields':       [
            'charge',
            'queueOcc',
            'temperature',
            'batteryVoltage',
            'numTxOk',
            'numTxFail',
            'numRxOk',
            'numRxLost',
            'numMacDropped',
            'numTxBad',
            'badLinkFrameId',
            'badLinkSlot',
            'badLinkOffset',
            'numNetMicErr',
            'numMacMicErr',
            'numMacCrcErr',
        ],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTCOMMANDFINISHED,
        'description':  '',
        'structure':    '>IB',
        'fields':       ['callbackId', 'rc'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTPATHCREATE,
        'description':  '',
        'structure':    '>QQB',
        'fields':       ['source', 'dest', 'direction'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTPATHDELETE,
        'description':  '',
        'structure':    '>QQB',
        'fields':       ['source', 'dest', 'direction'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTPING,
        'description':  '',
        'structure':    '>IQIHB',
        'fields':       ['callbackId', 'macAddress', 'delay', 'voltage', 'temperature'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTNETWORKTIME,
        'description':  '',
        'structure':    '>IQ5pH',
        'fields':       ['uptime', 'utcTime', 'asn', 'asnOffset'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTNETWORKRESET,
        'description':  '',
        'structure':    '>',
        'fields':       [],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTMOTEJOIN,
        'description':  '',
        'structure':    '>Q',
        'fields':       ['macAddress'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTMOTECREATE,
        'description':  '',
        'structure':    '>QH',
        'fields':       ['macAddress', 'moteId'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTMOTEDELETE,
        'description':  '',
        'structure':    '>QH',
        'fields':       ['macAddress', 'moteId'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTMOTELOST,
        'description':  '',
        'structure':    '>Q',
        'fields':       ['macAddress'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTMOTEOPERATIONAL,
        'description':  '',
        'structure':    '>Q',
        'fields':       ['macAddress'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTMOTERESET,
        'description':  '',
        'structure':    '>Q',
        'fields':       ['macAddress'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTPACKETSENT,
        'description':  '',
        'structure':    '>IB',
        'fields':       ['callbackId', 'rc'],
    },
    {
        'type':         SOL_TYPE_JUDD_T2D2R1N1,
        'description':  'ultrasonic snow depth and temperature sensor',
        'structure':    '>hHBB',
        'fields':       ['temperature', 'depth', 'numReadings', 'retries'],
    },
    {
        'type': SOL_TYPE_MB7554_DTYPE_D2SD2N1NL1NG1,
        'description': 'mean & stddev of Nval d2g readings',
        'structure': '<HHBBB',
        'fields': ['mean_d2g', 'stdev', 'Nval', 'Nltm', 'NgtM'],
        'apply': [
            {
                'tag': "mean_d2g",
                'function': lambda x: x,
                'args': ['mean_d2g'],
            },
            {
                'tag': "Nval",
                'function': lambda x: x,
                'args': ['Nval'],
            },
            {
                'tag': "stdev",
                'function': lambda x: x,
                'args': ['stdev'],
            }
        ],
    },
    {
        'type':         SOL_TYPE_SHT15_T4RH4N1,
        'description':  'temperature and relative humidity sensor',
        'structure':    '<ffB',
        'fields':       ['temperature', 'rH', 'numReadings'],
    },
    {
        'type':         SOL_TYPE_DUST_OAP_TEMPSAMPLE,
        'description':  '',
        'structure':    '>h',
        'fields':       ['temperature'],
    },
    {
        'type':         SOL_TYPE_SOLMANAGER_STATS,
        'description':  '',
        'structure':    '>III',
        'fields':       ['sol_version', 'solmanager_version', 'sdk_version'],
    },
    {
        'type':         SOL_TYPE_SENS_MB7363_D2S2N1L1G1,
        'description':  'mean & stddev of Nval d2g readings',
        'structure':    '<HHBBB',
        'fields':       ['mean_d2g', 'stdev', 'Nval', 'Nltm', 'NgtM'],
        'apply':        [
                {
                    'tag':     "mean_d2g",
                    'function': lambda x: x,
                    'args':     ['mean_d2g'],
                },
                {
                    'tag':     "Nval",
                    'function': lambda x: x,
                    'args':     ['Nval'],
                },
                {
                    'tag':     "stdev",
                    'function': lambda x: x,
                    'args':     ['stdev'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_SENS_GS3_I1D4T4E4N1,
        'description':  'soil moisture. sub_id indicates depth',
        'structure':    '<BfffB',
        'fields':       ['sub_id', 'dielect', 'temp', 'eleCond', 'Nval'],
        'apply':        [
                {
                    'tag':     "sub_id",
                    'function': lambda x: x,
                    'args':     ['sub_id'],
                },
                {
                    'tag':     "Nval",
                    'function': lambda x: x,
                    'args':     ['Nval'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_SENS_SHT25_T2N1H2N1,
        'description':  'temperature and humidity sensor',
        'structure':    '<HBHB',
        'fields':       ['temp_raw', 't_Nval', 'rh_raw', 'rh_Nval'],
        'apply':        [
                {
                    'field':     "temp_phys",
                    'function': lambda x: -46.85 + 175.72*(float(x)/65536),
                    'args':     ['temp_raw'],
                },
                {
                    'field':     "rh_phys",
                    'function': lambda x:  -6 + 125*(float(x)/65536),
                    'args':     ['rh_raw'],
                },
                {
                    'tag':     "t_Nval",
                    'function': lambda x: x,
                    'args':     ['t_Nval'],
                },
                {
                    'tag':     "rh_Nval",
                    'function': lambda x: x,
                    'args':     ['rh_Nval'],
                }
            ]
    },
    {
        'type':         SOL_TYPE_SENS_NEOVBAT_V2N1,
        'description':  'raw battery voltage of Neomote',
        'structure':    '<hB',
        'fields':       ['voltage', 'N'],
        'apply':        [
                {
                    'field':     "vol_phys",
                    'function': lambda x: float(x)*0.11,
                    'args':     ['voltage'],
                },
                {
                    'tag':     "N",
                    'function': lambda x: x,
                    'args':     ['N'],
                }
            ]
    },
    {
        'type':         SOL_TYPE_SENS_GS3_I1D4T4E4N1_0,
        'description':  'soil moisture at depth 0',
        'structure':    '<fffB',
        'fields':       ['dielect', 'temp', 'eleCond', 'Nval'],
        'apply':        [
                {
                    'tag':     "Nval",
                    'function': lambda x: x,
                    'args':     ['Nval'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_SENS_GS3_I1D4T4E4N1_1,
        'description':  'soil moisture at depth 1',
        'structure':    '<fffB',
        'fields':       ['dielect', 'temp', 'eleCond', 'Nval'],
        'apply':        [
                {
                    'tag':     "Nval",
                    'function': lambda x: x,
                    'args':     ['Nval'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_SENS_GS3_I1D4T4E4N1_2,
        'description':  'soil moisture at depth 2',
        'structure':    '<fffB',
        'fields':       ['dielect', 'temp', 'eleCond', 'Nval'],
        'apply':        [
                {
                    'tag':     "Nval",
                    'function': lambda x: x,
                    'args':     ['Nval'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_SENS_LP02_R4N1,
        'description':  'radiation sensor',
        'structure':    '<iB',
        'fields':       ['irradiance', 'N'],
    },
    {
        'type':         SOL_TYPE_SENS_ECTM,
        'description':  'Decagon ECTM soil moisture and temp',
        'structure':    '<iiif',
        'fields':       ['die_raw', 'EC_raw', 'temp_raw', 'depth'],
        'apply':        [
                {
                    'tag':     "depth",
                    'function': lambda x: x,
                    'args':     ['depth'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_SENS_MPS1,
        'description':  'Decagon MPS1 soil matric potential',
        'structure':    '<ff',
        'fields':       ['die_raw', 'depth'],
        'apply':        [
                {
                    'tag':     "depth",
                    'function': lambda x: x,
                    'args':     ['depth'],
                }
            ],
    },
    {
        'type':         SOL_TYPE_ADXL362_FFT_Z,
        'description':  'highest 5 frequency bins and magnitudes',
        'structure':    '<BBHHHHHHHHHH',
        'fields':       ['conf1', 'conf2', 'f0', 'f1', 'f2', 'f3', 'f4', 'm0', 'm1', 'm2', 'm3', 'm4'],
    },
    {
        'type':         SOL_TYPE_DUST_EVENTJOINFAILED,
        'description':  'generated when a mote sends a join request to the manager but the request can not be validated',
        'structure':    '>QB',
        'fields':       ['macAddress', 'reason'],
    },
    {
        'type':         SOL_TYPE_SOLMANAGER_STATS_2,
        'description':  '',
        'structure':    '>IIIII',
        'fields':       ['sol_version', 'solmanager_version', 'sdk_version',
                         'ram_usage', 'disk_usage'],
    },
    {
        'type':         SOL_TYPE_TEMPRH_SHT31,
        'description':  'temperature and humidity sensor',
        'structure':    '>HHB',
        'fields':       ['temp_raw', 'rh_raw', 'id'],
        'apply':        [
                {
                    'tag':     "id",
                    'function': lambda x: x,
                    'args':     ['id'],
                },
                {
                    'field':     "temp_phys",
                    'function': lambda x:  (x*175.0/0xffff)-45,
                    'args':     ['temp_raw'],
                },
                {
                    'field':     "rh_phys",
                    'function': lambda x:  x*100.0/0xffff,
                    'args':     ['rh_raw'],
                },
            ],
    },
    {
        'type':         SOL_TYPE_TEMPRH_SHT3X,
        'description':  'temperature and humidity sensor',
        'structure':    '<HBHB',
        'fields':       ['temp_raw', 't_Nval', 'rh_raw', 'rh_Nval'],
        'apply':        [
                {
                    'field':     "temp_phys",
                    'function': lambda x:  (x*175.0/0xffff)-45,
                    'args':     ['temp_raw'],
                },
                {
                    'field':     "rh_phys",
                    'function': lambda x:  x*100.0/0xffff,
                    'args':     ['rh_raw'],
                },
            ],
    },
    {
        'type':         SOL_TYPE_SENS_MPS6_ID1P4T4N1,
        'description':  'soil temp and matric potential',
        'structure':    '<BffB',
        'fields':       ['id', 'pot', 'temp', 'Nval'],
    },
    {
        'type':         SOL_TYPE_SENS_GS1_I1MV2,
        'description':  'analog soil moisture',
        'structure':    '<BH',
        'fields':       ['id', 'NmVolts'],
        'apply':        [
                {
                    'tag':     "id",
                    'function': lambda x: x,
                    'args':     ['id'],
                },
                {
                    'field':     "soil_moist",
                    'function': lambda x:  (0.000494 * x -0.554),
                    'args':     ['NmVolts'],
                },
            ],
    },
    {
        'type':         SOL_TYPE_DUST_OAP_ANALOG,
        'description':  'OAP analog sample',
        'structure':    '>Bh',
        'fields':       ['input','voltage'],
    },
    {
        'type':         SOL_TYPE_DUST_OAP_DIGITAL_IN,
        'description':  'OAP digital_in sample',
        'structure':    '>BB',
        'fields':       ['input','state'],
    },
    {
        'type': SOL_TYPE_SENS_MICROWAVE_MOTION,
        'description': 'microwave motion sensor with digital output',
        'structure': '<HB',
        'fields': ['edge_count', 'sensor_id'],
        'apply': [
            {
                'tag': "id",
                'function': lambda x: x,
                'args': ['sensor_id'],
            }
        ],
    },
    {
        'type': SOL_TYPE_SENS_INDUCTION_CURRENT_C_SOURCE,
        'description': 'clamp on current sensor with digital output',
        'structure': '<HB',
        'fields': ['tick_count', 'sensor_id'],
        'apply': [
            {
                'tag': "id",
                'function': lambda x: x,
                'args': ['sensor_id'],
            }
        ],
    },
    {
        'type': SOL_TYPE_SENS_INDUCTION_CURRENT_V_SOURCE,
        'description': 'clamp on current sensor with analog output, raw counts are reported',
        'structure': '<LLHB',
        'fields': ['accu_sum','accu_sum_of_squares', 'sample_count', 'sensor_id'],
        'apply': [
            {
                'tag': "id",
                'function': lambda x: x,
                'args': ['sensor_id'],
            },
            {
                'field': "current_A",
                'function': lambda x,y,z: sqrt(y/float(z)-x*x/float(z)/float(z))*0.001*98.464318,
                'args': ['accu_sum', 'accu_sum_of_squares', 'sample_count'],
            },
        ],
    },
]
