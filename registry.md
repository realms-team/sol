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
|   `0xff` | _reserved_                                                                  |
| `0xffff` | _reserved_                                                                  |

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

| macAddress | charge | queueOcc | temperature | batteryVoltage | numTxOk | numTxFail | numRxOk | numRxLost | numMacDropped | numTxBad | badLinkFrameId | badLinkSlot | badLinkOffset |
|------------|--------|----------|-------------|----------------|---------|-----------|---------|-----------|---------------|----------|----------------|-------------|---------------|
|         8B | INT32U |    INT8U |        INT8 |         INT16U |  INT16U |    INT16U |  INT16U |    INT16U |         INT8U |    INT8U |          INT8U |      INT32U |         INT8U |

#### DUST_NOTIF_HR_NEIGHBORS

**JSON representation:**

```
{
    'macAddress': 'xx-xx-xx-xx-xx-xx-xx-xx',
    'neighbors': [
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
}
```

**Binary representation:**

| macAddress | num_neighbors |  _neighbor_ | ... |  _neighbor_ |
|------------|---------------|-------------|-----|-------------|
|         8B |         INT8U | _see below_ | ... | _see below_ |

Where each _neighbor_:

| neighborId | neighborFlag | rssi | numTxPackets | numTxFailures | numRxPackets |
|------------|--------------|------|--------------|---------------|--------------|
|     INT16U |        INT8U | INT8 |       INT16U |        INT16U |       INT16U |

#### DUST_NOTIF_HR_DISCOVERED

**JSON representation:**

```
{
    'macAddress': 'xx-xx-xx-xx-xx-xx-xx-xx',
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

| macAddress | numJoinParents | num_discoveredNeighbors | _discoveredNeighbor_ | ... | _discoveredNeighbor_ |
|------------|----------------|-------------------------|----------------------|-----|----------------------|
|         8B |          INT8U |                   INT8U |          _see below_ | ... |          _see below_ |

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
{
    'xx-xx-xx-xx-xx-xx-xx-xx': {            #=== 8B
        'moteId':                 xx,       # INT16U
        'isAP':                   xx,       # BOOL
        'state':                  xx,       # INT8U
        'isRouting':              xx,       # BOOL
        'numNbrs':                xx,       # INT8U
        'numGoodNbrs':            xx,       # INT8U
        'requestedBw':            xx,       # INT32U
        'totalNeededBw':          xx,       # INT32U
        'assignedBw':             xx,       # INT32U
        'packetsReceived':        xx,       # INT32U
        'packetsLost':            xx,       # INT32U
        'avgLatency':             xx,       # INT32U
        'stateTime':              xx,       # INT32U
        'paths': {
            'xx-xx-xx-xx-xx-xx-xx-xx': {    #=== 8B
                'direction':      xx,       # INT8U
                'numLinks':       xx,       # INT8U
                'quality':        xx,       # INT8U
                'rssiSrcDest':    xx,       # INT8
                'rssiDestSrc':    xx,       # INT8
            },
            ...
        ]
    },
    ...
}
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
