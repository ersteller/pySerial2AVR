/*
 * IncFile1.h
 *
 * Created: 28.06.2012 20:40:47
 *  Author: Jan
 */ 


#ifndef REMO_H_
#define REMO_H_

#include <stdlib.h>
#include <avr/io.h>
#include <string.h>
#include "uart.h"
#include <avr/pgmspace.h>

uint8_t instructionHandler(uint8_t c);

uint8_t setValAddr(uint16_t addr, uint8_t val);
uint8_t getValAddr(uint16_t addr);






#endif /* REMO_H_ */