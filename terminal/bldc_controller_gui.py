'''
Created on 29.09.2013

@author: Jan
'''

import time
import sys
import os
import threading
from Tkinter import *

from remoAVR import AVR

class DebugScrollbar(Scrollbar):
    
    def set(self, *args):
        print "SCROLLBAR SET", args
        Scrollbar.set(self, *args)
        #listbox.delete(0,END)
        #listbox.insert(0,("SCROLLBAR SET", args))

class BLDCControlGui(Frame):
    
    cs = 0
    speed = 0
    amplitude = 1
    
    def __init__(self, parent):
        self.fStopthread = False
        self.mc = AVR()
        
        Frame.__init__(self, parent)   
        self.parent = parent        
        self.initUI()
        
        
    def initUI(self):
                     
        # control the prescaler value of the timer used for the pwm  
        scrolPrescaler = Scale(g, from_=0, to=8, label="Prescaler")
        scrolPrescaler.pack(ipadx=5, side=RIGHT, fill=Y) 
        self.scrolPrescaler = scrolPrescaler
        scrolPrescaler.config(command=self.setPrescaler)
        
                     
        # control the timer resolution and thus the period for the pwm
        scrolPWMResolution = Scale(g, from_=0, to=16, label="PWM Resolution")
        scrolPWMResolution.pack(side=RIGHT, fill=Y, ipadx=5)
        self.scrolPWMResolution = scrolPWMResolution
        scrolPWMResolution.config(command=self.setPWMResolution)
        
        
        # control the on_period of the pwm (amplitude of the waveform)
        scrolPulswitdh = Scale(g, from_=0, to=255, label="Amplitude")
        scrolPulswitdh.pack(side=RIGHT, fill=Y, ipadx=5) 
        self.scrolPulswitdh = scrolPulswitdh
        scrolPulswitdh.config(command=self.setAmplitude)
        
        
        # control the position of the waveform in degrees
        scrolPosistion = Scale(g, from_=0, to=359, label="Position")
        scrolPosistion.pack(side=RIGHT, fill=Y, ipadx=5)
        self.scrolPosistion = scrolPosistion
        scrolPosistion.config(command=self.setPosition)
        
        
        # control the rate of turn (change of position per period)
        scrolSpeed = Scale(g, from_=0, to=60, label="Speed")
        scrolSpeed.pack(side=RIGHT, fill=Y, ipadx=5)
        self.scrolSpeed = scrolSpeed
        scrolSpeed.config(command=self.setSpeed)
        
        
        initButton = Button(g, text="init bldc controller", command=self.initPWM)
        initButton.pack(anchor=CENTER)
        self.initButton = initButton
        
        pauseBbutton = Button(g, text="toggle pause in off phase", command=self.togglePause)
        pauseBbutton.pack(anchor=CENTER)
        self.pauseBbutton = pauseBbutton
    
        #label = Label(g)
        #label.pack()
        
    def setPrescaler(self, *args):
        self.cs = int(self.scrolPrescaler.get())
        self.mc.pwm_prescaler(self.cs)    
    
    def setPWMResolution(self, *args):             
        self.baselen = int(args[0]) #int(self.scrolPWMResolution.get()) 
        reso = 2**self.baselen - 1
        self.mc.pwm_prescaler(0)
        self.mc.pwm("ICR3", reso)
        self.mc.pwm_prescaler(self.cs)
            
    def setAmplitude(self, *args):
        #'A', amplitude, speed
        # save amplitude for speed command
        self.amplitude = int(args[0])
        self.mc.set_amplitude_and_speed(self.amplitude, self.speed)        
    
    def setPosition(self, *args):
        # use setPhaseshift 
        a = (int(args[0])) % 360
        b = (int(args[0]) + 120) % 360
        c = (int(args[0]) + 240) % 360
        self.mc.set_phase_shift(a, b, c)
    
    def setSpeed(self, *args):
        #'A', amplitude, speed
        # save speed for amplitude command
        self.speed = int(args[0])
        self.mc.set_amplitude_and_speed(self.amplitude, self.speed)
        
    
    def initPWM(self, *args):
        print "PWM init"
        self.mc.pwm_init()
        #set default buffer 
        _ = self.mc.set_defaul_buff() # 'a 0'
        
        # set phase schift 
        #'p' a,b,c
        _ = self.mc.set_phase_shift(0, 120, 240)
        
        # set pins to be toggled 
        # 'o', port_ah, pin_ah, port_al, pin_al, port_bh ...
        self.mc.setValAddr(self.mc.IO.DDRJ, 0xFF) # set port F pins to output
        _ = self.mc.set_output_pins(  self.mc.IO.PORTJ, 0,
                                                        1,
                                                        2,
                                                        3,
                                                        4,
                                                        5,)
        
        # enable interrupt for outputcompare match A B C and overflow
        self.scrolPrescaler.set(3)
        self.scrolPWMResolution.set(8)
        self.scrolPulswitdh.set(1)
        self.scrolPosistion.set(0)
        self.scrolSpeed.set(0)
        
        timsk3_val = (1 << self.mc.IO.OCIE3A | 
                      1 << self.mc.IO.OCIE3B |   
                      #1 << self.mc.IO.OCIE3C |
                      1 << self.mc.IO.TOIE3  
                      )
        self.mc.setValAddr(self.mc.IO.TIMSK3, timsk3_val)  
        
    def togglePause(self, *args):
        pass

    def quit(self, *args):
        print "quit"
        self.fStopthread = True
    """
    def on_dutycycle_change_i(self, widget):
        duty_cycle = int(widget.get()) 
        self.baselen = duty_cycle
        self.mc.pwm("ICR3", self.baselen)
        
    def on_dutycycle_change(self, param, dc):
        print "scaling", dc
        self.mc.pwm(param, int(dc * self.baselen / 100))
    """  
    '''def main(self):
        while not hwg.fStopthread:
            print time.time()
            time.sleep(5)'''
           
g = None 
gui = None

def main():
    loopthread = threading.Thread(target=mainthread, args=[])
    root = Tk()
    global g
    g = root
    
    root.geometry("700x200+100+100")    
    root.title("Colors")   
    
    loopthread.start()
    
    #self.pack(fill=BOTH, expand=1)
    #canvas.pack(fill=BOTH, expand=1)
     

       
    root.mainloop()  
 
def mainthread():
    root = g
    #root.geometry("400x100+300+300")
    global gui
    gui = BLDCControlGui(root)
    #while not gui.fStopthread:
        #time.sleep(5)
        #print ".",

if __name__ == '__main__':
    main()  
    