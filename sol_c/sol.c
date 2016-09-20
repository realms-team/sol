#include "sol.h"
#include <stdio.h>
#include <string.h>

//=========================== defines =========================================

const uint16_t SOL_PORT = 0xF0BA;

const uint8_t SOL_TYPE_TEMPRH_SHT31 = 0x40;
const uint8_t LENGTH_SOL_TYPE_TEMPRH_SHT31 = 5;

//=========================== public ==========================================


/**
\brief TODO

\pre TODO

\param[in] TODO

\return TODO
*/
void create_object(uint8_t type, uint8_t length, uint8_t* value, sol_MTtlv_t* sol_obj)
{
   memset(&sol_obj->mac,0,8);
   memset(&sol_obj->timestamp,0,8);
   sol_obj->type = type;
   sol_obj->length = length;
   memcpy(&sol_obj->value,value,length);
}

//brief TODO
uint8_t create_SOL_message(sol_MTtlv_t* obj_list, uint8_t N, uint8_t* txBuffer){
   // Sol-formatted packet
   // Sol header:
   // v:00b version 00
   // T:0 single-MTtlv object. We are sending temp+humidty from a well known format
   // M:0 we don`t add the MAC address
   // S:1 timestamp is taken from arrival time
   // Y:0 one-byte type field
   // L:00b No length field present

   // We use the TEMPRH_SHT31 (0x40)

   // Build the packet
   // V  T M S Y L
   // 00 1 0 1 0 00 -> 0x28
  
   txBuffer[0]= 0x28;           // header
   txBuffer[1]= N;              // four objects of two elements each
   
   uint8_t pos = 2;
   for(uint8_t i=0; i<N; i++){
      txBuffer[pos++]= SOL_TYPE_TEMPRH_SHT31;           // TEMPRH_SHT31
      txBuffer[pos++]= obj_list[i].value[0];              // Temperature high
      txBuffer[pos++]= obj_list[i].value[1];             // Temperature low
      txBuffer[pos++]= obj_list[i].value[2];               // Humidity high
      txBuffer[pos++]= obj_list[i].value[3];               // Hunidity low
      txBuffer[pos++]= obj_list[i].value[4];                       // ID
   }
   return pos;
}