"""
this script generates first quarter of a full sinus period from 0 to 2**16-1 with maximum slope of 1
this is the maximum resolution in 16bit
maybe usefull for 16bit pwm 
"""

from math import * 
p = float(0xffff)
y = [int(round(sin(e/p) * 0xffff)) for e in range(int(0xffff*pi/2))]
for e in y:
    print e, ","
