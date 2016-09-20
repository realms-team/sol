#ifndef SOL_H
#define SOL_H

//=========================== includes ========================================

#include <stdint.h>

//=========================== defines =========================================

#define OBJ_MAX_LEN 50

//=========================== variables =======================================

/// \brief The SOL default UDP port.
extern const uint16_t SOL_PORT;

extern const uint8_t SOL_TYPE_TEMPRH_SHT31;
extern const uint8_t LENGTH_SOL_TYPE_TEMPRH_SHT31;

//=========================== function pointers/structs =======================

/// \brief The SOL Object structures

typedef struct __attribute__((__packed__)) {
   uint8_t     mac[8];                  // M
   uint8_t     timestamp[8];            // T
   uint8_t     type;                    // t
   uint8_t     length;                  // l
   uint8_t     value[OBJ_MAX_LEN];      // v
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

//=========================== SOL Object structures ===========================
typedef struct __attribute__((__packed__)) {
   uint16_t    temp;
   uint16_t    rh;
   uint8_t     id;
}sol_SHT31_t;

//=========================== prototypes ======================================

void create_object(uint8_t type, uint8_t length, uint8_t* value, sol_MTtlv_t* sol_obj);
uint8_t create_SOL_message(sol_MTtlv_t* obj_list, uint8_t N, uint8_t* txBuffer);

#endif

