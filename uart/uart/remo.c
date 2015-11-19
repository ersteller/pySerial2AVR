/*
 * remo.c
 *
 * Created: 28.06.2012 20:40:34
 *  Author: Jan
 */ 

#include "remo.h"
#include <math.h>


#define INSTRUCTION_LEN 255

uint8_t instrIn = 0;
uint8_t instrOut = 0;
char instruction[INSTRUCTION_LEN] = {0};
	
uint8_t (*pfnCurrHandler)(uint8_t) = &HandlerCommand;
uint16_t guiPending = 0;
void* gpvMem = NULL; // binary mode working pointer

int16_t asSin[] = {
	  0, 2, 4, 7, 9, 11, 13, 15, 18, 20, 22, 24, 26, 29, 31, 33, 35, 37, 39, 41, 43, 46, 48, 50, 52, 54, 56, 58, 60, 
	  62, 63, 65, 67, 69, 71, 73, 75, 76, 78, 80, 82, 83, 85, 87, 88, 90, 91, 93, 94, 96, 97, 99, 100, 101, 103, 104,
	  105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 119, 120, 121, 121, 122, 123, 123, 124, 
	  124, 125, 125, 125, 126, 126, 126, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 126, 126, 126, 125, 
	  125, 125, 124, 124, 123, 123, 122, 121, 121, 120, 119, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 
	  108, 107, 105, 104, 103, 101, 100, 99, 97, 96, 94, 93, 91, 90, 88, 87, 85, 83, 82, 80, 78, 76, 75, 73, 71, 69, 
	  67, 65, 63, 62, 60, 58, 56, 54, 52, 50, 48, 46, 43, 41, 39, 37, 35, 33, 31, 29, 26, 24, 22, 20, 18, 15, 13, 11, 
	  9, 7, 4, 2, 0, -2, -4, -7, -9, -11, -13, -15, -18, -20, -22, -24, -26, -29, -31, -33, -35, -37, -39, -41, -43, 
	  -46, -48, -50, -52, -54, -56, -58, -60, -62, -64, -65, -67, -69, -71, -73, -75, -76, -78, -80, -82, -83, -85, 
	  -87, -88, -90, -91, -93, -94, -96, -97, -99, -100, -101, -103, -104, -105, -107, -108, -109, -110, -111, -112, 
	  -113, -114, -115, -116, -117, -118, -119, -119, -120, -121, -121, -122, -123, -123, -124, -124, -125, -125, -125,
	  -126, -126, -126, -127, -127, -127, -127, -127, -127, -127, -127, -127, -127, -127, -126, -126, -126, -125, -125, 
	  -125, -124, -124, -123, -123, -122, -121, -121, -120, -119, -119, -118, -117, -116, -115, -114, -113, -112, -111,
	  -110, -109, -108, -107, -105, -104, -103, -101, -100, -99, -97, -96, -94, -93, -91, -90, -88, -87, -85, -83, -82,
	  -80, -78, -76, -75, -73, -71, -69, -67, -65, -64, -62, -60, -58, -56, -54, -52, -50, -48, -46, -43, -41, -39,
	  -37, -35, -33, -31, -29, -26, -24, -22, -20, -18, -15, -13, -11, -9, -7, -4, -2

	/*0, 2, 4, 7, 9, 11, 13, 16, 18, 20, 22, 24, 26, 29, 31, 33, 35, 37, 39, 41, 44, 46, 48, 50, 52, 54, 56, 58, 60, 
	62, 64, 66, 67, 69, 71, 73, 75, 77, 78, 80, 82, 84, 85, 87, 88, 90, 92, 93, 95, 96, 97, 99, 100, 102, 103, 104, 
	105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 119, 120, 121, 122, 122, 123, 123, 124, 
	124, 125, 125, 126, 126, 126, 126, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 126, 126, 126, 126, 125, 
	125, 125, 124, 124, 123, 123, 122, 121, 121, 120, 119, 118, 117, 117, 116, 115, 114, 113, 112, 111, 110, 108, 
	107, 106, 105, 104, 102, 101, 100, 98, 97, 95, 94, 92, 91, 89, 88, 86, 84, 83, 81, 79, 77, 76, 74, 72, 70, 68, 
	67, 65, 63, 61, 59, 57, 55, 53, 51, 49, 47, 45, 43, 40, 38, 36, 34, 32, 30, 28, 25, 23, 21, 19, 17, 14, 12, 10, 
	8, 6, 3, 1, -1, -3, -6, -8, -10, -12, -14, -17, -19, -21, -23, -25, -28, -30, -32, -34, -36, -38, -40, -43, -45, 
	-47, -49, -51, -53, -55, -57, -59, -61, -63, -65, -67, -68, -70, -72, -74, -76, -77, -79, -81, -83, -84, -86,
	-88, -89, -91, -92, -94, -95, -97, -98, -100, -101, -102, -104, -105, -106, -107, -108, -110, -111, -112, -113, 
	-114, -115, -116, -117, -117, -118, -119, -120, -121, -121, -122, -123, -123, -124, -124, -125, -125, -125, 
	-126, -126, -126, -126, -127, -127, -127, -127, -127, -127, -127, -127, -127, -127, -126, -126, -126, -126, 
	-125, -125, -124, -124, -123, -123, -122, -122, -121, -120, -119, -119, -118, -117, -116, -115, -114, -113,
	-112, -111, -110, -109, -108, -107, -105, -104, -103, -102, -100, -99, -97, -96, -95, -93, -92, -90, -88, -87, 
	-85, -84, -82, -80, -78, -77, -75, -73, -71, -69, -67, -66, -64, -62, -60, -58, -56, -54, -52, -50, -48, -46, 
	-44, -41, -39, -37, -35, -33, -31, -29, -26, -24, -22, -20, -18, -16, -13, -11, -9, -7, -4, -2*/ // only 359deg
	};
				  
