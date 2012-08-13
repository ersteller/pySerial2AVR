/*
 * remo.c
 *
 * Created: 28.06.2012 20:40:34
 *  Author: Jan
 */ 

#include "remo.h"


#define INSTRUCTION_LEN 32

uint8_t instrIn = 0;
uint8_t instrOut = 0;
char instruction[INSTRUCTION_LEN] = {0};

/* return newline on succes 
 or errorcode
 call appropriate function
 
 frame looks like "i 0x12Ab 0xFf\n"
 */
uint8_t instructionHandler(uint8_t c)
{
	instruction[instrIn] =  c;
	instrIn++;
	
	// backspace
	if ( c == 8 || c == 0x7f )
	{
		// clear backspace from buffer
		instrIn--;
		instruction[instrIn] = 0;
		if (instrIn) 
		{
			//clear last char from buffer if there is one
			instrIn--;
			instruction[instrIn] = 0;
		}
	}		
	
	if (instrIn >= INSTRUCTION_LEN)
	{
		// Todo: should throw error because clearing buffer for new instructiosn
		instrIn = 0;
		uart_puts_P(" instruction too long -> cleared\n");
		memset(instruction, 0, INSTRUCTION_LEN);
	}		
		
	if ((c == '\r') && (instrIn < 3))
	{
		// Todo: should throw error because clearing buffer for new instructions
		instrIn = 0;
		uart_puts_P(" instruction too short -> cleared\n");
		memset(instruction, 0, INSTRUCTION_LEN);
	}
			
	if ((c == '\r') && (instrIn >= 3))
	{
		// call instruction now
		char* pParamEnd = NULL;
		uint16_t addr = 0;
		uint8_t val = 0;
		uint8_t ret = 0;		
		char buff[16];
		
		switch(instruction[0])
		{
			case 's':
				addr = (uint16_t) strtoul(&instruction[1], &pParamEnd, 16);
				val = (uint8_t)  strtoul(++pParamEnd, NULL, 16);
				ret = setValAddr(addr, val);
				if (ret != 0)
				{
					memset(buff, 0, 16);
					memcpy(buff, " --> 0x",7);

					itoa((int)ret, buff + 7, 16);
					uart_puts(buff);
				}
			break;
			
			case 'g':
				memset(buff, 0, 16);
				memcpy(buff, " 0x",3);
				addr = (uint16_t) strtoul(&instruction[1], NULL, 16);
				itoa((int)getValAddr(addr), buff + 3, 16);
				uart_puts(buff);
			break;
			
			default:
				uart_puts_P("unsupported instruction: ");
				uart_puts(instruction);
				uart_puts_P(" -> cleared");
				
		}
		instrIn = 0;
		memset(instruction, 0, INSTRUCTION_LEN);
		uart_putc('\n');
	}
	/* send received character back */
    uart_putc( (unsigned char)c );
	return 0;	
}

//sets value at addres 
uint8_t setValAddr(uint16_t addr, uint8_t val){
	void* pvAddr = NULL;
	uint8_t* pbAddr = NULL;
	
	pvAddr = (void*)addr;
	pbAddr = (uint8_t*)pvAddr;
	*pbAddr = val;
	uint8_t ret = getValAddr(addr);
	if (val != ret)
		return ret;
	return 0;
}


// returns value at address
uint8_t getValAddr(uint16_t addr){
	void* pvAddr = NULL;
	uint8_t* pbAddr = NULL;

	pvAddr = (void*)addr;
	pbAddr = (uint8_t*)pvAddr;
	uint8_t val = *pbAddr;
	return val;
}
