'''
Created on 06.07.2012

@author: Jan

remoAVR 
used for manipulating registers in the avr over uart

Protocol: 
All values and addresses are transmitted formated in hex


_instructions_

's' set value at address
    send: s <addr> <val>\r
    recv: s <addr> <val> [err_val]\n\r
    
'g' get value from address
    send: g <addr>\r
    recv: g <addr> <value>\n\r


remoAVR does:
setup serial communication 
issue instruction
parse return value 
    evtl raise exception
    

'''

import serial
import time
import string

from avrheaderconverter.IO import *
'''
establish serial connection
get name of device 
generate header 
import header 
'''



class AVR:
    
    ser = 0
    proc_time = 0.0005  # 0.5ms to process  
    t_trans = 0.00104        # 1.04ms transmit time per bite
    type = ""
    
    def __init__(self):
        self.ser = serial.Serial(0)
        print self.ser.portstr       # check which port was really used#
        # TODO: get type from device
        self.type = "m2560"
        #from /include/avr/io import *
        
    def cleanup(self):
        self.ser.close()             # close port
        
    def setValAddr(self, addr, val):
        # make a fresh input 
        self.ser.flushInput() 
        str = 's ' + hex(addr) + ' ' + hex(val) + '\r'
        self.ser.write(str)      # write instruction string
        
        s = ""
        trans_delay = (len(str)+2) * self.t_trans
        time.sleep(trans_delay)
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        '''Todo: parse return string s
        '''
        return s
        
    def getValAddr(self, addr):
        self.ser.flushInput() 
        str = 'g ' + hex(addr) + '\r'
        self.ser.write(str)        # write instruction string
        
        s = ""
        trans_delay = (len(str)+5) * self.t_trans
        time.sleep(trans_delay)
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        return s
        
    def toggle(self, addr, tempval, delay, finalval = None):
        if finalval == None:
            ret = self.getValAddr(addr)
            finalval = int(string.rsplit(ret, ' ')[-1], 16)              
        ret = self.setValAddr(addr, tempval)
        trans_delay = delay - (len(ret) + 3) * self.t_trans
        if trans_delay < 0:
            trans_delay = 0
        time.sleep(trans_delay)
        self.setValAddr(addr, finalval)
        
    

def test():
    mc = AVR()
    
    mc.setValAddr(0x25,0xfe)
    
    ''' for e in range(8):
        mc.toggle(37,~(1<<e), 0.5)
        time.sleep(0.1)
    '''
    
    delay_bytes = 7
    while 1:
        for e in range(8):
            ret = mc.setValAddr(PORTB, ~(1<<e))
            delay =  0.125 - ((len(ret) + delay_bytes ) * mc.t_trans)
            if delay < 0:
                delay = 0
            time.sleep(delay)
    pass
        



    """
    ret = mc.getValAddr(0x25)
    print ret
    ret = mc.setValAddr(0x25, 0xfd)
    print ret
    ret = mc.getValAddr(0x25)
    print ret
    """
   
if __name__ == '__main__':
    test()
        

