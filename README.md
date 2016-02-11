[![Build Status](https://travis-ci.org/realms-team/sol.svg?branch=master)](https://travis-ci.org/realms-team/sol)
[![Code Health](https://landscape.io/github/realms-team/basestation-fw/master/landscape.svg?style=flat)](https://landscape.io/github/realms-team/basestation-fw/master)

This repo contains a set of libraries to manipulate sensor objects.

An sensor object contains the following _conceptual_ fields:
* `M`: MAC address of the device creating the object
* `T`: timestamp of when the object was created
* `t`: type of object, a number
* `V`: object value, a opaque string of bytes

It is a generalization of the well-known "Type-Length-Value" (TLV) format.

# Registry

## "type" registry

See [registry](registry.md).

# Representations

This sections details how this object is represented.

## binary representation

This representation is used for:
* sending data in packets
* writing data to a file

Each object consists of the following fields:

```
| header | mac | timestamp | type | length | Value |
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
|0 0|T|M|S|Y| L |
+-+-+-+-+-+-+-+-+
```
* `T`: Type of MTtlv object:
    * `0`: single-MTtlv object
    * `1`: multi-MTtlv object (MTNtlv) this implies the 1st byte next to timestamp is N: number of objects
* `M`: MAC address encoding:
    * `0`: no MAC address present
    * `1`: 8-byte MAC address present
* `S`: timestamp encoding
    * `0`: timestamp is a 4-byte Linux epoch in UTC (1-second granularity)
    * `1`: timestamp is elided, and recovered from the timestamp field present in the SmartMesh IP header
* `Y`: type encoding
    * `0`: 1-byte type field
    * `1`: 2-byte type field
* `L`: length encoding
    * `b00`: use well-known value. No length field present
    * `b01`: 1-byte length field present
    * `b10`: 2-byte length field present
    * `b11`: elided. The length is recovered from the length of the packet or HDLC frame.


### example transmission use cases

**Example 1**. transmitting a single 2-byte temperature sensor reading, taken in the past:

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


**Example 2**. transmitting a single 2-byte temperature sensor reading, taken just now:

* `[1B]` "start" header
   * `V`=`00` (version 0)
   * `H`=`0` ("start" header)
   * `M`=`0` (no MAC address)
   * `S`=`1` (elided)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* `[3B]` sensor reading 1
   * `[--]` MAC: _elided_
   * `[--]` Timestamp: _elided_
   * `[1B]` type=`b..` (temperature)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`

Total: 4 bytes.


**Example 3**. Transmitting 3 sensor readings from 3 different sensors with well-known length, taken at the same time in the past:

* `[1B]` "start" header
   * `V`=`00` (version 0)
   * `H`=`1` ("start" header)
   * `M`=`0` (no MAC address)
   * `S`=`0` (epoch)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* `[--]` MAC: _elided_
* `[4B]` Timestamp: `0x........`
* `[1B]` Number of objects = 3
* `[3B]` sensor reading 1
   * `[--]` MAC: _elided_
   * `[--]` Timestamp: _elided_
   * `[1B]` type=`b..` (temperature)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`
* `[3B]` sensor reading 2
   * `[--]` MAC: _elided_
   * `[--]` Timestamp: _elided_
   * `[1B]` type=`b..` (RH)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`
* `[3B]` sensor reading 3
   * `[--]` MAC: _elided_
   * `[--]` Timestamp: _elided_
   * `[1B]` type=`b..` (solar)
   * `[--]` length: _elided_
   * `[2B]` value: `0x....`

Total: 15 bytes.


### rules for saving to a binary file

The assumption is that a binary file is stored on some hard/flash drive with orders of magnitude more space than a packet. The driving design choice are hence made to allow:
* simple parsing
* recoverable file in case parts of it get corrupted.

The following rules hence apply when saving to a binary file:
* sensor object chaining is NOT allowed (except on Neomote SD card level)
* each sensor object MUST be framed using HDLC framing ([RFC1662](https://tools.ietf.org/html/rfc1662))
* the length field MUST be elided, and the `L` bit in the start header set to `b11`


## JSON representation

A [JSON](http://json.org/) representation is used to communicate sensors objects across a network, typically using HTTP.

We use clean indentation for easier readability in these examples. An efficient implementation SHOULD represent the entire JSON string on a single line.

The following is the general format of a JSON representation of sensor objects:

```
{
   "v": 0,
   "o": [
       <minimal or verbose representation>,
       <minimal or verbose representation>,
       ...
       <minimal or verbose representation>,
   ]
}
```

* `v`: the version of the representation. Only version `0` is defined in this specification. Other values SHOULD NOT be used. Future revisions of this document MIGHT define further versions.
* `o`: an array of representations. Each representation can be either a JSON string (for the "minimal" representation) or a JSON object (for the "verbose" representation). A single JSON string CAN contain both "minimal" and "verbose" representations.

This specification defines two formats:
* a "compact" representation for minimal communication overhead.
* a "verbose" representation for readability.

#### "minimal" representation

```
"TWFuIGlzIGRpc3Rpbmd1aXNoZWQs"
```

* the minimal representation is a string representing the binary representation of exactly one sensor objects.
* the string MUST be a [Base64](https://en.wikipedia.org/wiki/Base64) encoding of the binary representation of exactly one sensor objects.

#### "verbose" representation

```
{
   "mac":       "00-17-0d-00-00-12-34-56",
   "timestamp": 12345678890,
   "type":      12,
   "value":     "TWFuIGlzIGRpc3Rpbmd1aXNoZWQs",
}
```

* "mac"
    * represented exactly like in the example above, lowercase hex bytes (exactly 2 characters per byte), separated by `-`.
* "timestamp"
    * an integer representing the epoch
* "type"
    * an integer, per the registry above
* "value"
    * a [Base64](https://en.wikipedia.org/wiki/Base64) encoding of the binary value
