'''
Created on 10.08.2012

@author: Thomas
'''

import time 
import os
import subprocess 
import string
import ConfigParser
import remoAVR


def getRawFiles(data_path):
    # returns all files found in "raw" sub folders of data_path 
    file_list = list()
    for root, dirs, files in os.walk(data_path):
        if "raw" in root:
            for e in files:
                file_list.append(root + e) 
    return file_list

def isFileNewerThan(path, time):
    # is path newer than time(since the epoch) --> True or False
    t = os.path.getmtime(path)
    if t > time:
        return True
    else: 
        return False 

def readConfig():
    # reads config.txt file and generates global statements
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    
    global zyklus
    zyklus = config.getint('globals', 'zyklus')                        # sensor werte auslese zyklus in secunden 
    
    global data_path
    data_path = config.get('globals', 'data_path')                  # path of raw files
    
    global export_path
    export_path = config.get('globals', 'export_path')              # path of converted files
    
    global install_path
    install_path = config.get('globals', 'install_path')            # install path of the raw file converter
    
    global delete_used_files
    delete_used_files = config.getboolean('globals', 'delete_used_files')  # enable deleting old raw files after reading 
    
    global logger_cnt
    logger_cnt = config.getint('globals', 'logger_cnt')                # the amount of loggers                  ;# the amount of loggers
    
    global sensor_ports
    sensor_ports_list = config.items('sensor_port_assignment')
    sensor_ports
    for key, value in sensor_ports_list:
        try:
            sensor_ports[key] = int(value)
        except:
            pass
      


date = 0
letzte_zyklus = 0
zyklus = 901
data_path = "C:\\GP5W_Shell\\DATA\\"
export_path = "C:\\GP5W_Shell\\export\\"
install_path = "c:\\GP5W_Shell\\GP5wSHELL.exe"
delete_used_files = False
sensor_ports = dict() 

# overwrite default values if present in config file
readConfig()     


mc = remoAVR.AVR()
mc.setValAddr(remoAVR.DDRA,0xff)
mc.setValAddr(remoAVR.PORTA,0x00)
mc.setValAddr(remoAVR.PORTB,0x01)
while 1:
    anfangszeit = time.time()
    wartezeit = letzte_zyklus + zyklus - anfangszeit
    letzte_zyklus = anfangszeit
    if wartezeit > 0:
        time.sleep(wartezeit)
    
    files = getRawFiles(data_path)
    
    newest_file = 0
    # TODO: multiple loggers generate more than one new file
    for filepath in files:
        if isFileNewerThan (filepath,date):
            date = os.path.getmtime (filepath)
            newest_file = filepath
    
    if not newest_file:
        continue
        
    #converting g2d to raw
    proc = subprocess.Popen( install_path +  ' ' + newest_file)
    time.sleep(5)
    proc.kill()
    
    if delete_used_files: 
        for filepath in files:
            os.remove(filepath) 
    
    # open exported file
    path, filename = os.path.split(newest_file)
    # drop file extension from filename
    filename  = string.split(filename,'.')[0]
    F = open(export_path + filename + ".csv")
         
    header = F.readline().strip()
    keys = F.readline().strip()
    # TODO: readout last valid line in file 
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
    


    # TODO: sensor port zuordnen
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


        












    