volatile struct  {
	void*		pvBufferA;
	uint16_t	lenA;
	void*		pvReadA;
	void*		pvReadB;
	void*		pvReadC;
	int16_t		A;
	int16_t		B;
	int16_t		C;
	uint16_t    OCRA;
	uint16_t    OCRB;
	uint16_t    OCRC;
	uint16_t	phaseaA;
	uint16_t	phaseaB;
	uint16_t	phaseaC;
	LEVELS_T    levels[3];  // pinlevels for each interrupt 0 = overflow 1,2,3 = ocrA,B,C
	uint8_t     aubPortLevels[3];
	uint8_t		ubAmpl;
	uint8_t     ubSpeed;
	uint16_t	usPos;
	}pwm_buffer;//, tmp_pwm_buffer, *ptpwm_buffer, *pttmp_pwm_buffer;
	
volatile uint8_t gaubPortLevels[3] = {0}; // this saves the only the necessary data for one duty cycle
	
struct PWM_OUTPINS{
	void*		pvPORT;
	uint8_t		ubAHPin;
	uint8_t		ubALPin;
	uint8_t		ubBHPin;
	uint8_t		ubBLPin;
	uint8_t		ubCHPin;
	uint8_t		ubCLPin;
	uint8_t     ubMsk;
	}pwm_outpins;

/*
 * function handles regular commands 
 * return newline on succes 
 * or errorcode
 * call appropriate function
 * frame looks like "i 0x12Ab 0xFf\n"
 */
