''' 
this place is for header conversion 

drop the device specific header in the avr folder
    you can find the appropriate header in io.h 
    in the line below #if defined (__YOUR_DEVICE__)
    
    maybe a device class specific header is needed also for example iocanxx.h

run:  h2py io.h
    or 
call: h2py.convert(['avr/io.h'])

this generates IO.py which can be imported in the terminal to 
    use avr/io.h nameing


Notes:
sfr_defs.h is modified in some places to be convertable.
this conversion respects only io adresses so it is intended to skip interrupt
vectors and such things.
'''