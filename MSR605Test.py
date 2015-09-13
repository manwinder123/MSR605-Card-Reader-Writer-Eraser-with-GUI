#!/usr/bin/env python3

import sys, time, cardReaderExceptions, cardReader


#INITIALIZE MSR605
try:
    msr = cardReader.CardReader()
except cardReaderExceptions.MSR605ConnectError as e:
    print (e)
    sys.exit()
except cardReaderExceptions.CommunicationTestError as e:
    print (e)
    sys.exit()
    
#RESET MSR605
msr.reset()


time.sleep(1)

try:
    msr.communication_test()
except cardReaderExceptions.CommunicationTestError as e :
    print (e)
    sys.exit()

time.sleep(1)

#SENSOR TEST, REQUIRES A CARD SWIPE
try:
    msr.sensor_test()
except cardReaderExceptions.SensorTestError as e :
    print (e)
    sys.exit()

time.sleep(1)

#RAM TEST
try:
    msr.ram_test()
except cardReaderExceptions.RamTestError as e :
    print (e)
    sys.exit()

time.sleep(1)

#GETTING DEVICE MODEL
try:
    msr.get_device_model()
except cardReaderExceptions.GetDeviceModelError as e :
    print (e)
    sys.exit()
    
time.sleep(1)
    
#GET FIRMWARE VERSION
try:
    msr.get_firmware_version()
except cardReaderExceptions.GetFirmwareVersionError as e :
    print (e)
    sys.exit()

time.sleep(1)

#SETTING MSR605 TO LOW-CO, I DID LOW FIRST BECAUSE I'M PRETTY SURE HI IS THE DEFAULT
try:
    msr.set_low_co()
except cardReaderExceptions.SetCoercivityError as e :
    print (e)
    sys.exit()    

time.sleep(1)

#CHECKING IF THE MSR605 IS IN LOW-CO (WAS SET BEFORE)
try:
    msr.get_hi_or_low_co()
except cardReaderExceptions.GetCoercivityError as e :
    print (e)
    sys.exit()

time.sleep(1)

#SETTING MSR605 TO HI-CO
try:
    msr.set_hi_co()
except cardReaderExceptions.SetCoercivityError as e :
    print (e)
    sys.exit()    

time.sleep(1)

#CHECKING IF THE MSR605 IS IN HI-CO
try:
    msr.get_hi_or_low_co()
except cardReaderExceptions.GetCoercivityError as e :
    print (e)
    sys.exit()

time.sleep(2)

tracks = ['','','']

#READING THE MAGNETIC STRIPE CARD
try:
    tracks = msr.read_card()
except cardReaderExceptions.CardReadError as e :
    print (e)
    sys.exit()
except cardReaderExceptions.StatusError as e :
    print (e)
    sys.exit()
    
print ("\nTHE DATA THAT WAS READ FROM THE LAST READ (ABOVE) WILL BE USED TO WRITE")

time.sleep(2)

#WRITE THE DATA THAT WAS READ IN BACK TO THE CARD
try:
    msr.write_card(tracks, True)
except cardReaderExceptions.CardWriteError as  e :
    print (e)
    sys.exit()
except cardReaderExceptions.StatusError as e :
    print (e)
    sys.exit()

time.sleep(2)

#CHECK IF THE DATA WAS WRITTEN PROPERLY
try:
    tracks = msr.read_card()
except cardReaderExceptions.CardReadError as e :
    print (e)
    sys.exit()
except cardReaderExceptions.StatusError as e :
    print (e)
    sys.exit()
    
time.sleep(2)

#ERASED THE CARD
try:
    msr.erase_card(7)
except cardReaderExceptions.EraseCardError as e :
    print (e)
    sys.exit()

time.sleep(2)

#CHECK IF THE CARD IS ERASED
#NOTE THAT THE MSR605 WILL NO RESPOND TO EMPTY CARDS, SO YOU WILL NEED TO SWIPE A CARD WITH DATA
try:
    msr.read_card()
except cardReaderExceptions.CardReadError as e :
    print (e)
    sys.exit()
except cardReaderExceptions.StatusError as e :
    print (e)
    sys.exit()
    
print ("TRACKS: ", tracks)



#CLOSE THE SERIAL CONNECTION
msr.close_serial_connection()
    

