avrheaderconverter: 
place for header conversion 

drop the device specific header in the avr folder
    you can find the appropriate header in io.h 
    in the line below #if defined (__YOUR_DEVICE__)
    
    maybe a device class specific header is needed also for example iocanxx.h

run:  h2py io.h
    or 
call: h2py.convert(['avr/io.h'])

this generates IO.py which can be imported in the terminal to
    use it just like #include <avr/io.h> names
    
Notes:
sfr_defs.h is modified in some places to be convertable.
this conversion respects only io adresses so it is intended to skip interrupt
vectors and such things. (no program memory)



terminal:
place for communication
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

________________________________________

remoAVR does:
setup serial communication 
issue instruction
parse return value 

if IO.py is imported then all registers have their usual names 

    

