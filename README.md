# Sensor Object Library

This repo contains a set of libraries to manipulate sensor objects:

An sensor object contains the following _conceptual_ fields:
* `M`: MAC address of the device creating the object
* `T`: timestamp of when the object was create
* `t`: type of object, a number
* `V`: object value, a opaque string of bytes

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

### example transmission use cases

Transmitting a single 2-byte temperature sensor reading:

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

Transmitting 3 sensor readings from 3 different sensors with well-known length, taken at the same time:

TODO

### rules for saving to a binary file

The following rules apply when saving to a binary file:
* sensor object chaining is NOT allowed
* each sensor object MUST be framed using HDLC framing ([RFC1662](https://tools.ietf.org/html/rfc1662))
* the length field MUST be elided.

## JSON representation

TODO