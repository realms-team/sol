When a sensor is associated a well-known length, the `L` (length) field MAY be omitted from its binary representation.
When the well-known length is the table below is "None", the `L` (length) MUST be present in the object's binary representation.

| value    |     name                                                                    |
|---------:|-----------------------------------------------------------------------------|
|   `0x00` |                                                                             |
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
|   `0x0d` | [`NOTIF_LOG`](#notif_log)                                                   |
|   `0x0e` | [`NOTIF_DATA_RAW`](#notif_data_raw)                                         |
|   `0x0f` | [`NOTIF_IPDATA`](#notif_ipdata)                                             |
|   `0x10` | [`NOTIF_HEALTHREPORT`](#notif_healthreport)                                 |
|   `0x11` | [`NOTIF_EVENT_COMMANDFINISHED`](#notif_event_commandfinished)               |
|   `0x12` | [`NOTIF_EVENT_PATHCREATE`](#notif_event_pathcreate)                         |
|   `0x13` | [`NOTIF_EVENT_PATHDELETE`](#notif_event_pathdelete)                         |
|   `0x14` | [`NOTIF_EVENT_PING`](#notif_event_ping)                                     |
|   `0x15` | [`NOTIF_EVENT_NETWORKTIME`](#notif_event_networktime)                       |
|   `0x16` | [`NOTIF_EVENT_NETWORKRESET`](#notif_event_networkreset)                     |
|   `0x17` | [`NOTIF_EVENT_MOTEJOIN`](#notif_event_motejoin)                             |
|   `0x18` | [`NOTIF_EVENT_MOTECREATE`](#notif_event_motecreate)                         |
|   `0x19` | [`NOTIF_EVENT_MOTEDELETE`](#notif_event_motedelete)                         |
|   `0x1a` | [`NOTIF_EVENT_MOTELOST`](#notif_event_motelost)                             |
|   `0x1b` | [`NOTIF_EVENT_MOTEOPERATIONAL`](#notif_event_moteoperational)               |
|   `0x1c` | [`NOTIF_EVENT_MOTERESET`](#notif_event_motereset)                           |
|   `0x1d` | [`NOTIF_EVENT_PACKETSENT`](#notif_event_packetsent)                         |
|   `0xff` |                                                                             |
| `0xffff` |                                                                             |

#### DISTANCE_JUDD_RS232_RAW

| airtemp | travel_time | distance | retries |
|---------|-------------|----------|---------|
|  INT16U |      INT16U |   INT16U |   INT8U |

#### DISTANCE_JUDD_RS232_STATS

| airtemp | travel_time | distance | retries | num_readings | std_readings |
|---------|-------------|----------|---------|--------------|--------------|
|  INT16U |      INT16U |   INT16U |   INT8U |        INT8U |       INT32U |

#### SNOW_MAXBOTIX_MB7554_RS232_RAW

| distance |
|----------|
|   INT16U |

#### SNOW_MAXBOTIX_MB7554_RS232_STATS

| distance | num_reading |    std |
|----------|-------------|--------|
|   INT16U |       INT8U | INT32U |

#### TEMPRH_SENSERION_SHT15_RS232_RAW

|   temp |     rH |
|--------|--------|
| INT32U | INT32U |

#### TEMPRH_SENSERION_SHT15_RS232_STATS

|   temp |     rH | num_readings | temp_std | rH_std |
|--------|--------|--------------|----------|--------|
| INT32U | INT32U |        INT8U |   INT32U | INT32U |

#### TEMPRH_SENSERION_SHT25_RS232_RAW

|   temp |     rH |
|--------|--------|
| INT32U | INT32U |

#### TEMPRH_SENSERION_SHT25_RS232_STATS

|   temp |     rH | num_readings | temp_std | rH_std |
|--------|--------|--------------|----------|--------|
| INT32U | INT32U |        INT8U |   INT32U | INT32U |

#### SOLAR_HUKSEFLUX_LP25_AV_RAW

|   vout |
|--------|
| INT32U |

#### SOLAR_HUKSEFLUX_LP25_AV_STATS

|   vout | num_reading |    std |
|--------|-------------|--------|
| INT32U |       INT8U | INT32U |

#### SOIL_DECAGON_GS3_RS232_RAW

| moisture | soiltemp | soilec |
|----------|----------|--------|
|   INT32U |   INT32U | INT32U |

#### SOIL_DECAGON_GS3_RS232_STATS

| moisture | soiltemp | soilec | num_reading |    std |
|----------|----------|--------|-------------|--------|
|   INT32U |   INT32U | INT32U |       INT8U | INT32U |

#### NOTIF_LOG

|    payload |
|------------|
| _variable_ |

#### NOTIF_DATA_RAW

| srcPort | dstPort |    payload |
|---------|---------|------------|
|  INT16U |  INT16U | _variable_ |

#### NOTIF_IPDATA

|    payload |
|------------|
| _variable_ |

#### NOTIF_HEALTHREPORT

|    payload |
|------------|
| _variable_ |

#### NOTIF_EVENT_COMMANDFINISHED

| callbackId |    rc |
|------------|-------|
|     INT32U | INT8U |

#### NOTIF_EVENT_PATHCREATE

| source | dest | direction |
|--------|------|-----------|
|     8B |   8B |     INT8U |

#### NOTIF_EVENT_PATHDELETE

| source | dest | direction |
|--------|------|-----------|
|     8B |   8B |     INT8U |

#### NOTIF_EVENT_PING

| callbackId | macAddress |  delay | voltage | temperature |
|------------|------------|--------|---------|-------------|
|     INT32U |         8B | INT32U |  INT16U |       INT8U |

#### NOTIF_EVENT_NETWORKTIME

| uptime | utcTime | asn | asnOffset |
|--------|---------|-----|-----------|
| INT32U |      8B |  5B |    INT16U |

#### NOTIF_EVENT_NETWORKRESET

_no payload_

#### NOTIF_EVENT_MOTEJOIN

| macAddress |
|------------|
|         8B |

#### NOTIF_EVENT_MOTECREATE

| macAddress | moteId |
|------------|--------|
|         8B | INT16U |

#### NOTIF_EVENT_MOTEDELETE

| macAddress | moteId |
|------------|--------|
|         8B | INT16U |

#### NOTIF_EVENT_MOTELOST

| macAddress |
|------------|
|         8B |

#### NOTIF_EVENT_MOTEOPERATIONAL

| macAddress |
|------------|
|         8B |

#### NOTIF_EVENT_MOTERESET

| macAddress |
|------------|
|         8B |

#### NOTIF_EVENT_PACKETSENT

| callbackId |    rc |
|------------|-------|
|     INT32U | INT8U |
