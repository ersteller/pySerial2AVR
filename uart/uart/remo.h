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
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

volatile uint8_t fOverflow;

typedef struct LEVELS_Ttag{
	uint8_t		fAH;
	uint8_t		fAL;
	uint8_t		fBH;
	uint8_t		fBL;
	uint8_t		fCH;
	uint8_t		fCL;
}LEVELS_T;

uint8_t instructionHandler(uint8_t c);
uint8_t HandlerCommand(uint8_t c);
uint8_t HandlerBinary(uint8_t c);
void setHandler(uint8_t (*pfnH)(uint8_t));

uint8_t setValAddr(uint16_t addr, uint8_t val);
uint32_t getValAddr(uint16_t addr, uint8_t len);
void* getMalloc(uint16_t len);
void setFree(void* pvMem);
void* setPWMBuffer(char* pbInstruction);

void PWMHandler();
void lookupPWM();
void setPinLevles(volatile uint8_t ubPortLevel);
void setOutputPinsAddr(char* szParam);
void setAmplidudeAndSpeed(char* szParam);
void setPhaseShift(char* szParam);

#endif /* REMO_H_ */