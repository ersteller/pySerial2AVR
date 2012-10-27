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
                file_list.append(root+"\\"+ e) 
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
    
    # TODO: sollwert pro senso SOLLWERT
    
    global data_path
    data_path = config.get('globals', 'data_path')                  # path of raw files
    
    global export_path
    export_path = config.get('globals', 'export_path')              # path of converted files
    
    global install_path
    install_path = config.get('globals', 'install_path')            # install path of the raw file converter
    
    global Kp
    Kp = config.getint('globals', 'Kp')
    
    global delete_used_files
    delete_used_files = config.getboolean('globals', 'delete_used_files')  # enable deleting old raw files after reading 
    
    global loggers
    loggers_keyvalue = config.items('loggers')                                   # list sensor_names
    for key, value in loggers_keyvalue:
        loggers[int(key)] = value
        
    global sensor_ports
    sensor_ports_list = config.items('sensor_port_assignment')
    sensor_ports
    for key, value in sensor_ports_list:
        try:
            sensor_ports[key] = int(value)
        except:
            pass
 
# internal wiring       
PinPort = dict()    
PinPort['1'] = (remoAVR.PORTA, 0x01) 
PinPort['2'] = (remoAVR.PORTA, 0x02)
PinPort['3'] = (remoAVR.PORTA, 0x04)
PinPort['4'] = (remoAVR.PORTA, 0x08)
PinPort['5'] = (remoAVR.PORTA, 0x10)
PinPort['6'] = (remoAVR.PORTA, 0x20)
PinPort['7'] = (remoAVR.PORTA, 0x40)
PinPort['8'] = (remoAVR.PORTA, 0x80)
PinPort['9'] = (remoAVR.PORTB, 0x01)
PinPort['10'] = (remoAVR.PORTB, 0x02)
PinPort['11'] = (remoAVR.PORTB, 0x04)
PinPort['12'] = (remoAVR.PORTB, 0x08)
PinPort['13'] = (remoAVR.PORTB, 0x10)
PinPort['14'] = (remoAVR.PORTB, 0x20)
PinPort['15'] = (remoAVR.PORTB, 0x40)
PinPort['16'] = (remoAVR.PORTB, 0x80)
  
def getPort(logger, sensor):
    # may raise key value error if "logger,sensor" has no Port assignment
    Port = sensor_ports[str(logger) + "," + str(sensor)]    
    return PinPort[str(Port)]


date = 0
letzte_zyklus = 0
zyklus = 901
Kp = 0
data_path = "C:\\GP5W_Shell\\DATA\\"
export_path = "C:\\GP5W_Shell\\export\\"
install_path = "c:\\GP5W_Shell\\GP5wSHELL.exe"
delete_used_files = False
sensor_ports = dict() 
loggers = dict()

# overwrite default values if present in config file
readConfig() 
  
date = loggers.keys() #allocate a date for each logger folder

mc = remoAVR.AVR()
mc.setValAddr(remoAVR.DDRA,0xff)
mc.setValAddr(remoAVR.PORTA,0x00)
#mc.setValAddr(remoAVR.PORTB,0x00)
while 1:
    print "start new zycle"
    anfangszeit = time.time()
    wartezeit = letzte_zyklus + zyklus - anfangszeit
    letzte_zyklus = anfangszeit
    if wartezeit > 0:
        print "sleep {} sec".format(wartezeit)
        time.sleep(wartezeit)
    
    for logger in loggers.keys():
        print "processing data from logger {0}".format(loggers[logger])
        
        files = getRawFiles(data_path + loggers[logger] + "\\")
        
        newest_file = 0

        for filepath in files:
            if isFileNewerThan(filepath,date[logger]):
                date[logger] = os.path.getmtime (filepath)
                newest_file = filepath
        
        if not newest_file:
            continue
            
        #converting g2d to raw
        print "opening conversion shell" 
        proc = subprocess.Popen( install_path +  ' ' + newest_file)
        time.sleep(5)
        proc.kill()
        print "killed conversion shell"
        
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
        
        # readout last valid line in file 
        liste_werte = None
        for line in F.readlines():
            werte = line.strip()
            try:
                int(werte.split(",")[0])
                liste_werte = werte.split(",")
            except:
                continue
                    
        F.close()
        
        liste_sensoren = keys.split(",")
        liste_floatwerte = list()
        for e in liste_werte:
            try:
                liste_floatwerte.append(float(e))
            except:
                liste_floatwerte.append(e)
                
        
        ergebnis_messung = dict(zip(liste_sensoren, liste_floatwerte)) 
        
        ergebnis_messung_sensoren = dict()   
        for key in ergebnis_messung.keys():
            #parse the key for a number
            int_list = []
            for s in key:
                try:
                    if ":" in s:
                        break
                    int_list.append(int(s))
                except ValueError:
                    # ignore bad strings
                    pass
            
            if len(int_list) != 0:
                s = ""
                for i in int_list:
                    s = s+ str(i)
                ergebnis_messung_sensoren[int(s)] = ergebnis_messung[key]
            
  
    
        # TODO: sollwert pro sensor
        for sensor_keys in ergebnis_messung_sensoren.keys():
            print "sensor {}".format(sensor_keys)
                          
            sollwert = 30
            
            istwert= ergebnis_messung_sensoren[sensor_keys] 
            regelabweichung = sollwert - istwert
            stellgroesse = regelabweichung * Kp
            
            try:
                Port, Pin = getPort(logger, sensor_keys)
                if stellgroesse > 0:
                    #mc.setValAddr(remoAVR.PORTB,0x00)
                    mc.toggle(Port, Pin, stellgroesse)                
                    #mc.setValAddr(remoAVR.PORTB,0x01)
            except:
                print """logger {} kanal {} 
                hat keinen zugewiesenen Port""".format(
                                                       loggers[logger],
                                                       sensor_keys)
                print "stellgroesse waere: {}".format(stellgroesse)
