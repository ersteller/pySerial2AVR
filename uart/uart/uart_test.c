/*
 * uart.c
 *
 * Created: 17.06.2012 23:51:15
 *  Author: Jan
 */ 
/*************************************************************************
Title:    example program for the Interrupt controlled UART library
Author:   Peter Fleury <pfleury@gmx.ch>   http://jump.to/fleury
File:     $Id: test_uart.c,v 1.4 2005/07/10 11:46:30 Peter Exp $
Software: AVR-GCC 3.3
Hardware: any AVR with built-in UART, tested on AT90S8515 at 4 Mhz

DESCRIPTION:
          This example shows how to use the UART library uart.c

*************************************************************************/


#include <stdlib.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/signal.h>
#include <avr/pgmspace.h>

#include "uart.h"
//#include "seriellout.h"


/* define CPU frequency in Mhz here if not defined in Makefile */

#define F_CPU 8000000UL

#ifndef F_CPU
#define F_CPU 8000000UL
#endif


/* 9600 baud */
#define UART_BAUD_RATE      9600      

/*
int main (void){
	init_usart();

	//PORTF=0<<4; 	//1 bedeutet pullup an f�r adc
	//DDRE |= (1<<3);		//wegen uart
  sei();  

	while(1)
	{ 		
		outc(12);
	  for (uint8_t i=0;i<=15;i++)
		{
			 outs("adc ");outu(i);outs("   ");
		}

    asm("sleep");
	}
}

*/


int main(void)
{
	
    unsigned int c;
    char buffer[7];
    int  num=134;
	char instruction[8] = {0};
	uint8_t cnt = 0;	
			
	DDRB = 0xff;
	PORTB = 0xfe;

    /*
     *  Initialize UART library, pass baudrate and AVR cpu clock
     *  with the macro 
     *  UART_BAUD_SELECT() (normal speed mode )
     *  or 
     *  UART_BAUD_SELECT_DOUBLE_SPEED() ( double speed mode)
     */
    uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); 
     
    /*
     * now enable interrupt, since UART library is interrupt controlled
     */
    sei();
		
    /*
     *  Transmit string to UART
     *  The string is buffered by the uart library in a circular buffer
     *  and one character at a time is transmitted to the UART using interrupts.
     *  uart_puts() blocks if it can not write the whole string to the circular 
     *  buffer
     */
    uart_puts("Atmega2560 initialized\n");
    
    /*
     * Transmit string from program memory to UART
     */
    //uart_puts_P("DEFString stored in FLASH\n");
    
        
    /* 
     * Use standard avr-libc functions to convert numbers into string
     * before transmitting via UART
     */     
    //itoa( num, buffer, 10);   // convert interger into string (decimal format)         
    //uart_puts(buffer);        // and transmit string to UART

    
    /*
     * Transmit single character to UART
     */
    uart_putc('\r');
    
    for(;;)
    {
        /*
         * Get received character from ringbuffer
         * uart_getc() returns in the lower byte the received character and 
         * in the higher byte (bitmask) the last receive error
         * UART_NO_DATA is returned when no data is available.
         *
         */
		
		/*
		if (cnt > 100)
		{	
			cnt = 0;
			PORTB = PORTB ^ 1;
		}        
		cnt++;*/
		
		c = uart_getc();
        if ( c & UART_NO_DATA )
        {
            /* 
             * no data available from UART 
             */
        }
        else
        {
            /*
             * new data available from UART
             * check for Frame or Overrun error
             */
            if ( c & UART_FRAME_ERROR )
            {
                /* Framing Error detected, i.e no stop bit detected */
                uart_puts_P("UART Frame Error: ");
            }
            if ( c & UART_OVERRUN_ERROR )
            {
                /* 
                 * Overrun, a character already present in the UART UDR register was 
                 * not read by the interrupt handler before the next character arrived,
                 * one or more received characters have been dropped
                 */
                uart_puts_P("UART Overrun Error: ");
            }
            if ( c & UART_BUFFER_OVERFLOW )
            {
                /* 
                 * We are not reading the receive buffer fast enough,
                 * one or more received character have been dropped 
                 */
                uart_puts_P("Buffer overflow error: ");
            }

			
			/* 
			 * Instruction handler sums up characters for an instruction  
			 * frame and calls the appropriate function if the frame was  
			 * received successfully, or returns error code
			 */
			instructionHandler( (unsigned char)c );
			
			
			
			
			
			
        }
    }
    
}
