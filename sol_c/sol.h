#ifndef SOL_H
#define SOL_H

//=========================== includes ========================================

#include <stdint.h>

//=========================== defines =========================================

/// \brief The SOL default UDP port.
const uint16_t SOL_PORT = 0xF0BA;

const uint8_t SOL_TYPE_TEMPRH_SHT31 = 0x40;

//=========================== function pointers/structs =======================

/// \brief The SOL Object structures

typedef struct __attribute__((__packed__)) {
    uint8_t     mac[8];         // M
    uint8_t     timestamp[8];   // T
    uint8_t     type;           // t
    uint8_t     lenght;         // l
    uint8_t     value;          // v
} sol_MTtlv_t;

typedef struct __attribute__((__packed__)) {
    uint8_t     header;
    sol_MTtlv_t object;
} sol_single_MTtlv;

typedef struct __attribute__((__packed__)) {
    uint8_t     header;
    uint8_t     object_number;
    sol_MTtlv_t object;
} sol_multi_MTtlv;

//=========================== prototypes ======================================

void create_object(uint8_t type, uint8_t length, uint8_t value, sol_MTtlv_t* sol_obj);

#endif

