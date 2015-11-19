'''
Created on 25.11.2012

@author: Jan
'''

"""
    helloworld with pygtk and glade 
    This is not threadable 
"""

import time
import sys
import os
import threading

from remoAVR import AVR

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)



class HellowWorldGTK:
    """This is an Hello World GTK application"""
    fStopthread = False

    def __init__(self):
        
        self.baselen = 0xffff # initial base resolution
        
        #Set the Glade file (relative path)
        self.gladefile = os.path.split(__file__)[0] + "\\pwmgui.glade"  
        self.wTree = gtk.glade.XML(self.gladefile) 
        
        #Create our dictionay and connect it
        dic = { "on_btnInit_clicked" :              self.btnInit_clicked,
                "on_window1_destroy" :              self.quit,    
                "on_scalePrescale_value_changed":   self.on_prescal_change,   
                "on_scaleOutA_value_changed":       self.on_dutycycle_change_a,
                "on_scaleOutB_value_changed":       self.on_dutycycle_change_b,
                "on_scaleOutC_value_changed":       self.on_dutycycle_change_c,
                "on_scaleICR_value_changed" :       self.on_dutycycle_change_i,
                }
        self.wTree.signal_autoconnect(dic)
        #gtk.gdk.threads_init()  # unlocking thread lock in main process
        self.mc = AVR()
        #self.mc.reset()

    def btnInit_clicked(self, widget):
        print "PWM init"
        self.mc.pwm_init()        
        
    def quit(self, widget):
        self.fStopthread = True
        gtk.main_quit()
        
    def on_prescal_change(self, widget): 
        cs = int(widget.get_value())
        self.mc.pwm_prescaler(cs)
        pass
                   
                   
    def on_dutycycle_change_a(self, widget):
        duty_cycle = widget.get_value()
        self.on_dutycycle_change("OCR3A", duty_cycle)
        
    def on_dutycycle_change_b(self, widget):
        duty_cycle = widget.get_value()
        self.on_dutycycle_change("OCR3B", duty_cycle)
        
    def on_dutycycle_change_c(self, widget):
        duty_cycle = widget.get_value()
        self.on_dutycycle_change("OCR3C", duty_cycle)
        
    def on_dutycycle_change_i(self, widget):
        duty_cycle = int(widget.get_value()) 
        self.baselen = duty_cycle
        self.mc.pwm("ICR3", self.baselen)
        self.on_dutycycle_change("OCR3A", self.wTree.get_widget("scaleOutA").get_value())
        self.on_dutycycle_change("OCR3B", self.wTree.get_widget("scaleOutB").get_value())
        self.on_dutycycle_change("OCR3C", self.wTree.get_widget("scaleOutC").get_value())
        
        
    def on_dutycycle_change(self, param, dc):
        print "scaling", dc
        self.mc.pwm(param, int(dc * self.baselen / 100))
        
    def main(self):
        while not hwg.fStopthread:
            print time.time()
            time.sleep(5)
            
if __name__ == "__main__":
    hwg = HellowWorldGTK()
    
    gtk.gdk.threads_init()
    #t= threading.Thread(target=hwg.main)
    #t.start()
    
    gtk.gdk.threads_enter()
    gtk.mainloop()
    gtk.gdk.threads_leave()    

    