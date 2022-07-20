'''
Created on 24.11.2012

@author: Jan
'''
"""
    tkinter way of scrollbar manipulation with command function 
    and the proper way of scale 
    
"""


import Tkinter
from Tkinter import *
import threading
import time

class DebugScrollbar(Scrollbar):
    def set(self, *args):
        print "SCROLLBAR SET", args
        Scrollbar.set(self, *args)
        #listbox.delete(0,END)
        #listbox.insert(0,("SCROLLBAR SET", args))
        
class DebugListbox(Listbox):
    def yview(self, *args):
        print "LISTBOX YVIEW", args
        Listbox.yview(self, *args)    
        
def set_pulsWidth(*width):
    print "set_pulsWidth args: {0}".format(width)
    p1,p2 = scrollbar.get()
    dp = p2-p1
    print"call set with", (width[1],dp)
    scrollbar.set(width[1], float(width[1]) + dp) 
    print ""
     
def sel():
    selection = "Value = " + str(var.get())
    label.config(text = selection)

        
def bla(*args):
    print args
 
if __name__ == "__main__":
    root = Tk()
    t = threading.Thread(target = mainloop)
    t.start()
    
    scrollbar = DebugScrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.set(0,0.2)
    listbox = DebugListbox(root)
    listbox.pack()
    
    #listbox.config(yscrollcommand=scrollbar.set)
    #scrollbar.config(command=listbox.yview)
    scrollbar.config(command=set_pulsWidth)
    scrollbar.set(0,0.2)
    
    var = DoubleVar()
    scale = Scale( root, command=bla)#variable = var
    scale.pack(anchor=CENTER)

    button = Button(root, text="Get Scale Value", command=sel)
    button.pack(anchor=CENTER)

    label = Label(root)
    label.pack()
    
    while 1:
        time.sleep(1)














