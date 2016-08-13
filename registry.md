When a sensor is associated a well-known length, the `L` (length) field MAY be omitted from its binary representation.
When the well-known length is the table below is "None", the `L` (length) MUST be present in the object's binary representation.

| value    |     name                                                                    |
|---------:|-----------------------------------------------------------------------------|
|   `0x00` | _reserved_                                                                  |
|   `0x01` | [`DISTANCE_JUDD_RS232_RAW`](#distance_judd_rs232_raw)                       |
|   `0x02` | [`DISTANCE_JUDD_RS232_STATS`](#distance_judd_rs232_stats)                   |
|   `0x03` | [`SNOW_MAXBOTIX_MB7554_RS232_RAW`](#snow_maxbotix_mb7554_rs232_raw)         |
|   `0x04` | [`SNOW_MAXBOTIX_MB7554_RS232_STATS`](#snow_maxbotix_mb7554_rs232_stats)     |
|   `0x05` | [`TEMPRH_SENSERION_SHT15_RS232_RAW`](#temprh_senserion_sht15_rs232_raw)     |
|   `0x06` | [`TEMPRH_SENSERION_SHT15_RS232_STATS`](#temprh_senserion_sht15_rs232_stats) |
|   `0x07` | [`TEMPRH_SENSERION_SHT25_RS232_RAW`](#temprh_senserion_sht25_rs232_raw)     |
|   `0x08` | [`TEMPRH_SENSERION_SHT25_RS232_STATS`](#temprh_senserion_sht25_rs232_stats) |
|   `0x09` | [`SOLAR_HUKSEFLUX_LP25_AV_RAW`](#solar_hukseflux_lp25_av_raw)               |
|   `0x0a` | [`SOLAR_HUKSEFLUX_LP25_AV_STATS`](#solar_hukseflux_lp25_av_stats)           |
|   `0x0b` | [`SOIL_DECAGON_GS3_RS232_RAW`](#soil_decagon_gs3_rs232_raw)                 |
|   `0x0c` | [`SOIL_DECAGON_GS3_RS232_STATS`](#soil_decagon_gs3_rs232_stats)             |
|   `0x0d` | [`DUST_NOTIF_LOG`](#dust_notif_log)                                         |
|   `0x0e` | [`DUST_NOTIF_DATA_RAW`](#dust_notif_data_raw)                               |
|   `0x0f` | [`DUST_NOTIF_IPDATA`](#dust_notif_ipdata)                                   |
|   `0x10` | [`DUST_NOTIF_HR_DEVICE`](#dust_notif_hr_device)                             |
|   `0x11` | [`DUST_NOTIF_HR_NEIGHBORS`](#dust_notif_hr_neighbors)                       |
|   `0x12` | [`DUST_NOTIF_HR_DISCOVERED`](#dust_notif_hr_discovered)                     |
|   `0x13` | [`DUST_NOTIF_EVENT_COMMANDFINISHED`](#dust_notif_event_commandfinished)     |
|   `0x14` | [`DUST_NOTIF_EVENT_PATHCREATE`](#dust_notif_event_pathcreate)               |
|   `0x15` | [`DUST_NOTIF_EVENT_PATHDELETE`](#dust_notif_event_pathdelete)               |
|   `0x16` | [`DUST_NOTIF_EVENT_PING`](#dust_notif_event_ping)                           |
|   `0x17` | [`DUST_NOTIF_EVENT_NETWORKTIME`](#dust_notif_event_networktime)             |
|   `0x18` | [`DUST_NOTIF_EVENT_NETWORKRESET`](#dust_notif_event_networkreset)           |
|   `0x19` | [`DUST_NOTIF_EVENT_MOTEJOIN`](#dust_notif_event_motejoin)                   |
|   `0x1a` | [`DUST_NOTIF_EVENT_MOTECREATE`](#dust_notif_event_motecreate)               |
|   `0x1b` | [`DUST_NOTIF_EVENT_MOTEDELETE`](#dust_notif_event_motedelete)               |
|   `0x1c` | [`DUST_NOTIF_EVENT_MOTELOST`](#dust_notif_event_motelost)                   |
|   `0x1d` | [`DUST_NOTIF_EVENT_MOTEOPERATIONAL`](#dust_notif_event_moteoperational)     |
|   `0x1e` | [`DUST_NOTIF_EVENT_MOTERESET`](#dust_notif_event_motereset)                 |
|   `0x1f` | [`DUST_NOTIF_EVENT_PACKETSENT`](#dust_notif_event_packetsent)               |
|   `0x20` | [`DUST_SNAPSHOT`](#dust_snapshot)                                           |
|   `0x21` | [`GS3_DTYPE_ID1D2T2E2N1`]()                                                 |
|   `0x22` | [`JUDD_DTYPE_T2D2R1N1`]()                                                   |
|   `0x23` | [`LP02_DTYPE_IR4N1`]()                                                      |
|   `0x24` | [`MB7554_DTYPE_D2N1NL1NG1`]()                                               |
|   `0x25` | [`SHT15_DTYPE_T4RH4N1`]()                                                   |
|   `0x26` | [` LP02_DTYPE_IRS60`]()                                                     |
|   `0x27` | [`DUST_OAP_TEMPSAMPLE`](#dust_oap_tempsample)                               |
|   `0x28` | [`SOLMANAGER_STATS`](#solmanager_stats)                                     |
|   `0x29` | [`SENS_MB7363_D2S2N1L1G1`](#sens_mb7363_d2s2n1l1g1)                         |
|   `0x30` | [`SENS_GS3_I1D4T4E4N1`](#sens_gs3_i1d4t4e4n1)                               |
|   `0x31` | [`SENS_SHT25_T2N1H2N1`](#sens_sht25_t2n1h2n1)                               |
|   `0x32` | [`SENS_NEOVBAT_V2N1`](#sens_neovbat_v2n1)                                   |
|   `0x37` | [`SENS_ECTM`](#sens_ECTM)                                                   |
|   `0x38` | [`SENS_MPS1`](#sens_MPS1)                                                   |
|   `0xff` | _reserved_                                                                  |
| `0xffff` | _reserved_                                                                  |


#### SENS_NEOVBAT_V2N1

| voltageRaw | nvalid | 
|------------|--------|
|  INT16U    | INT8U  | 

#### SENS_MB7363_D2S2N1L1G1

| distance | stdDev | count | count< | count> |
|----------|--------|-------|--------|--------|
|  INT16U  | INT16U | INT8U | INT8U  | INT8U  |

#### SENS_GS3_I1D4T4E4N1

| id       | dielectric | temp   | elec conduct | count  |
|----------|------------|--------|--------------|--------|
|  INT8U   | FLOAT4     | FLOAT4 |  FLOAT4      | INT8U  |

#### SENS_SHT25_T2N1H2N1

| temp_raw | tcount | rhumidity | rhcount  |
|----------|--------|-----------|----------|
|  INT16U  | INT16U | INT16U    | INT8U    |

#### DISTANCE_JUDD_RS232_RAW

| airtemp | travel_time | distance | retries |
|---------|-------------|----------|---------|
|  INT16U |      INT16U |   INT16U |   INT8U |

#### DISTANCE_JUDD_RS232_STATS

| airtemp | travel_time | distance | retries | count |    std |
|---------|-------------|----------|---------|-------|--------|
|  INT16U |      INT16U |   INT16U |   INT8U | INT8U | INT32U |

#### SNOW_MAXBOTIX_MB7554_RS232_RAW

| distance |
|----------|
|   INT16U |

#### SNOW_MAXBOTIX_MB7554_RS232_STATS

| distance | count |    std |
|----------|-------|--------|
|   INT16U | INT8U | INT32U |

#### TEMPRH_SENSERION_SHT15_RS232_RAW

|   temp |     rH |
|--------|--------|
| INT32U | INT32U |

#### TEMPRH_SENSERION_SHT15_RS232_STATS

|   temp |     rH | count | std_temp | std_rH |
|--------|--------|-------|----------|--------|
| INT32U | INT32U | INT8U |   INT32U | INT32U |

#### TEMPRH_SENSERION_SHT25_RS232_RAW

|   temp |     rH |
|--------|--------|
| INT32U | INT32U |

#### TEMPRH_SENSERION_SHT25_RS232_STATS

|   temp |     rH | count | std_temp | std_rH |
|--------|--------|-------|----------|--------|
| INT32U | INT32U | INT8U |   INT32U | INT32U 

#### SOLAR_HUKSEFLUX_LP25_AV_RAW

|   Vout |
|--------|
| INT32U |

#### SOLAR_HUKSEFLUX_LP25_AV_STATS

|   Vout | count |    std |
|--------|-------|--------|
| INT32U | INT8U | INT32U |

#### SOIL_DECAGON_GS3_RS232_RAW

| moisture | soil_temp | soil_ec |
|----------|-----------|---------|
|   INT32U |    INT32U |  INT32U |

#### SOIL_DECAGON_GS3_RS232_STATS

| moisture | soil_temp | soil_ec | count |    std |
|----------|-----------|---------|-------|--------|
|   INT32U |    INT32U |  INT32U | INT8U | INT32U |

#### DUST_NOTIF_LOG

|    payload |
|------------|
| _variable_ |

#### DUST_NOTIF_DATA_RAW

| srcPort | dstPort |    payload |
|---------|---------|------------|
|  INT16U |  INT16U | _variable_ |

#### DUST_NOTIF_IPDATA

|    payload |
|------------|
| _variable_ |

#### DUST_NOTIF_HR_DEVICE

| charge | queueOcc | temperature | batteryVoltage | numTxOk | numTxFail | numRxOk | numRxLost | numMacDropped | numTxBad | badLinkFrameId | badLinkSlot | badLinkOffset |
|--------|----------|-------------|----------------|---------|-----------|---------|-----------|---------------|----------|----------------|-------------|---------------|
| INT32U |    INT8U |        INT8 |         INT16U |  INT16U |    INT16U |  INT16U |    INT16U |         INT8U |    INT8U |          INT8U |      INT32U |         INT8U |

#### DUST_NOTIF_HR_NEIGHBORS

**JSON representation:**

```
[
    {
        'neighborId':         xx,  # INT16U
        'neighborFlag':       xx,  # INT8U
        'rssi':               xx,  # INT8
        'numTxPackets':       xx,  # INT16U
        'numTxFailures':      xx,  # INT16U
        'numRxPackets':       xx,  # INT16U
    },
    ...
]
```

**Binary representation:**

| num_neighbors |  _neighbor_ | ... |  _neighbor_ |
|---------------|-------------|-----|-------------|
|         INT8U | _see below_ | ... | _see below_ |

Where each _neighbor_:

| neighborId | neighborFlag | rssi | numTxPackets | numTxFailures | numRxPackets |
|------------|--------------|------|--------------|---------------|--------------|
|     INT16U |        INT8U | INT8 |       INT16U |        INT16U |       INT16U |

#### DUST_NOTIF_HR_DISCOVERED

**JSON representation:**

```
{
    'numJoinParents':             xx,  # INT8U
    'discoveredNeighbors': [
        {
            'neighborId':         xx,  # INT16U
            'rssi':               xx,  # INT8
            'numRx':              xx,  # INT8U
        },
        ...
    ]
}
```

**Binary representation:**

| numJoinParents | num_discoveredNeighbors | _discoveredNeighbor_ | ... | _discoveredNeighbor_ |
|----------------|-------------------------|----------------------|-----|----------------------|
|          INT8U |                   INT8U |          _see below_ | ... |          _see below_ |

Where each _discoveredNeighbor_:

| neighborId | rssi | numRx |
|------------|------|-------|
|     INT16U | INT8 | INT8U |

#### DUST_NOTIF_EVENT_COMMANDFINISHED

| callbackId |    rc |
|------------|-------|
|     INT32U | INT8U |

#### DUST_NOTIF_EVENT_PATHCREATE

| source | dest | direction |
|--------|------|-----------|
|     8B |   8B |     INT8U |

#### DUST_NOTIF_EVENT_PATHDELETE

| source | dest | direction |
|--------|------|-----------|
|     8B |   8B |     INT8U |

#### DUST_NOTIF_EVENT_PING

| callbackId | macAddress |  delay | voltage | temperature |
|------------|------------|--------|---------|-------------|
|     INT32U |         8B | INT32U |  INT16U |       INT8U |

#### DUST_NOTIF_EVENT_NETWORKTIME

| uptime | utcTime | asn | asnOffset |
|--------|---------|-----|-----------|
| INT32U |      8B |  5B |    INT16U |

#### DUST_NOTIF_EVENT_NETWORKRESET

_no payload_

#### DUST_NOTIF_EVENT_MOTEJOIN

| macAddress |
|------------|
|         8B |

#### DUST_NOTIF_EVENT_MOTECREATE

| macAddress | moteId |
|------------|--------|
|         8B | INT16U |

#### DUST_NOTIF_EVENT_MOTEDELETE

| macAddress | moteId |
|------------|--------|
|         8B | INT16U |

#### DUST_NOTIF_EVENT_MOTELOST

| macAddress |
|------------|
|         8B |

#### DUST_NOTIF_EVENT_MOTEOPERATIONAL

| macAddress |
|------------|
|         8B |

#### DUST_NOTIF_EVENT_MOTERESET

| macAddress |
|------------|
|         8B |

#### DUST_NOTIF_EVENT_PACKETSENT

| callbackId |    rc |
|------------|-------|
|     INT32U | INT8U |

#### DUST_SNAPSHOT

**JSON representation:**

```
[
    {   'macAddress':          (0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08),
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
                'macAddress':    (0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18),
                'direction':      0x2c,       # INT8U   B
                'numLinks':       0x2d,       # INT8U   B
                'quality':        0x2e,       # INT8U   B
                'rssiSrcDest':    -1,         # INT8    b
                'rssiDestSrc':    -2,         # INT8    b
            },
            {
                'macAddress':    (0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28),
                'direction':      0x2c,       # INT8U  B
                'numLinks':       0x2d,       # INT8U  B
                'quality':        0x2e,       # INT8U  B
                'rssiSrcDest':    -1,         # INT8   b
                'rssiDestSrc':    -2,         # INT8   b
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
                'macAddress':     (0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48),
                'direction':      0x2c,       # INT8U
                'numLinks':       0x2d,       # INT8U
                'quality':        0x2e,       # INT8U
                'rssiSrcDest':    -1,         # INT8
                'rssiDestSrc':    -2,         # INT8
            },
        ],
    },
]
```

**Binary representation:**

| num_motes  |     _mote_ | ... |     _mote_ |
|------------|------------|-----|------------|
|      INT8U | _variable_ | ... | _variable_ |

Where each _mote_:

| macAddress | moteId |  isAP | state | isRouting | numNbrs | numGoodNbrs | requestedBw | totalNeededBw | assignedBw | packetsReceived | packetsLost | avgLatency | stateTime | num_paths |      _path_ | ... |      _path_ |
|------------|--------|-------|-------|-----------|---------|-------------|-------------|---------------|------------|-----------------|-------------|------------|-----------|-----------|-------------|-----|-------------|
|         8B | INT16U | INT8U | INT8U |     INT8U |   INT8U |       INT8U |      INT32U |        INT32U |     INT32U |          INT32U |      INT32U |     INT32U |    INT32U |     INT8U | _see below_ | ... | _see below_ |

Where each _path_:

| macAddress | direction |  numLinks | quality | rssiSrcDest | rssiDestSrc |
|------------|-----------|-----------|---------|-------------|-------------|
|         8B |     INT8U |     INT8U |   INT8U |        INT8 |        INT8 |

#### DUST_OAP_TEMPSAMPLE

| temperature |
|-------------|
|       INT16 |

#### SOLMANAGER_STATS

| sol_version | solmanager_version | sdk_version |
|-------------|--------------------|-------------|
|      INT32U |             INT32U |      INT32U |

#### SENS_MB7363_D2S2N1L1G1

| distance | stdDev | countValid | countLt | countGt |
|----------|--------|------------|---------|---------|
|   INT16U | INT16U |      INT8U |   INT8U |   INT8U |

### SENS_GS3_I1D2T2E2N1
|    id | dielectric | temperature | elec_conduct | countValid |
|-------|------------|-------------|--------------|------------|
| INT8U |     INT16U |      INT16U |       INT16U |      INT8U |

### SENS_SHT25_T2N1H2N1
| temp_raw | t_countV | rhumidity | rh_countV |
|----------|----------|-----------|-----------|
|   INT16U |    INT8U |    INT16U |     INT8U |

### VBAT_DTYPE_V2N1
|  voltage |  numReadings |
|----------|--------------|
|   INT16U |        INT8U |

### SENS_ECTM
|  die_raw |  temp_raw    |  depth  |
|----------|--------------|---------|
|  FLOAT4  |    FLOAT4    | FLOAT4  |