uint8_t HandlerCommand(uint8_t c)
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
		uint16_t ulAlocLen = 0;
		uint8_t val = 0;
		uint8_t ret = 0;	
		uint8_t len = 0;	
		char buff[16];
		
		switch(instruction[0])
		{
			/* set value */
			case 's':
				addr = (uint16_t) strtoul(&instruction[1], &pParamEnd, 16);
				val = (uint8_t)  strtoul(++pParamEnd, NULL, 16);
				ret = setValAddr(addr, val);
				if (ret != 0)
				{
					memset(buff, 0, 16);
					memcpy(buff, " 0x",7);
					itoa((int)ret, buff + 7, 16);
					uart_puts(buff);
				}
			break;
			
			/* get Value */  
			case 'g':
				memset(buff, 0, 16);
				memcpy(buff, " 0x",3);
				addr = (uint16_t) strtoul(&instruction[1], &pParamEnd, 16);
				len = (uint8_t) strtoul(++pParamEnd, NULL, 16);			
				if (len == 0) len = 1;
				utoa((unsigned int)getValAddr(addr,len), buff + 3, 16);	
				uart_puts(buff);
			break;
			
			/* allocate memory */ 
			case 'm':
				ulAlocLen = (uint16_t) strtoul(&instruction[1], &pParamEnd, 16);
				addr = (uint16_t)getMalloc(ulAlocLen);
				memset(buff, 0, 16);
				memcpy(buff, " 0x",3);
				itoa((int)addr, buff + 3, 16);
				uart_puts(buff);
			break;
			
			/* free memory */
			case 'f':
				addr = (uint16_t) strtoul(&instruction[1], &pParamEnd, 16);
				setFree((void*)addr);
			break;
			
			/* write binary stream of len */
			case 'b':
				/* binary data is received without response, so we need to switch handling mechanism */
				gpvMem = (void*)(uint16_t)strtoul(&instruction[1], &pParamEnd, 16);
				guiPending = (uint16_t)strtoul(++pParamEnd, NULL, 16);
				setHandler(&HandlerBinary);
				instrIn = 0;
				memset(instruction, 0, INSTRUCTION_LEN);
				//uart_putc( (unsigned char)c ); // would destroys return string
				return 0;
			break;
			
			case 'a':
				addr = (uint16_t)setPWMBuffer(&instruction[1]);
				memset(buff, 0, 16);
				memcpy(buff, " 0x",3);
				itoa((int)addr, buff + 3, 16);
				uart_puts(buff);
			break;
			
			case 'p':
				setPhaseShift(&instruction[1]);
				memset(buff, 0, 16);
				//memcpy(buff, " 0x",3);
				//itoa((int)addr, buff + 3, 16);
				//uart_puts(buff);
			break;
			
			case 'o':
				setOutputPinsAddr(&instruction[1]);
				memset(buff, 0, 16);
				//memcpy(buff, " 0x",3);
				//itoa((int)addr, buff + 3, 16);
				//uart_puts(buff);
			break;
			
			case 'A':
				setAmplidudeAndSpeed(&instruction[1]);
				memset(buff, 0, 16);
				//memcpy(buff, " 0x",3);
				//itoa((int)addr, buff + 3, 16);
				//uart_puts(buff);
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

uint8_t instructionHandler(uint8_t c){
	// wrapper for handlers
	return pfnCurrHandler(c);
	}

/* sets value at address */
uint8_t setValAddr(uint16_t addr, uint8_t val){
	void* pvAddr = NULL;
	uint8_t* pbAddr = NULL;
	
	pvAddr = (void*)addr;
	pbAddr = (uint8_t*)pvAddr;
	*pbAddr = val;
	uint8_t ret = (uint8_t)getValAddr(addr,1);
	if (val != ret)
		return ret;
	return 0;
}


// returns value at address
uint32_t getValAddr(uint16_t addr,uint8_t len){
	void* pvAddr = NULL;
	uint32_t val = 0;
	pvAddr = (void*)addr;
	uint8_t sregtemp = SREG;
	//cli();	
	memcpy(&val, pvAddr, len);
	//if (sregtemp & 1 << SREG_I)
		//sei();
	return val;
}

/* get pointer to allocated space */
void* getMalloc(uint16_t len){
	void* pvRet = NULL; 
	pvRet = malloc(len);
	return pvRet;
}

/* free space */
void setFree(void* pvMem){
	free(pvMem);
}

/* binary mode handler */
uint8_t HandlerBinary(uint8_t c){
	if (guiPending > 0)
	{
		if (gpvMem != NULL){
			// save char in location 
			memcpy(gpvMem, &c, 1);
			gpvMem++;
		}			
		// reduce pending
		guiPending--;
		// if zero pending reset current handler to HndlerCommand
		if (guiPending == 0)
		{
			char buff[16] = {0};
			setHandler(&HandlerCommand);	
			//memset(buff, 0, 16);
			memcpy(buff, " 0x",3);
			itoa((int)gpvMem, buff + 3, 16);
			uart_puts(buff);
			uart_puts("\n\r");	
		}
	}
	else 
	{// something is wrong: zero pending but still in binary mode
		// set handler to HandlerCommand 
		setHandler(&HandlerCommand);
		// call handler for this wrong call
		return HandlerCommand(c);
	}
	return 0;
}
	
/* registrar */
void setHandler(uint8_t (*pfnH)(uint8_t)){
	// set handler atomically 
	cli();
	pfnCurrHandler = pfnH;
	sei();
}

void setPhaseShift(char* szParam)
{
	uint16_t usPhaseA = 0;
	uint16_t usPhaseB = 0;
	uint16_t usPhaseC = 0;
	
	char* pbParamEnd = NULL;
	usPhaseA = (uint16_t) strtoul(szParam, &pbParamEnd, 16);
	usPhaseB = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	usPhaseC = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	
	pwm_buffer.phaseaA = usPhaseA;
	pwm_buffer.phaseaB = usPhaseB;
	pwm_buffer.phaseaC = usPhaseC;
	
	pwm_buffer.pvReadA = (uint8_t*)pwm_buffer.pvBufferA + usPhaseA * 2; // we have 16 bit so we need to increment times 2  
	pwm_buffer.pvReadB = (uint8_t*)pwm_buffer.pvBufferA + usPhaseB * 2;
	pwm_buffer.pvReadC = (uint8_t*)pwm_buffer.pvBufferA + usPhaseC * 2;
}

void setAmplidudeAndSpeed(char* szParam)
{
	char* pbParamEnd = NULL;
	pwm_buffer.ubAmpl  = (uint8_t)strtoul(szParam, &pbParamEnd, 16);
	pwm_buffer.ubSpeed = (uint8_t)strtoul(pbParamEnd, &pbParamEnd, 16);
}

void* setPWMBuffer(char* szParam)
{
	
	void* pvBuffA = NULL;
	uint16_t lenA = 0;
	char* pbParamEnd = NULL;	
	
	if(strlen(szParam) >  4)
	{
		pvBuffA =	(void*)(uint16_t)strtoul(szParam, &pbParamEnd, 16);
		lenA =		(uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	}
	else 
	{
		pvBuffA	= asSin;
		lenA = sizeof(asSin);
	}
	pwm_buffer.pvBufferA = pvBuffA;
	pwm_buffer.lenA = lenA; 
	pwm_buffer.pvReadA = pvBuffA;
	pwm_buffer.pvReadB = pvBuffA;
	pwm_buffer.pvReadC = pvBuffA;
	return &pwm_buffer.pvReadA;
}

void PWMHandler()
{
	if (fOverflow)
	{
		lookupPWM();	
	}		
		
}	


void lookupPWM()
{
	PORTB |= 1<<1; // lut lamp on
	fOverflow = 0;
	  
	pwm_buffer.A = (*(int16_t*)pwm_buffer.pvReadA);
	pwm_buffer.B = (*(int16_t*)pwm_buffer.pvReadB);
	pwm_buffer.C = (*(int16_t*)pwm_buffer.pvReadC);
	
	if(pwm_buffer.ubAmpl != 0)
	{
		pwm_buffer.A *= pwm_buffer.ubAmpl;
		pwm_buffer.B *= pwm_buffer.ubAmpl;
		pwm_buffer.C *= pwm_buffer.ubAmpl;
	}
	
	// put val from addr in ocrx
	/* pwm is split in two on cycles 
	first:  overflow: setting A and opposite pin
	second: ocrA:     disable first pin of double on and enable second
	third:  ocrB:     disable all
	*/
	if(signbit(pwm_buffer.A) == signbit(pwm_buffer.B))
	{
		pwm_buffer.OCRA = abs(pwm_buffer.A);
		pwm_buffer.OCRB = abs(pwm_buffer.A) + abs(pwm_buffer.B);
	}
	else if(signbit(pwm_buffer.B) == signbit(pwm_buffer.C))
	{
		pwm_buffer.OCRA = abs(pwm_buffer.B);
		pwm_buffer.OCRB = abs(pwm_buffer.B) + abs(pwm_buffer.C);
	}
	else if(signbit(pwm_buffer.A) == signbit(pwm_buffer.C))
	{
		pwm_buffer.OCRA = abs(pwm_buffer.A);
		pwm_buffer.OCRB = abs(pwm_buffer.A) + abs(pwm_buffer.C);
	}
	else		
		PORTB |= 1<<7; // error lamp on
	
	// calc pins level for bottom	ocr A B C 
	//[0 1 2 3 ]			
	if(pwm_buffer.A > 0)
	{
		//AH 1;
		pwm_buffer.levels[0].fAH = 1;
		pwm_buffer.levels[0].fAL = 0;			
		
		if(pwm_buffer.B < 0)
		{
			// BL 1;
			pwm_buffer.levels[0].fBH = 0;
			pwm_buffer.levels[0].fBL = 1;
			
			// c later
			pwm_buffer.levels[0].fCH = 0;
			pwm_buffer.levels[0].fCL = 0;
		}
		else 
		{	
			// BH 1 after A
			pwm_buffer.levels[0].fBH = 0;
			pwm_buffer.levels[0].fBL = 0;
			
			// CL 1;
			pwm_buffer.levels[0].fCH = 0;
			pwm_buffer.levels[0].fCL = 1;
			
			
		}
	}
	else if(pwm_buffer.A < 0)
	{
		// AL 1;
		pwm_buffer.levels[0].fAH = 0;
		pwm_buffer.levels[0].fAL = 1;

		if(pwm_buffer.B > 0)
		{
			// BH 1;
			pwm_buffer.levels[0].fBH = 1;
			pwm_buffer.levels[0].fBL = 0;
			
			// c later
			pwm_buffer.levels[0].fCH = 0;
			pwm_buffer.levels[0].fCL = 0;
		}
		else 
		{
			// BL 1 after A
			pwm_buffer.levels[0].fBH = 0;
			pwm_buffer.levels[0].fBL = 0;
			
			// CH 1;
			pwm_buffer.levels[0].fCL = 0;
			pwm_buffer.levels[0].fCH = 1;
		}
	}
	else 
	{
		pwm_buffer.levels[0].fAH = 0;
		pwm_buffer.levels[0].fAL = 0;
		if(pwm_buffer.B < 0)
		{
			// BL 1;
			pwm_buffer.levels[0].fBH = 0;
			pwm_buffer.levels[0].fBL = 1;
			// CH 1;
			pwm_buffer.levels[0].fCH = 1;
			pwm_buffer.levels[0].fCL = 0;
		}
		else
		{
			// BH 1;
			pwm_buffer.levels[0].fBH = 1;
			pwm_buffer.levels[0].fBL = 0;
			// CL 1;
			pwm_buffer.levels[0].fCH = 0;
			pwm_buffer.levels[0].fCL = 1;
		}
	}
	
	// now pinlevels for the second half of the on-phase
	if(signbit(pwm_buffer.A) == signbit(pwm_buffer.B))
	{
		pwm_buffer.levels[1].fAH = 0;
		pwm_buffer.levels[1].fAL = 0;
		pwm_buffer.levels[1].fCH = pwm_buffer.levels[0].fCH;
		pwm_buffer.levels[1].fCL = pwm_buffer.levels[0].fCL ;
		
		if(pwm_buffer.B > 0)
		{
			//BH = 1;
			pwm_buffer.levels[1].fBH = 1;
			pwm_buffer.levels[1].fBL = 0;
		}
		else if (pwm_buffer.B < 0 )
		{
			//BL = 1;
			pwm_buffer.levels[1].fBH = 0;
			pwm_buffer.levels[1].fBL = 1;
		}
	}
	else if(signbit(pwm_buffer.A) == signbit(pwm_buffer.C))
	{
		pwm_buffer.levels[1].fAH = 0;
		pwm_buffer.levels[1].fAL = 0;
		pwm_buffer.levels[1].fBH = pwm_buffer.levels[0].fBH;
		pwm_buffer.levels[1].fBL = pwm_buffer.levels[0].fBL;
		
		if(pwm_buffer.C > 0)
		{
			//CH = 1;
			pwm_buffer.levels[1].fCH = 1;
			pwm_buffer.levels[1].fCL = 0;
		}
		else if (pwm_buffer.C < 0 )
		{
			//CL = 1;
			pwm_buffer.levels[1].fCH = 0;
			pwm_buffer.levels[1].fCL = 1;
		}
	}
	else if(signbit(pwm_buffer.B) == signbit(pwm_buffer.C))
	{
		pwm_buffer.levels[1].fBH = 0;
		pwm_buffer.levels[1].fBL = 0;
		pwm_buffer.levels[1].fAH = pwm_buffer.levels[0].fAH;
		pwm_buffer.levels[1].fAL = pwm_buffer.levels[0].fAL;
		if (pwm_buffer.C > 0)
		{
			// CH = 1;
			pwm_buffer.levels[1].fCH = 1;
			pwm_buffer.levels[1].fCL = 0;
		}
		else if (pwm_buffer.C < 0)
		{
			// CL = 1;
			pwm_buffer.levels[1].fCH = 0;
			pwm_buffer.levels[1].fCL = 1;
		}
	}
	
	pwm_buffer.levels[2].fAH = 0;
	pwm_buffer.levels[2].fAL = 0;
	pwm_buffer.levels[2].fBH = 0;
	pwm_buffer.levels[2].fBL = 0;
	pwm_buffer.levels[2].fCH = 0;
	pwm_buffer.levels[2].fCL = 0;	
	
	// calc Portlevels (takes ages)
	// overflow
	pwm_buffer.aubPortLevels[0] = (pwm_buffer.levels[0].fAH << pwm_outpins.ubAHPin |
								pwm_buffer.levels[0].fAL << pwm_outpins.ubALPin |
								pwm_buffer.levels[0].fBH << pwm_outpins.ubBHPin |
								pwm_buffer.levels[0].fBL << pwm_outpins.ubBLPin |
								pwm_buffer.levels[0].fCH << pwm_outpins.ubCHPin |
								pwm_buffer.levels[0].fCL << pwm_outpins.ubCLPin  );
	// ocra
	pwm_buffer.aubPortLevels[1] = (pwm_buffer.levels[1].fAH << pwm_outpins.ubAHPin |
								pwm_buffer.levels[1].fAL << pwm_outpins.ubALPin |        
								pwm_buffer.levels[1].fBH << pwm_outpins.ubBHPin |        
								pwm_buffer.levels[1].fBL << pwm_outpins.ubBLPin |        
								pwm_buffer.levels[1].fCH << pwm_outpins.ubCHPin |        
								pwm_buffer.levels[1].fCL << pwm_outpins.ubCLPin  );      
	// ocrb
	pwm_buffer.aubPortLevels[2] = (pwm_buffer.levels[2].fAH << pwm_outpins.ubAHPin |  
 								pwm_buffer.levels[2].fAL << pwm_outpins.ubALPin |  
 								pwm_buffer.levels[2].fBH << pwm_outpins.ubBHPin |  
 								pwm_buffer.levels[2].fBL << pwm_outpins.ubBLPin |  
 								pwm_buffer.levels[2].fCH << pwm_outpins.ubCHPin |  
 								pwm_buffer.levels[2].fCL << pwm_outpins.ubCLPin  );
								 
	// increment addr	(sizeof(uint16_t) == 2)
	pwm_buffer.pvReadA = pwm_buffer.pvReadA + 2 * pwm_buffer.ubSpeed;
	pwm_buffer.pvReadB = pwm_buffer.pvReadB + 2 * pwm_buffer.ubSpeed;
	pwm_buffer.pvReadC = pwm_buffer.pvReadC + 2 * pwm_buffer.ubSpeed;
		
	// check if in range of buffer otherwise front of buffer 
	if (pwm_buffer.pvReadA >= pwm_buffer.pvBufferA + pwm_buffer.lenA)
	{ 
		// we have detected overflow over buffA
		pwm_buffer.pvReadA -= pwm_buffer.lenA;
	}
	if (pwm_buffer.pvReadB >= pwm_buffer.pvBufferA + pwm_buffer.lenA)
	{
		pwm_buffer.pvReadB -= pwm_buffer.lenA;
	}
	if (pwm_buffer.pvReadC >= pwm_buffer.pvBufferA + pwm_buffer.lenA)
	{   
		pwm_buffer.pvReadC -= pwm_buffer.lenA;
	}	
	PORTB &= ~(1<<1);
}

void setOutputPinsAddr(char* szParam)
{	
	char* pbParamEnd = NULL;	
	pwm_outpins.pvPORT	= (void*)(uint16_t)strtoul(szParam, &pbParamEnd, 16);
	pwm_outpins.ubAHPin = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	pwm_outpins.ubALPin = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	pwm_outpins.ubBHPin = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	pwm_outpins.ubBLPin = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	pwm_outpins.ubCHPin = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	pwm_outpins.ubCLPin = (uint16_t) strtoul(pbParamEnd, &pbParamEnd, 16);
	
	// make mask
	pwm_outpins.ubMsk = ( 1 << pwm_outpins.ubAHPin |
						  1 << pwm_outpins.ubALPin |
						  1 << pwm_outpins.ubBHPin |
						  1 << pwm_outpins.ubBLPin |
						  1 << pwm_outpins.ubCHPin |
						  1 << pwm_outpins.ubCLPin  );
}


void setPinLevles(volatile uint8_t ubPortLevel)
{
	// read value from buffer structure given by interrupt source
	// set pins from pwm_outpins
	PORTB |= 1<<2;  // for debugging timings with oszi 
	
	// remember other pins
	uint8_t ubLvl = *(uint8_t*)pwm_outpins.pvPORT;
	ubLvl = ubLvl & ~pwm_outpins.ubMsk;
	
	// set highs (and lows implicit) this may be done in main context
	ubLvl = ubLvl | ubPortLevel;
	*(uint8_t*)pwm_outpins.pvPORT = ubLvl;
	
	PORTB &= ~(1<<2);
}

ISR (TIMER3_COMPA_vect){
	setPinLevles(gaubPortLevels[1]);
}

ISR (TIMER3_COMPB_vect){
	setPinLevles(gaubPortLevels[2]);
}

/*ISR (TIMER3_COMPC_vect){
    setPinLevles(&pwm_buffer.levels[3]);
}*/

ISR (TIMER3_OVF_vect){
	// copy the structure with the current info into the one for the interrupt
	
	PORTB |= 1<<3; // stop time with osci
	//tmp_pwm_buffer = pwm_buffer;// this is too slow
	memcpy(gaubPortLevels, pwm_buffer.aubPortLevels, 3);  // remember current pin switching pattern for the current duty cycle
	fOverflow = 1;
	
	// set pinlevels according to first tmp_pwm_buffer.levels
	setPinLevles(gaubPortLevels[0]);
	
	// put ocr values from structure into timer registers
	OCR3A = pwm_buffer.OCRA;
	OCR3B = pwm_buffer.OCRB;
	//OCR3C = tmp_pwm_buffer.OCRC;
	PORTB &= ~(1<<3);
	
}