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

'm' malloc space for writing
    send: m <required space in bytes>\r
    recv: m <admitted space in bytes> <addr>\n\r
    
'f' free space allocated by malloc
    send: f <addr>\n\r
    recv: f <addr>\n\r

'b' write binary data to allocated space
    send: b <addr> <length>\r<binary_data_0:binary_data_len+1>
    recv: b <addr> <length> <currentAddr>\n\r
    
'a' set pwm buffers for wave generaton
    send: a <addrbuffA> <lenA> <addrbuffB> <lenB>\r
    recv: a <addrbuffA> <lenA> <addrbuffB> <lenB> <addr of readpointer>\r\n



remoAVR does:
setup serial communication 
issue instruction
parse return value 
    evtl raise exception
    

'''

import serial
import time
import string

# append root dir of project
import os
import sys
sys.path.append(os.path.split(__file__)[0].rsplit('\\',1)[0])

from avrheaderconverter.IO import *
import avrheaderconverter.IO as IO  # used for the class to give to user
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
    IO = IO
    
    def __init__(self):
        self.ser = serial.Serial(0, timeout=1)
        self.ser.setBaudrate(38400)
        print self.ser.portstr       # check which port was really used#
        self.type = self.reset()
        
        #from /include/avr/io import *
        
    def cleanup(self):
        self.ser.close()             # close port
        
    def setValAddr(self, addr, val):
        # make a fresh input 
        self.ser.flushInput() 
        out_str = 's ' + hex(addr) + ' ' + hex(val) + '\r'
        self.ser.write(out_str)      # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+2) * self.t_trans
        time.sleep(trans_delay)
        breaktime = time.time() + 1
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
            if time.time() > breaktime:
                raise IOError("failed to reset target")
        self.ser.flushInput()
    
        # TODO: parse return string s
        # TODO: make recursive call for larger values than 0xff  
              
        return s
        
    def getValAddr(self, addr, length = None):
        self.ser.flushInput() 
        lenstr = ""
        if length:
            lenstr = " " + hex(length)
        out_str = 'g ' + hex(addr) + lenstr + '\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        time.sleep(trans_delay)
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        finalval = int(string.rsplit(s, ' ')[-1], 16)
        return finalval
        
    def toggle(self, addr, tempval, delay, finalval = None):
        if finalval == None:
            finalval = self.getValAddr(addr)
        ret = self.setValAddr(addr, tempval)
        trans_delay = delay - (len(ret) + 3) * self.t_trans
        if trans_delay < 0:
            trans_delay = 0
        time.sleep(trans_delay)
        self.setValAddr(addr, finalval)
    
    def reset(self):
        self.setValAddr(WDTCSR,8)
        s = ""
        breaktime = time.time()+1
        while '\r' not in s:
            time.sleep(0.1)
            s += self.ser.read(self.ser.inWaiting())
            if time.time() > breaktime:
                raise IOError("failed to reset target")
        return s
    
    def operate_on_value(self, addr, op, new_val):
        old_val = self.getValAddr(addr)
        res = eval(str(old_val) +" " + op +  " " + str(new_val))
        self.setValAddr(addr, res)        
    
    def pwm_prescaler(self, cs, nr = 3):
        self.operate_on_value(TCCR3B, "&", ~7)
        self.operate_on_value(TCCR3B, "|", cs)
        pass

    
    def pwm_init(self, nr = 3, *duty_cycl_list):
        # enable output driver DDR for pin
        self.setValAddr(DDRE, 1 << 3 | 1 << 4 | 1 << 5)
                
        # b10 on com
        self.setValAddr(TCCR3A, 1 << COM3A1 | 1 << COM3B1 | 1 << COM3C1 | 1 << WGM31)
       
        #set icr to 0xffff
        self.setValAddr(ICR3H, 0xff)
        self.setValAddr(ICR3L, 0xff)
        
        # force output compare in normal mode
        #self.setValAddr(TCCR3C, 1 << FOC3A | 1 << FOC3B | 1 << FOC3C) 
        
        # cs 0b001 no prescaler
        # wgm 0 (normal) fast pwm top in icr 
        self.setValAddr(TCCR3B, 1 << CS30 | 1 << WGM32 | 1 << WGM33)        
        
    def pwm(self, param, duty_cycl):
        H = duty_cycl >> 8
        Hres = None
        while Hres != H:
            s = self.setValAddr(eval(param + "H"), duty_cycl >> 8)
            Hres = int(s.rsplit()[-1],16)
        L = duty_cycl & 0xff
        Lres = None
        while Lres != L:
            s = self.setValAddr(eval(param + "L"), duty_cycl & 0xff)
            Lres = int(s.rsplit()[-1],16)

    def malloc(self, length):
        
        self.ser.flushInput() 
        out_str = 'm ' + hex(length) + '\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        #time.sleep(trans_delay)
    
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        ret = int(string.rsplit(s, ' ')[-1], 16)
        return ret
    
    def free(self, addr):
        self.ser.flushInput() 
        out_str = 'f ' + hex(addr) + '\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans    
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput() 
        
    
    def write_binary(self,addr, in_list, base_bytes = 1, length = None, intel = True):
        if length == None:
            length = len(in_list) * base_bytes
        self.ser.flushInput() 
        
        l = []
        if intel:
            for e in in_list:
                l.extend([chr((e & 0xff << (8 * idx)) >> (8 * idx)) for idx in range(base_bytes)])
        else:
            for e in in_list:
                l.extend([chr((e & 0xff << (8 * idx)) >> (8 * idx)) for idx in range(base_bytes - 1, -1, -1)])
            
        binary_str = "".join(l)
                
        out_str = 'b ' + hex(addr) + ' ' + hex(length) + '\r' + binary_str
        
        self.ser.write(out_str)        # write instruction string
    
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans    
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput() 
        pass
    
    def set_pwm_buff(self, buffA, lenA, buffB, lenB):
        """ returns the addr of the current read pointer """
        self.ser.flushInput() 
        out_str = 'a ' + hex(buffA) + ' ' + hex(lenA) + ' ' + hex(buffB) + ' ' + hex(lenB) + '\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        #time.sleep(trans_delay)
    
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        ret = int(string.rsplit(s, ' ')[-1], 16)
        return ret
    
    def set_defaul_buff(self):
        """ returns the addr of the current read pointer"""
        self.ser.flushInput() 
        out_str = 'a 0\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        #time.sleep(trans_delay)
    
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        ret = int(string.rsplit(s, ' ')[-1], 16)
        return ret 
    
    def set_phase_shift(self, alpha, beta, gamma):
        """ phase schift in degree """
        self.ser.flushInput() 
        out_str = 'p ' + hex(alpha) + ' ' + hex(beta) + ' ' + hex(gamma) + '\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        #time.sleep(trans_delay)
    
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        ret = int(string.rsplit(s, ' ')[-1], 16)
        return ret 
    
    def set_output_pins(self,   Po, AHPi,
                                    ALPi,
                                    BHPi,
                                    BLPi,
                                    CHPi,
                                    CLPi
                        ):
        """ set the pins to be toggled by the pwm 
        retrun 0 on succes
        """
        self.ser.flushInput() 
        out_str = ( 'o ' + 
                    hex(Po)   + ' ' + 
                    hex(AHPi) + ' ' +
                    hex(ALPi) + ' ' +
                    hex(BHPi) + ' ' +
                    hex(BLPi) + ' ' +
                    hex(CHPi) + ' ' +
                    hex(CLPi) + ' ' +       
                    '\r'
                    )
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        #time.sleep(trans_delay)
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        #ret = int(string.rsplit(s, ' ')[-1], 16)
        #return ret 
        if out_str[:-2] in s:
            return False
        else:
            return True 
    
    
    def set_amplitude_and_speed(self, amplitude, speed):
        self.ser.flushInput() 
        out_str = 'A ' + hex(amplitude) + ' ' + hex(speed) + '\r'
        self.ser.write(out_str)        # write instruction string
        
        s = ""
        trans_delay = (len(out_str)+5) * self.t_trans
        #time.sleep(trans_delay)
        while '\r' not in s:
            time.sleep(self.t_trans)
            s += self.ser.read(self.ser.inWaiting())
        self.ser.flushInput()
        #ret = int(string.rsplit(s, ' ')[-1], 16)
        #return ret         
        
    
def test():
    mc = AVR()
    
    mc.setValAddr(PORTB,0xff)
    
    '''
    # toggle test
     for e in range(8):
        mc.toggle(37,~(1<<e), 0.5)
        time.sleep(0.1)
    '''
    
    """ # check for time keeping
    delay_bytes = 7
    while 1:
        for e in range(8):
            ret = mc.setValAddr(PORTB, ~(1<<e))
            delay =  0.125 - ((len(ret) + delay_bytes ) * mc.t_trans)
            if delay < 0:
                delay = 0
            time.sleep(delay)
    """ 
    
    
    bufflen= 1000
    # check for pwm buffer
    #malloc
    buffA = mc.malloc(bufflen)
    buffB = mc.malloc(bufflen)

    #make sin table
    from math import sin, pi, cos
    p = float(0xffff) #amplitude
    y = [int(round(cos(e/p) * 0xffff/2 + 0xffff/2)) for e in range(int(0xffff*pi*2))]
    hundretsin = y[::(len(y)/500)]
    ramp = range(0,2**16-1,(2**16)/500)[:500]
    
    #wrte bnary 
    mc.write_binary(buffA, ramp, 2) 
    mc.write_binary(buffB, hundretsin, 2)
    
    #set pwm 
    pcurrent = mc.set_pwm_buff(buffA, bufflen, buffB, bufflen)
    
    #start pwm
    mc.pwm_init()
    mc.pwm("OCR3B", 0x8000)  # pwm3b half duty cycle
    
    
    mc.setValAddr(TIMSK3, 1<<OCIE3A) # enable interrupt for outputcompare match 
    
    
    # in buffA    in buffb
    # 
    # 
    # 
    # 
    def isposinbuff(pos,buff,length):
        if pos >= buff and pos < buff + length:
            return True        
        return False
    
    
    lastA = True
    lastB = False
    donewithA = False
    donewithB = False
    
    cur_list = []
    
    while 1:
        
        # get current position of the lookup-table of isr cmpmatchtimer3a
        curr = mc.getValAddr(pcurrent, 2) #+ (mc.getValAddr(pcurrent+1)<<8)
        
        nowinA = isposinbuff(curr,buffA,bufflen)
        nowinB = isposinbuff(curr,buffB,bufflen)
        #print curr,"\t", nowinA, nowinB , lastA, lastB
        cur_list.append(curr)
        
        if nowinA and not lastA:
            # we are now in A write B
            #mc.write_binary(buffB, hundretsin, 2)
            pass
        if nowinB and not lastB:
            # we can now write A
            print "write A"
            ramp.reverse()
            atime = time.clock()
            mc.write_binary(buffA, ramp, 2)   
            btime = time.clock() 
            print btime-atime
        lastA = nowinA
        lastB = nowinB
    
    
        pass




        
    """
    mc.pwm_init()
    mc.reset()
    mc.setValAddr(PORTB,0xf5)

    ret = mc.getValAddr(0x25)
    print ret
    ret = mc.setValAddr(0x25, 0xfd)
    print ret
    ret = mc.getValAddr(0x25)
    print ret
    """
   
if __name__ == '__main__':
    test()
        

