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
|   `0x0d` | [`DUST_NOTIFLOG`](#dust_notiflog)                                           |
|   `0x0e` | [`DUST_NOTIFDATA`](#dust_notifdata)                                         |
|   `0x0f` | [`DUST_NOTIFIPDATA`](#dust_notifipdata)                                     |
|   `0x10` | [`DUST_NOTIF_HRDEVICE`](#dust_notif_hrdevice)                               |
|   `0x11` | [`DUST_NOTIF_HRNEIGHBORS`](#dust_notif_hrneighbors)                         |
|   `0x12` | [`DUST_NOTIF_HRDISCOVERED`](#dust_notif_hrdiscovered)                       |
|   `0x13` | [`DUST_EVENTCOMMANDFINISHED`](#dust_eventcommandfinished)                   |
|   `0x14` | [`DUST_EVENTPATHCREATE`](#dust_eventpathcreate)                             |
|   `0x15` | [`DUST_EVENTPATHDELETE`](#dust_eventpathdelete)                             |
|   `0x16` | [`DUST_EVENTPING`](#dust_eventping)                                         |
|   `0x17` | [`DUST_EVENTNETWORKTIME`](#dust_eventnetworktime)                           |
|   `0x18` | [`DUST_EVENTNETWORKRESET`](#dust_eventnetworkreset)                         |
|   `0x19` | [`DUST_EVENTMOTEJOIN`](#dust_eventmotejoin)                                 |
|   `0x1a` | [`DUST_EVENTMOTECREATE`](#dust_eventmotecreate)                             |
|   `0x1b` | [`DUST_EVENTMOTEDELETE`](#dust_eventmotedelete)                             |
|   `0x1c` | [`DUST_EVENTMOTELOST`](#dust_eventmotelost)                                 |
|   `0x1d` | [`DUST_EVENTMOTEOPERATIONAL`](#dust_eventmoteoperational)                   |
|   `0x1e` | [`DUST_EVENTMOTERESET`](#dust_eventmotereset)                               |
|   `0x1f` | [`DUST_EVENTPACKETSENT`](#dust_eventpacketsent)                             |
|   `0x20` | [`DUST_SNAPSHOT`](#dust_snapshot)                                           |
|   `0x21` | [`DUST_SNAPSHOT_2`](#dust_snapshot_2)                                       |
|   `0x22` | [`JUDD_T2D2R1N1`](#judd_t2d2r1n1)                                           |
|   `0x24` | [`MB7554_DTYPE_D2SD2N1NL1NG1`](#mb7554_dtype_d2sd2n1nl1ng1)                 |
|   `0x25` | [`SHT15_T4RH4N1`](#sht15_t4rh4n1)                                           |
|   `0x27` | [`DUST_OAP_TEMPSAMPLE`](#dust_oap_tempsample)                               |
|   `0x28` | [`SOLMANAGER_STATS`](#solmanager_stats)                                     |
|   `0x29` | [`SENS_MB7363_D2S2N1L1G1`](#sens_mb7363_d2s2n1l1g1)                         |
|   `0x30` | [`SENS_GS3_I1D4T4E4N1`](#sens_gs3_i1d4t4e4n1)                               |
|   `0x31` | [`SENS_SHT25_T2N1H2N1`](#sens_sht25_t2n1h2n1)                               |
|   `0x32` | [`SENS_NEOVBAT_V2N1`](#sens_neovbat_v2n1)                                   |
|   `0x33` | [`SENS_GS3_I1D4T4E4N1_0`](#sens_gs3_i1d4t4e4n1_0)                           |
|   `0x34` | [`SENS_GS3_I1D4T4E4N1_1`](#sens_gs3_i1d4t4e4n1_1)                           |
|   `0x35` | [`SENS_GS3_I1D4T4E4N1_2`](#sens_gs3_i1d4t4e4n1_2)                           |
|   `0x36` | [`SENS_LP02_R4N1`](#sens_lp02_r4n1)                                         |
|   `0x37` | [`SENS_ECTM`](#sens_ectm)                                                   |
|   `0x38` | [`SENS_MPS1`](#sens_mps1)                                                   |
|   `0x39` | [`ADXL362_FFT_Z`](#adxl362_fft_z)                                           |
|   `0x3a` | [`DUST_EVENTJOINFAILED`](#dust_eventjoinfailed)                             |
|   `0x3b` | [`SOLMANAGER_STATS_2`](#solmanager_stats_2)                                 |
|   `0x40` | [`TEMPRH_SHT31`](#temprh_sht31)                                             |
|   `0x41` | [`DUST_OAP_ANALOG`](#dust_oap_analog)                                       |
|   `0x42` | [`DUST_OAP_DIGITAL_IN`](#dust_oap_digital_in)                               |
|   `0x43` | [`TEMPRH_SHT3X`](#temprh_sht3x)                                             |
|   `0x44` | [`DUST_NOTIF_HREXTENDED`](#dust_notif_hrextended)                           |
|   `0x45` | [`SENS_MPS6_ID1P4T4N1`](#sens_mps6_id1p4t4n1)                               |
|   `0x46` | [`SENS_GS1_I1MV2`](#sens_gs1_i1mv2)                                         |
|   `0x47` | [`SENS_MICROWAVE_MOTION`](#sens_microwave_motion)                           |
|   `0x48` | [`SENS_INDUCTION_CURRENT_C_SOURCE`](#sens_induction_current_c_source)       |
|   `0x49` | [`SENS_INDUCTION_CURRENT_V_SOURCE`](#sens_induction_current_v_source)       |
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
| INT32U | INT32U | INT8U |    INT8U | INT32U |

#### TEMPRH_SENSERION_SHT25_RS232_RAW

|   temp |     rH |
|--------|--------|
| INT32U | INT32U |

#### TEMPRH_SENSERION_SHT25_RS232_STATS

|   temp |     rH | count | std_temp | std_rH |
|--------|--------|-------|----------|--------|
| INT32U | INT32U | INT8U |   INT32U | INT32U |

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

#### DUST_NOTIFDATA

| srcPort | dstPort |
|---------|---------|
|  INT16U |  INT16U |

#### DUST_NOTIF_HRDEVICE

| charge | queueOcc | temperature | batteryVoltage | numTxOk | numTxFail | numRxOk | numRxLost | numMacDropped | numTxBad | badLinkFrameId | badLinkSlot | badLinkOffset | numNetMicErr | numMacMicErr | numMacCrcErr |
|--------|----------|-------------|----------------|---------|-----------|---------|-----------|---------------|----------|----------------|-------------|---------------|--------------|--------------|--------------|
| INT32U |    INT8U |        INT8 |         INT16U |  INT16U |    INT16U |  INT16U |    INT16U |         INT8U |    INT8U |          INT8U |      INT32U |         INT8U |        INT8U |        INT8U |        INT8U |

#### DUST_EVENTCOMMANDFINISHED

| callbackId |    rc |
|------------|-------|
|     INT32U | INT8U |

#### DUST_EVENTPATHCREATE

| source |   dest | direction |
|--------|--------|-----------|
| INT64U | INT64U |     INT8U |

#### DUST_EVENTPATHDELETE

| source |   dest | direction |
|--------|--------|-----------|
| INT64U | INT64U |     INT8U |

#### DUST_EVENTPING

| callbackId | macAddress |  delay | voltage | temperature |
|------------|------------|--------|---------|-------------|
|     INT32U |     INT64U | INT32U |  INT16U |       INT8U |

#### DUST_EVENTNETWORKTIME

| uptime | utcTime |   asn | asnOffset |
|--------|---------|-------|-----------|
| INT32U |  INT64U | 5INT8 |      INT8 |

#### DUST_EVENTNETWORKRESET

|
|
|

#### DUST_EVENTMOTEJOIN

| macAddress |
|------------|
|     INT64U |

#### DUST_EVENTMOTECREATE

| macAddress | moteId |
|------------|--------|
|     INT64U | INT16U |

#### DUST_EVENTMOTEDELETE

| macAddress | moteId |
|------------|--------|
|     INT64U | INT16U |

#### DUST_EVENTMOTELOST

| macAddress |
|------------|
|     INT64U |

#### DUST_EVENTMOTEOPERATIONAL

| macAddress |
|------------|
|     INT64U |

#### DUST_EVENTMOTERESET

| macAddress |
|------------|
|     INT64U |

#### DUST_EVENTPACKETSENT

| callbackId |    rc |
|------------|-------|
|     INT32U | INT8U |

#### JUDD_T2D2R1N1

| temperature |  depth | numReadings | retries |
|-------------|--------|-------------|---------|
|       INT16 | INT16U |       INT8U |   INT8U |

#### MB7554_DTYPE_D2SD2N1NL1NG1

| mean_d2g |  stdev |  Nval |  Nltm |  NgtM |
|----------|--------|-------|-------|-------|
|   INT16U | INT16U | INT8U | INT8U | INT8U |

#### SHT15_T4RH4N1

| temperature |    rH | numReadings |
|-------------|-------|-------------|
|       INT32 | INT32 |       INT8U |

#### DUST_OAP_TEMPSAMPLE

| temperature |
|-------------|
|       INT16 |

#### SOLMANAGER_STATS

| sol_version | solmanager_version | sdk_version |
|-------------|--------------------|-------------|
|      INT32U |             INT32U |      INT32U |

#### SENS_MB7363_D2S2N1L1G1

| mean_d2g |  stdev |  Nval |  Nltm |  NgtM |
|----------|--------|-------|-------|-------|
|   INT16U | INT16U | INT8U | INT8U | INT8U |

#### SENS_GS3_I1D4T4E4N1

| sub_id | dielect |  temp | eleCond |  Nval |
|--------|---------|-------|---------|-------|
|  INT8U |   INT32 | INT32 |   INT32 | INT8U |

#### SENS_SHT25_T2N1H2N1

| temp_raw | t_Nval | rh_raw | rh_Nval |
|----------|--------|--------|---------|
|   INT16U |  INT8U | INT16U |   INT8U |

#### SENS_NEOVBAT_V2N1

| voltage |     N |
|---------|-------|
|   INT16 | INT8U |

#### SENS_GS3_I1D4T4E4N1_0

| dielect |  temp | eleCond |  Nval |
|---------|-------|---------|-------|
|   INT32 | INT32 |   INT32 | INT8U |

#### SENS_GS3_I1D4T4E4N1_1

| dielect |  temp | eleCond |  Nval |
|---------|-------|---------|-------|
|   INT32 | INT32 |   INT32 | INT8U |

#### SENS_GS3_I1D4T4E4N1_2

| dielect |  temp | eleCond |  Nval |
|---------|-------|---------|-------|
|   INT32 | INT32 |   INT32 | INT8U |

#### SENS_LP02_R4N1

| irradiance |     N |
|------------|-------|
|      INT32 | INT8U |

#### SENS_ECTM

| die_raw | EC_raw | temp_raw | depth |
|---------|--------|----------|-------|
|   INT32 |  INT32 |    INT32 | INT32 |

#### SENS_MPS1

| die_raw | depth |
|---------|-------|
|   INT32 | INT32 |

#### ADXL362_FFT_Z

| conf1 | conf2 |     f0 |     f1 |     f2 |     f3 |     f4 |     m0 |     m1 |     m2 |     m3 |     m4 |
|-------|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| INT8U | INT8U | INT16U | INT16U | INT16U | INT16U | INT16U | INT16U | INT16U | INT16U | INT16U | INT16U |

#### DUST_EVENTJOINFAILED

| macAddress | reason |
|------------|--------|
|     INT64U |  INT8U |

#### SOLMANAGER_STATS_2

| sol_version | solmanager_version | sdk_version | ram_usage | disk_usage |
|-------------|--------------------|-------------|-----------|------------|
|      INT32U |             INT32U |      INT32U |    INT32U |     INT32U |

#### TEMPRH_SHT31

| temp_raw | rh_raw |    id |
|----------|--------|-------|
|   INT16U | INT16U | INT8U |

#### TEMPRH_SHT3X

| temp_raw | t_Nval | rh_raw | rh_Nval |
|----------|--------|--------|---------|
|   INT16U |  INT8U | INT16U |   INT8U |

#### SENS_MPS6_ID1P4T4N1

|    id |   pot |  temp |  Nval |
|-------|-------|-------|-------|
| INT8U | INT32 | INT32 | INT8U |

#### SENS_GS1_I1MV2

|    id | NmVolts |
|-------|---------|
| INT8U |  INT16U |

#### DUST_OAP_ANALOG

| input | voltage |
|-------|---------|
| INT8U |   INT16 |

#### DUST_OAP_DIGITAL_IN

| input | state |
|-------|-------|
| INT8U | INT8U |

#### SENS_MICROWAVE_MOTION

| edge_count | sensor_id |
|------------|-----------|
|     INT16U |     INT8U |

#### SENS_INDUCTION_CURRENT_C_SOURCE

| tick_count | sensor_id |
|------------|-----------|
|     INT16U |     INT8U |

#### SENS_INDUCTION_CURRENT_V_SOURCE

| accu_sum | accu_sum_of_squares | sample_count | sensor_id |
|----------|---------------------|--------------|-----------|
|   INT32U |              INT32U |       INT16U |     INT8U |
