When a sensor is associated a well-known length, the `L` (length) field MAY be omitted from its binary representation.
When the well-known length is the table below is "None", the `L` (length) MUST be present in the object's binary representation.

| value    |     name                            | well-known length | description |
|---------:|-------------------------------------|------------------:|-------------|
|   `0x00` |                                     |              N.A. | _reserved_  |
|   `0x01` | [`DISTANCE_JUDD_RS232_RAW`](#DISTANCE_JUDD_RS232_RAW)           |               7 B | airtemp (`2B`), travel time (`2B`), distance (`2B`), retries (`1B`) |
|   `0x02` | `DISTANCE_JUDD_RS232_STATS`         |              12 B | airtemp (`2B`), travel time (`2B`), distance (`2B`), retries (`1B`) , num_readings (`1B`) , std readings(`4B`) |
|   `0x03` | `SNOW_MAXBOTIX_MB7554_RS232_RAW`    |               2 B | distance (`2B`) |
|   `0x04` | `SNOW_MAXBOTIX_MB7554_RS232_STATS`  |               7 B | distance (`2B`), num_reading (`1B`), std (`4B`) |
|   `0x05` | `TEMPRH_SENSERION_SHT15_RS232_RAW`  |               8 B | temp (`4B`), rH (`4B`) |
|   `0x06` | `TEMPRH_SENSERION_SHT15_RS232_STATS`|              17 B | temp (`4B`), rH (`4B`), num_readings (`1B`), temp_std (`4B`), rH_std (`4B`)  |
|   `0x07` | `TEMPRH_SENSERION_SHT25_RS232_RAW`  |               8 B | temp (`4B`), rH (`4B`)   |
|   `0x08` | `TEMPRH_SENSERION_SHT25_RS232_STATS`|              17 B | temp (`4B`), rH (`4B`), num_readings (`1B`), temp_std (`4B`), rH_std (`4B`) |
|   `0x09` | `SOLAR_HUKSEFLUX_LP25_AV_RAW`       |               4 B | vout (`4B`) |
|   `0x0a` | `SOLAR_HUKSEFLUX_LP25_AV_STATS`     |               9 B | vout (`4B`) , num_readings (`1B`), std_readings(`4B`) |
|   `0x0b` | `SOIL_DECAGON_GS3_RS232_RAW`        |              12 B | moisture (`4B`), soiltemp (`4B`), soilec (`4B`) |
|   `0x0c` | `SOIL_DECAGON_GS3_RS232_STATS`      |              17 B | moisture (`4B`), soiltemp (`4B`), soilec (`4B`), num_readings (`1B`) , std_readings (`4B`) |
|   `0x0d` | `NOTIF_LOG`                         | _variable length_ | payload (_variable_) |
|   `0x0e` | `NOTIF_DATA_RAW`                    | _variable length_ | srcPort (`2B`), dstPort (`2B`), payload (_variable_) |
|   `0x0f` | `NOTIF_IPDATA`                      | _variable length_ | payload (_variable_) |
|   `0x10` | `NOTIF_HEALTHREPORT`                | _variable length_ | payload (_variable_) |
|   `0x11` | `NOTIF_EVENT_COMMANDFINISHED`       |               5 B | callbackId (`4`), rc (`1`) |
|   `0x12` | `NOTIF_EVENT_PATHCREATE`            |              17 B | source (`8B`), dest (`8B`), direction (`1B`) |
|   `0x13` | `NOTIF_EVENT_PATHDELETE`            |              17 B | source (`8B`), dest (`8B`), direction (`1B`) |
|   `0x14` | `NOTIF_EVENT_PING`                  |              19 B | callbackId (`4B`), macAddress (`8B`), delay (`4B`), voltage (`2B`), temperature (`1B`) |
|   `0x15` | `NOTIF_EVENT_NETWORKTIME`           |              19 B | uptime (`4B`), utcTime (`8B`), asn(`5B`), asnOffset(`2B`) |
|   `0x16` | `NOTIF_EVENT_NETWORKRESET`          |               0 B | N.A. |
|   `0x17` | `NOTIF_EVENT_MOTEJOIN`              |               8 B | macAddress (`8B`) |
|   `0x18` | `NOTIF_EVENT_MOTECREATE`            |              10 B | macAddress (`8B`), moteId (`2B`) |
|   `0x19` | `NOTIF_EVENT_MOTEDELETE`            |              10 B | macAddress (`8B`), moteId (`2B`)  |
|   `0x1a` | `NOTIF_EVENT_MOTELOST`              |               8 B | macAddress (`8B`) |
|   `0x1b` | `NOTIF_EVENT_MOTEOPERATIONAL`       |               8 B | macAddress (`8B`) |
|   `0x1c` | `NOTIF_EVENT_MOTERESET`             |               8 B | macAddress (`8B`) |
|   `0x1d` | `NOTIF_EVENT_PACKETSENT`            |               5 B | callbackId (`4B`), rc (`1`)  |
|   `0xff` |                                     |              N.A. | _reserved_  |   
| `0xffff` |                                     |              N.A. | _reserved_  |

# DISTANCE_JUDD_RS232_RAW