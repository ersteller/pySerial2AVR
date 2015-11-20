This project has the goal to manipulate input and output pins of avr devices over serial interface,
allowing python scripts to set and get io states of the device. 

it is possible to change io manually in realtime with a terminal input according to the protocol.

There are some functions to manipulate the PWM module. PWM controll gui uses these functions.
this allows for microstepping a bldc-motor. 

TODO: problem is rather large minimum pulse width resulting from pin level calculation in isr 

it consists of 
- terminal class: 	handling the communication with the device for python scripts 
- headerconverter: 	to be able to use familiar naming conventions in python
- filehandler:		polling folders for input files 
- avr firmware:     serving the incoming requests


avrheaderconverter: 
- place for header conversion 

- drop the device specific header in the avr folder
    you can find the appropriate header in io.h 
    in the line below #if defined (__YOUR_DEVICE__)
    
    maybe a device class specific header is needed also, for example iocanxx.h
    
- run:  h2py io.h
    or 
- call: h2py.convert(['avr/io.h'])

- this generates IO.py which can be imported in the terminal to
    use it just like #include <avr/io.h> names
    
Notes:
sfr_defs.h is modified in some places to be convertable.
this conversion respects only io adresses so it is intended to skip interrupt
vectors and such things. (no program memory)



terminal:
- place for communication
	remoAVR:
		AVR class used for manipulating registers in the device over uart
		
		Protocol: 
		All values and addresses are transmitted formated in hex (0x12af)
		
		__instructions:_________________________
		
		's' set value at address
		    send: s <addr> <val>\r
		    recv: s <addr> <val> [err_val]\n\r
		    
		'g' get value from address
		    send: g <addr>\r
		    recv: g <addr> <value>\n\r
		    
		'm' malloc
		    send: m <size>\r
		    recv: m <size> <addr>\n\r
		    
		'f' free memor
		    send: f <addr>\r
		    recv: f <addr>\n\r
		    
		'b'  write binary stream of len 
		    binary data is received without response

	        'a' setPWMBuffer defaults to sin LUT if no addr specified
	            send: a <addr>\r
	            recv: a <addr> <realaddr>\n\r  

		'p' setPhaseShift in number of sample offset in LUT buffer
		    send: p <phaseA> <phaseB> <phaseC>\r
	            recv: p <phaseA> <phaseB> <phaseC>\n\r  

		'o' setOutputPinsAddr 
		    send: o <portAddr> <AHighPinNr> <ALowPinNr> <BHighPinNr> <BLowPinNr> <CHighPinNr> <CLowPinNr> \r
	            recv: o <portAddr> <AHighPinNr> <ALowPinNr> <BHighPinNr> <BLowPinNr> <CHighPinNr> <CLowPinNr> \n\r  
	            
		'A' setAmplidudeAndSpeed
		    currently not usefull (amplification is only natural numbers (uint8) and speed not imlemented)

		  
		________________________________________
		
		
		
		remoAVR does:
		setup serial communication 
		issue instruction
		parse return value 
		
		if IO.py is imported then all registers can be addressed through their usual names 


filehandler:
only proof of concept atm



avr firmware:
based on Peter Fleury's uart. 
waits for a instruction to be finalized with return
is build in avr studio 6 
for atmega2560 uart0 (tested)
for atmega16  uart (tested)


