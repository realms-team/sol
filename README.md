| Master branch  | Develop branch |
| -------------- | ------------- |
| [![Build Status](https://travis-ci.org/realms-team/sol.svg?branch=master)](https://travis-ci.org/realms-team/sol)  | [![Build Status](https://travis-ci.org/realms-team/sol.svg?branch=develop)](https://travis-ci.org/realms-team/sol)  |
| [![Code Health](https://landscape.io/github/realms-team/sol/master/landscape.svg?style=flat)](https://landscape.io/github/realms-team/sol/master)  | [![Code Health](https://landscape.io/github/realms-team/sol/develop/landscape.svg?style=flat)](https://landscape.io/github/realms-team/sol/develop)  |

This repo contains a set of libraries to manipulate sensor Objects.

An sensor Object contains the following _conceptual_ fields:
* `M`: MAC address of the device creating the Object
* `T`: timestamp of when the Object was created
* `t`: type of Object, a number
* `L`: the length of the value
* `V`: Object value, a opaque string of bytes

We refer to this format as the MTtlv format. It is a generalization of the well-known "Type-Length-Value" (TLV) format.

# Installation
Download source:
`git clone https://github.com/realms-team/sol.git`

# Code documentation
http://realms-sol.readthedocs.io

# Registry

## Objects' "types" registry

See [registry](registry.md).

# Representations

The SOL Objects are manipulated in groups.
Each group of Objects can be represented in [binary](#binary-representation), [JSON](#json-representation) or [HTTP](#http-representation) format.

## Binary representation

This representation is used for:
* sending data in packets
* writing data to a file

Each group of Objects consists of the following fields:

```
| SOL header | Objects list |
```

Some rules:
* all multi-byte value are encoded "big endian" (a.k.a "network order")
* when saving Objects in a binary file, each Object MUST be framed using HDLC.

#### SOL Header

```
 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+
| V |T|M|S|Y| L |
+-+-+-+-+-+-+-+-+
```
* `V`: Version of the Object:
    * Only value `b00` is defined in this document. Other values for the 2 first bits are reserved and may be defined in later revisions of this document.
* `T`: Type of MTtlv Object:
    * `0`: single-MTtlv Object
    * `1`: multi-MTtlv Object (MTNtlv) this implies the 1st byte next to timestamp is N: number of Objects
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

#### Object List

According to the header flags, the Object list structure can vary.

* If the T flag is `0` then the message will have the following structure:  
   ```|| SOL Header || MT | tlv |```
* If the T flag is `1` then the message will have the following structure:  
   ```|| SOL Header || MT | N | tlv | tlv | ... ```

#### Example transmission use cases

**Example 1**. transmitting a single 2-byte temperature sensor reading, taken in the past:

* `[1B]` SOL Header
   * `V`=`00` (version 0)
   * `T`=`0` (Type of MTtlv Object)
   * `M`=`0` (no MAC address)
   * `S`=`0` (epoch)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* `[--]` MAC: _elided_
* `[4B]` Timestamp: `0x........`
* `[1B]` type=`b..` (temperature)
* `[--]` length: _elided_
* `[2B]` value: `0x....`

Total 8 bytes.

**Example 2**. transmitting a single 2-byte temperature sensor reading, taken just now:

* `[1B]` SOL Header
   * `V`=`00` (version 0)
   * `T`=`0` (Type of MTtlv Object)
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

* `[1B]` SOL Header
   * `V`=`00` (version 0)
   * `T`=`1` (Type of MTtlv Object)
   * `M`=`0` (no MAC address)
   * `S`=`0` (epoch)
   * `Y`=`0` (1-byte type)
   * `L`=`b00` (well-known value, no length field)
* `[--]` MAC: _elided_
* `[4B]` Timestamp: `0x........`
* `[1B]` Number of Objects = 3
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


### Rules for saving to a binary file

The assumption is that a binary file is stored on some hard/flash drive with orders of magnitude more space than a packet. The driving design choice are hence made to allow:
* simple parsing
* recoverable file in case parts of it get corrupted.

The following rules hence apply when saving to a binary file:
* sensor Object chaining is NOT allowed (except on Neomote SD card level)
* each sensor Object MUST be framed using HDLC framing ([RFC1662](https://tools.ietf.org/html/rfc1662))
* the length field MUST be elided, and the `L` bit in the start header set to `b11`


## JSON representation

A [JSON](http://json.org/) representation is used:
 * when the Objects are stored in a database
 * when manipulating Objects

We use clean indentation for easier readability in these examples. An efficient implementation SHOULD represent the entire JSON string on a single line.

The following is the general format of a JSON representation of sensor Objects:

```
{
   "mac":       "00-17-0d-00-00-12-34-56",
   "timestamp": 12345678890,
   "type":      39,
   "value":     {
       'temperature': 0x0a33,
   },
}
```

* "mac"
    * represented exactly like in the example above, lowercase hex bytes (exactly 2 characters per byte), separated by `-`.
* "timestamp"
    * an integer representing the epoch
* "type"
    * an integer, per the registry above
* "value"
    * a dictionary of values


## HTTP representation

This representation is used for minimal communication overhead (when data transists).

```
{
   "v": 0,
   "o": [
       ew0KICAgIm1hYyI6ICAg,
       ICAgICIwMC0xNy0wZC0w,
       ...
       1NiIsDQogICAidGltZXw,
   ]
}
```

* `v`: the version of the representation. Only version `0` is defined in this specification. Other values SHOULD NOT be used. Future revisions of this document MIGHT define further versions.
* `o`: an array of representations. Each representation is a string representing the binary representation of one or more sensor Objects.
  * the string MUST be a [Base64](https://en.wikipedia.org/wiki/Base64) encoding of the binary representation of exactly one sensor Objects.

