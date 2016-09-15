#ifndef SOL_H
#define SOL_H

//=========================== defines =========================================

/// \brief The SOL default UDP port.
#define SOL_PORT 0xF0BA

#define SOL_TYPE_TEMPRH_SHT31                   = 0x40

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

void       sol_create_MTtlv();

#endif

