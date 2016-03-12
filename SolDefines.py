SOL_PORT                = 0xf0ba
OAP_PORT                = 0xf0b9

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
SOL_TYPE_DUST_NOTIF_LOG                     = 0x0d
SOL_TYPE_DUST_NOTIF_DATA_RAW                = 0x0e
SOL_TYPE_DUST_NOTIF_IPDATA                  = 0x0f
SOL_TYPE_DUST_NOTIF_HR_DEVICE               = 0x10
SOL_TYPE_DUST_NOTIF_HR_NEIGHBORS            = 0x11
SOL_TYPE_DUST_NOTIF_HR_DISCOVERED           = 0x12
SOL_TYPE_DUST_NOTIF_EVENT_COMMANDFINISHED   = 0x13
SOL_TYPE_DUST_NOTIF_EVENT_PATHCREATE        = 0x14
SOL_TYPE_DUST_NOTIF_EVENT_PATHDELETE        = 0x15
SOL_TYPE_DUST_NOTIF_EVENT_PING              = 0x16
SOL_TYPE_DUST_NOTIF_EVENT_NETWORKTIME       = 0x17
SOL_TYPE_DUST_NOTIF_EVENT_NETWORKRESET      = 0x18
SOL_TYPE_DUST_NOTIF_EVENT_MOTEJOIN          = 0x19
SOL_TYPE_DUST_NOTIF_EVENT_MOTECREATE        = 0x1a
SOL_TYPE_DUST_NOTIF_EVENT_MOTEDELETE        = 0x1b
SOL_TYPE_DUST_NOTIF_EVENT_MOTELOST          = 0x1c
SOL_TYPE_DUST_NOTIF_EVENT_MOTEOPERATIONAL   = 0x1d
SOL_TYPE_DUST_NOTIF_EVENT_MOTERESET         = 0x1e
SOL_TYPE_DUST_NOTIF_EVENT_PACKETSENT        = 0x1f
SOL_TYPE_DUST_SNAPSHOT                      = 0x20
SOL_TYPE_DUST_OAP                           = 0x27


def solTypeToString(solDefinesClass,sol_type):
    for k in dir(solDefinesClass):
        if k.startswith('SOL_TYPE_') and getattr(solDefinesClass,k)==sol_type:
            return k
    return "UNKNOWN!"

# header

SOL_HDR_V_OFFSET        = 6
SOL_HDR_V               = 0

SOL_HDR_H_OFFSET        = 5
SOL_HDR_H_START         = 0
SOL_HDR_H_MORE          = 1
SOL_HDR_H_ALL           = [
    SOL_HDR_H_START,
    SOL_HDR_H_MORE,
]

# "start" header

SOL_HDR_START_M_OFFSET  = 4
SOL_HDR_START_M_NOMAC   = 0
SOL_HDR_START_M_8BMAC   = 1
SOL_HDR_START_M_ALL     = [
    SOL_HDR_START_M_NOMAC,
    SOL_HDR_START_M_8BMAC,
]

SOL_HDR_START_S_OFFSET  = 3
SOL_HDR_START_S_EPOCH   = 0
SOL_HDR_START_S_ELIDED  = 1
SOL_HDR_START_S_ALL     = [
    SOL_HDR_START_S_EPOCH,
    SOL_HDR_START_S_ELIDED,
]

SOL_HDR_START_Y_OFFSET  = 2
SOL_HDR_START_Y_1B      = 0
SOL_HDR_START_Y_2B      = 1
SOL_HDR_START_Y_ALL     = [
    SOL_HDR_START_Y_1B,
    SOL_HDR_START_Y_2B,
]

SOL_HDR_START_L_OFFSET  = 0
SOL_HDR_START_L_WK      = 0
SOL_HDR_START_L_1B      = 1
SOL_HDR_START_L_2B      = 2
SOL_HDR_START_L_ELIDED  = 3
SOL_HDR_START_L_ALL     = [
    SOL_HDR_START_L_WK,
    SOL_HDR_START_L_1B,
    SOL_HDR_START_L_2B,
    SOL_HDR_START_L_ELIDED,
]

# "more" header

SOL_HDR_MORE_S_OFFSET   = 4
SOL_HDR_MORE_S_NONE     = 0
SOL_HDR_MORE_S_INHERIT  = 1
SOL_HDR_MORE_S_ALL      = [
    SOL_HDR_MORE_S_NONE,
    SOL_HDR_MORE_S_INHERIT,
]

SOL_HDR_MORE_Y_OFFSET   = 3
SOL_HDR_MORE_Y_NONE     = 0
SOL_HDR_MORE_Y_INHERIT  = 1
SOL_HDR_MORE_Y_ALL      = [
    SOL_HDR_MORE_Y_NONE,
    SOL_HDR_MORE_Y_INHERIT,
]

SOL_HDR_MORE_L_OFFSET   = 3
SOL_HDR_MORE_L_NONE     = 0
SOL_HDR_MORE_L_INHERIT  = 1
SOL_HDR_MORE_L_ALL      = [
    SOL_HDR_MORE_L_NONE,
    SOL_HDR_MORE_L_INHERIT,
]

SOL_HDR_MORE_N_OFFSET   = 3
SOL_HDR_MORE_N_2        = 0
SOL_HDR_MORE_N_8        = 1
SOL_HDR_MORE_N_16       = 2
SOL_HDR_MORE_N_EXPLICIT = 3
SOL_HDR_MORE_N_ALL      = [
    SOL_HDR_MORE_N_2,
    SOL_HDR_MORE_N_8,
    SOL_HDR_MORE_N_16,
    SOL_HDR_MORE_N_EXPLICIT,
]

# type definitions

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
]







