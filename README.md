This repo contains a set of libraries to manipulate sensor objects.

An sensor object contains the following _conceptual_ fields:
* `M`: MAC address of the device creating the object
* `T`: timestamp of when the object was created
* `t`: type of object, a number
* `V`: object value, a opaque string of bytes

It is a generalization of the well-known "Type-Length-Value" (TLV) format.

# Registry

## "type" registry

When a sensor is associated a well-known length, the `L` (length) field MAY be omitted from its binary representation.
When the well-known length is the table below is "None", the `L` (length) MUST be present in the object's binary representation.

| value    | well-known length | description |
|---------:|------------------:|-------------|
| `0x00`   |              N.A. | _reserved_  |
| `0xff`   |              N.A. | _reserved_  |
| `0xffff` |              N.A. | _reserved_  |

# Representations

This sections details how this object is represented.

## binary representation

This representation is used for:
* sending data in packets
* writing data to a file

Each object consists of the following fields:

```
| header | MAC | Timestamp | type | Length | Value |
```

Some rules:
* all multi-byte value are encoded "big endian" (a.k.a "network order")
* when chaining objects in a packet, a "more" header SHOULD be inserted for a more compact representation.
* when chaining objects in a binary file, each MUST be frames using HDLC.

### field format

#### "header" field format

The header always starts with a 2-bit `V` field (version).
Only value `b00` is defined in this document. Other values for the 2 first bits are reserved and may be defined in later revisions of this document.

```
 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+
| V |x x x x x x|
+-+-+-+-+-+-+-+-+
```

The `H` bit in position 2 identifies the type of header

```
 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+
| V |H| x x x x |
+-+-+-+-+-+-+-+-+
```

* `H`: header
    * `0`: "start" header
    * `1`: "more" header

##### "start" header

This header appears in front on each object, or in a front of a chain of objects.

```
 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+
|0 0|0|M|S|Y| L |
+-+-+-+-+-+-+-+-+
```

* `M`: MAC address encoding:
    * `0`: no MAC address present
    * `1`: 8-byte MAC address present
* `S`: timestamp encoding
    * `0`: timestamp is a 4-byte Linux epoch (1-second granularity)
    * `1`: timestamp is elided, and recovered from the timestamp field present in the SmartMesh IP header
* `Y`: type encoding
    * `0`: 1-byte type field
    * `1`: 2-byte type field
* `L`: length encoding
    * `b00`: use well-known value. No length field present
    * `b01`: 1-byte length field present
    * `b10`: 2-byte length field present
    * `b11`: elided. The length is recovered from the length of the packet or HDLC frame.

##### "more" header

```
 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+
|0 0|1|S|Y|L| N |
+-+-+-+-+-+-+-+-+
```

* `S`:
    * `0` no timestamp present in any of the sensor objects following
    * `1` timestamp present in each of the sensor objects following. Same format as in the "start" header.
* `Y`:
    * `0` no type field present in any of the sensor objects following
    * `1` type field present in each of the sensor objects following. Same format as in the "start" header.
* `L`: length field
    * `0` no length field present in any of the sensor objects following
    * `1` length  field present in each of the sensor objects following. Same format as in the "start" header.
* `N`: number of objects following
    * `b00`: 2 objects following
    * `b01`: 4 objects following
    * `b10`: 8 objects following
    * `b11`: 16 objects following

### example transmission use cases

Transmitting a single 2-byte temperature sensor reading, taken in the past:

* `[1B]` "start" header
   * `V`=`00` (version 0)
   * `H`=`0` ("start" header)
   * `M`=`0` (no MAC address)
   * `S`=`0` (epoch)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* `[0B]` MAC: _elided_
* `[4B]` Timestamp: `0x........`
* `[1B]` type=`b..` (temperature)
* `[0B]` length: _elided_
* `[2B]` value: `0x....`

Transmitting a single 2-byte temperature sensor reading, taken just now:

* `[1B]` "start" header
   * `V`=`00` (version 0)
   * `H`=`0` ("start" header)
   * `M`=`0` (no MAC address)
   * `S`=`1` (elided)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* sensor reading 1
   * `[0B]` MAC: _elided_
   * `[0B]` Timestamp: _elided_
   * `[1B]` type=`b..` (temperature)
   * `[0B]` length: _elided_
   * `[2B]` value: `0x....`

Transmitting 3 sensor readings from 3 different sensors with well-known length, taken at the same time in the past:

* `[1B]` "start" header
   * `V`=`00` (version 0)
   * `H`=`0` ("start" header)
   * `M`=`0` (no MAC address)
   * `S`=`0` (epoch)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* sensor reading 1
   * `[--]` MAC: _elided_
   * `[4B]` Timestamp: `0x........`
   * `[1B]` type=`b..` (temperature)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`
* `[1B]` "more" header
   * `S`=`0` (inherit)
   * `Y`=`1` (1-byte type)
   * `L`=`0` (inherit)
* sensor reading 2
   * `[--]` MAC: _elided_
   * `[--]` Timestamp: _elided_
   * `[1B]` type=`b..` (RH)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`
* sensor reading 3
   * `[--]` MAC: _elided_
   * `[--]` Timestamp: _elided_
   * `[1B]` type=`b..` (solar)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`

### rules for saving to a binary file

The assumption is that a binary file is stored on some hard/flash drive with orders of magnitude more space than a packet. The driving design choice are hence made to allow:
* simple parsing
* recoverable file in case parts of it get corrupted.

The following rules hence apply when saving to a binary file:
* sensor object chaining is NOT allowed
* each sensor object MUST be framed using HDLC framing ([RFC1662](https://tools.ietf.org/html/rfc1662))
* the length field MUST be elided, and the `L` bit in the start header set to `b11`

## JSON representation

TODO