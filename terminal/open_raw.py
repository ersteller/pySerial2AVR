'''
Created on 10.08.2012

@author: Thomas
'''

import time 
import os
import subprocess
import time 
import string
import remoAVR


def getRawFiles(data_path):
    # returns all files found in "raw" subfolders of data_path
    file_list = list()
    for root, dirs, files in os.walk(data_path):
        if "raw" in root:
            for e in files:
                file_list.append(root + "\\" + e) 
    return file_list

def isFileNewerThan(path, time):
    # is path newer than time(since the epoch) --> True or False
    t = os.path.getmtime(path)
    if t > time:
        return True
    else: 
        return False 
  
    
date = 0
letzte_zyklus = 0
zyklus = 900
mc = remoAVR.AVR()
mc.setValAddr(remoAVR.DDRA,0xff)
mc.setValAddr(remoAVR.PORTA,0x00)
mc.setValAddr(remoAVR.PORTB,0x01)
while 1:
    #TODO: zyklus time in config file
    anfangszeit = time.time()
    wartezeit = letzte_zyklus + zyklus - anfangszeit
    letzte_zyklus = anfangszeit
    if wartezeit > 0:
        time.sleep(wartezeit)
    
    files = getRawFiles("C:\GP5W_Shell\DATA")
    
    newest_file = 0
    
    for filepath in files:
        if isFileNewerThan (filepath,date):
            date = os.path.getmtime (filepath)
            newest_file = filepath
    
    if not newest_file:
        continue
        
      
    
    #converting g2d to raw
    
    proc = subprocess.Popen('c:\\GP5W_Shell\\GP5wSHELL.exe' +  ' ' + newest_file)
    time.sleep(5)
    proc.kill()
    
    #for filepath in files:
        #os.remove(filepath) 
    
    path, filename = os.path.split(newest_file)
    
    filename  = string.split(filename,'.')[0]
    
    F = open("C:\\GP5W_Shell\\export\\" + filename + ".csv")
         
    header = F.readline().strip()
    keys = F.readline().strip()
    #todo letzte gueltige Zeile auslesen
    werte = F.readline().strip()
    
    liste_sensoren = keys.split(",")
    liste_werte = werte.split(",")
    liste_floatwerte = list()
    for e in liste_werte:
        try:
            liste_floatwerte.append(float(e))
        except:
            liste_floatwerte.append(e)
            
    
    ergebnis_messung = dict(zip(liste_sensoren, liste_floatwerte)) 
    
    ergebnis_messung_sensoren = dict(ergebnis_messung)
        
    for key in ergebnis_messung.keys():
    
        if"#" not in key:del ergebnis_messung_sensoren[key]
        
    #senor_messwerte = list()
    


    
    for sensor_keys in ergebnis_messung_sensoren.keys():
               
        #senor_messwerte.append(ergebnis_messung_sensor[sensor_keys])
            
        sollwert = 40
        
        Kp = 22
        
        istwert= ergebnis_messung [sensor_keys] 
        regelabweichung = sollwert - istwert
        stellgroesse = regelabweichung * Kp
        
        if stellgroesse > 0:
            mc.setValAddr(remoAVR.PORTB,0x00)
            mc.toggle(remoAVR.PORTA, 1, stellgroesse)
            mc.setValAddr(remoAVR.PORTB,0xff)

            
pass


        












    
