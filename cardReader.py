#!/usr/bin/env python3

""" cardReader.py
    
    LISENSE:
        This file is part of MSR605 Card Reader/Writer.
    
        MSR605 Card Reader/Writer is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by the Free
        Software Foundation, either version 3 of the License, or (at your option) any
        later version.
    
        MSR605 Card Reader/Writer is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
        or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
        more details.
    
        You should have received a copy of the GNU General Public License
        along with MSR605 Card Reader/Writer.  If not, see <http://www.gnu.org/licenses/>.
        
        MSR605 Card Reader/Writer version 1, Copyright (C) 2017 of Manwinder Sidhu
        
    Edited: 25 August 2017
    Author: Manwinder Sidhu
    Contact: manwindersapps@gmail.com
    Platform: Windows
    Python: 3.5.2

    Description: This is an interface that allows manipulation of the MSR605 magnetic
                 stripe card reader/writer.
    

                There is a programming manual for the MSR605:
                    https://docs.google.com/file/d/0B9M7JgYQ-UQdT2ZUMk9aUDBNUnc/edit
                    
                I also got some understanding of how to use it with python from these sites:                
                    https://www.triades.net/msr605-driver.html
                    https://github.com/pezmanlou/msr605
                    
                
                I don't use Python much, so if there are any coding style problems that don't
                conform to the PEP 8 standard feel free to email me
                
                This class imports serial which is pySerial module, more info on it here:
                    http://pyserial.sourceforge.net/index.html
                    
                It also imports time, just incase you want to include delays, I had some but I
                took them out
                
                It also imports isoStandardDictionary which follows an ISO standard (described
                here:  http://www.abacus21.com/magnetic-strip-encoding-1586.html) for how to
                encode the 3 tracks on the magnetic stripe card (magstripe)
                
                
                The programming manual mostly has info in Hex (Base 16) and Decimal (Base 10)
                but also has some info in Binary (Base 2). If you're confused about it I provide
                some comments on both hex and decimal implementations. I recommned looking at an
                ASCII table if you're confused
                
"""


import serial, time, sys, cardReaderExceptions

from isoStandardDictionary import isoDictionaryTrackOne, isoDictionaryTrackTwoThree,\
        iso_standard_track_check

#These constants are from the MSR605 Programming Manual under 'Section 6 Command and Response'
#I thought it would be easier if I used constants rather than putting hex in the code

#\x is the escape character for hex in python

#these three are used a lot, i think they are called control characters
ESCAPE = b'\x1B'
FILE_SEPERATOR = b'\x1C'
ACKNOWLEDGE = b'\x79'

#used when reading and writing 
START_OF_HEADING = b'\x01'
START_OF_TEXT = b'\x02'
END_OF_TEXT = b'\x03'

#used to manipulate the MSR605
RESET = b'\x61'
READ = b'\x72'
WRITE = b'\x77'
COMMUNICATIONS_TEST = b'\x65'
ALL_LED_OFF = b'\x81'
ALL_LED_ON = b'\x82'
GREEN_LED_ON = b'\x83'
YELLOW_LED_ON = b'\x84'
RED_LED_ON = b'\x85'
SENSOR_TEST = b'\x86'
RAM_TEST = b'\x87'
ERASE_CARD = b'\x63'
DEVICE_MODEL = b'\x74'
FIRMWARE = b'\x76'
HI_CO = b'\x78'
LOW_CO = b'\x79'
HI_OR_LOW_CO = b'\x64'


class CardReader():
    """Allows interfacing with the MSR605 using the serial module
        
        I have not implemented all the functionality described in the MSR605 programming
        manual, here is what I have not implemented:
            
            - Set leading zero, Check leading zero, Select BPI, Read raw data, Write raw
              data, Set BPC
              
            This functionality wasn't added because I didn't require it but can easily be
            implemented if you follow the programming manual
        
        Attributes:
            A lot of constants lol
    """
    
    
    
    def __init__(self):
        """Connects to the MSR605 using pyserial (serial connection)
        
            Checks the first 256 COM ports, hopefully the MSR605 is connected to
            one of those ports
        
            Args:
                None
        
            Returns:
                Nothing
        
            Raises:
                MSR605ConnectError: An error occurred when connecting to the MSR605
        """
        
        print ("\nATTEMPTING TO CONNECT TO MSR605")
        
        #this looks for the first available COM port, can be changed to look for the MSR
        for x in range(0, 255):
            try:

                self.__serialConn = serial.Serial('COM' + str(x))  # opens the serial port
            except(serial.SerialException, OSError):
                pass #continues going through the loop
            
        #checks to see if the serial connection exists
        try:
            self.__serialConn
        except(NameError, AttributeError):
            raise cardReaderExceptions.MSR605ConnectError("THE CARD READER IS BEING USED BY "
                                                          "SOMETHING ELSE OR IT IS NOT PLUGGED IN")


        #this is in the Programmers Manual under 'Section 8 Communication Sequence', it states
        #how to properly initialize the MSR605
        print ("\nINITIALIZING THE MSR605")
        
        self.reset()
        
        try:
            self.communication_test()
        except cardReaderExceptions.CommunicationTestError as e:
            raise (cardReaderExceptions.CommunicationTestError(e))
            
        self.reset()
        
        print ("\nCONNECTED TO MSR605")
        
        
    def close_serial_connection(self):
        """closes the serial connection to the MSR605
            
            Allows other applications to use the MSR605
        
            Args:
                None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nCLOSING COM PORT SERIAL CONNECTION")
        
        self.__serialConn.close()



    def reset(self):
        """This command reset the MSR605 to initial state.
        
            Args:
                None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nATTEMPTING TO RESET THE MSR605")
        
        # flusing the input and output solves the issue where the MSR605 app/gui would need
        # to be restarted if there was an issue like say swiping the card backwards, I 
        # found out about the flushing input & output before the reset from this MSR605
        # project: https://github.com/steeve/msr605/blob/master/msr605.py
        # I assume before there would be data left on the buffer which would mess up
        # the reading and writing of commands since there would be extra data which
        # wasn't expected
        self.__serialConn.flushInput()
        self.__serialConn.flushOutput()

        #writes the command code for resetting the MSR605
        self.__serialConn.write(ESCAPE + RESET)
        
        #so i might be a noob here but from what i read, flush waits for the command above
        #to fully write and complete, I thought this was better than adding time delays
        self.__serialConn.flush() 
        
        
        print ("MSR605 SHOULD'VE BEEN RESET")
        #there is no response from the MSR605
        
        return None
    
    
    
    # **************************************************
    #
    #        MSR605 Read/Write/Erase Card Functions
    #
    # **************************************************
    
    def read_card(self):
        """This command request MSR605 to read a card swiped and respond with
            the data read.
        
            Here is a simplification of Section 7 Data Format from the Programming Manual
            of what the response should look like when reading a magstripe card, shown in
            ASCII and Hexidecimal
            
                ASCII:
                    Response:[DataBlock]<ESC>[StatusByte]
                        DataBlock: <ESC>s[Carddata]?<FS><ESC>[Status]
                            Carddata: <ESC>1[string1]<ESC>2[string2]<ESC>3[string3]
                        Status:
                            OK: 0
                            Error, Write or read error: 1
                            Command format error: 2
                            Invalid command: 4
                            Invalid card swipe when in write mode: 9
                            
                HEX:
                    Response:[DataBlock] 1B [StatusByte]
                        DataBlock: 1B 73 [Carddata] 3F 1C 1B [Status]
                            Carddata: 1B 01 [string1] 1B 02 [string2] 1B 03[string3]
                        Status:
                            OK: 0x30h
                            Error, Write or read error: 0x31h
                            Command format error: 0x32h
                            Invalid command: 0x34h
                            Invalid card swipe when in write mode: 0x39h
        
            Args:
                None
        
            Returns:
                An array of size 3, that contains the 3 tracks from a
                magstripe card (magnetic stripe card)
                example:
        
                [
                    track 1,
                    track 2,
                    track 3
                ]
        
                [
                    A1234568^Jon Snow^           0123,
                    1234567890=01010,
                    9876
                ]
        
                Not all tracks contain data, most magstripe cards do not
                contain track 3 data.
                
                For more examples you can go to:
                    http://en.wikipedia.org/wiki/Magnetic_stripe_card
                    **the examples start Financial cards part of the wiki article**
                    
                For more info on the track data and ISO standard check out these sites:
                    http://www.abacus21.com/magnetic-strip-encoding-1586.html
                    http://www.gae.ucm.es/~padilla/extrawork/tracks.html
                    http://www.magtek.com/documentation/public/99800004-1.08.pdf
        
            Raises:
                CardReadError: An error occurred when trying to read the magstripe card, this
                                is a Datablock error, refer to the MSR605 Programmer's Manual
                                
                StatusError: If something went wrong during the reading of the card, this is
                                the Status Byte error, it could also be a Status error from
                                the Ending Field in the Data Block
                             
        """
        
        print ("\nATTEMPTING TO READ FROM CARD (SWIPE NOW)")        
        #read in track data will be stored in this array
        tracks = ['','','']
        
        #command code for reading written to the MSR605
        self.__serialConn.write(ESCAPE + READ)
        self.__serialConn.flush()
        
        
        #response from the MSR605
        #goes through what is expected as output from the MSR
        if self.__serialConn.read() != ESCAPE:
            return cardReaderExceptions.CardReadError("[Datablock] READ ERROR, R/W Data "
                                            "Field, looking for ESCAPE(\x1B)", None)
        
        if self.__serialConn.read() != b's':
            return cardReaderExceptions.CardReadError("[Datablock] READ ERROR, R/W Data "
                                            "Field, looking for s (\x73)", None)
        
        if self.__serialConn.read() != ESCAPE:
            return cardReaderExceptions.CardReadError("[Carddata] READ ERROR, R/W Data "
                                            "Field, looking for ESCAPE(\x1B)", None)
        
        
        
        #track one data will be read in, this isn't raising an exception because the card
        #might not have track 1 data 
        if self.__serialConn.read() != START_OF_HEADING:
            
            #could be changed to be stored in some sort of error data structure and returned
            #with track data array but lets keep it simple for now ;)
            print ("This card might not have a TRACK 1")
            print ("[Carddata] READ ERROR, R/W Data Field, looking for START OF HEAD - SOH(\x01)")
            
        #if there is a track 1 then the data is read and stored
        else:
            
            tracks[0] = self.read_until(ESCAPE, 1, True)
            print ("TRACK 1: ", tracks[0])
            
            #removes any ? and %, theses are part of the ISO standard and also have
            #to be removed for writing to the card, the MSR605 adds the question marks automatically
            if (len(tracks[0]) > 0):
                if(tracks[0][-1] == '?'): 
                    tracks[0] = tracks[0][:-1]
                
                if(tracks[0][0] == '%'): 
                    tracks[0] = tracks[0][1:]
                
            else:
                tracks[0] = ''
                
        #track 2
        if self.__serialConn.read() != START_OF_TEXT:
            print ("This card might not have a TRACK 2")
            print ("[Carddata] READ ERROR, R/W Data Field, looking for START OF TEXT - STX(\x02)")
            
        else:
            
            tracks[1] = self.read_until(ESCAPE, 2, True)
            print ("TRACK 2: " , tracks[1])
            
            if (len(tracks[1]) > 0):
                if(tracks[1][-1] == '?'):
                    tracks[1] = tracks[1][:-1]
                
                #removes any semicolons, these are added automatically when writing
                if(tracks[1][0] == ';'): 
                    tracks[1] = tracks[1][1:]
                    
            else:
                tracks[1] = ''
        
        #track 3
        if self.__serialConn.read() != END_OF_TEXT:
            print ("This card might not have a TRACK 3")
            print ("[Carddata] READ ERROR, R/W Data Field, looking for END OF TEXT - ETX(\x03)")
        else:
            
            tracks[2] = self.read_until(FILE_SEPERATOR, 3, True)
            print ("TRACK 3: " , tracks[2])
            
            if (len(tracks[2]) > 0):
                if(tracks[2][-1] != '?'):
                    tracks[2] += '?'
                    
                if(tracks[2][0] == ';'): 
                    tracks[2] = tracks[2][1:]    
                
            else: #since track 3 requres a ? when writing
                tracks[2] = '?'
        
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.CardReadError("[Datablock] READ ERROR, Ending "
                                                    "Field, looking for ESCAPE(\x1B)",
                                                    tracks)
        
        #this reads the status byte and raises exceptions
        self.status_read()
                
        return tracks
    
    
    def write_card(self, tracks, statusByteCheck):
        """This command request MSR605 to write the Data Block into the card
            swiped.
        
            Refer to the docstring of the read function for an example of how to
            sort of format the tracks, it is changed a little bit, here is an example:
        
            Args:
                tracks: An array of size 3, each index is a track.
                
                statusByteCheck: A boolean that if true will enable the regular statusByte
                                checks, if its false it will not check the statusByte
        
            Returns:
               None
        
            Raises:
                CardWriteError: An error occurred when writing to the magstripe card
        """
        
        print ("\nWRITING TO CARD (SWIPE NOW)")
        
        #Data block of the command code when writing to a magstripe card
        dataToWrite = (ESCAPE + b's' + ESCAPE + START_OF_HEADING + (tracks[0]).encode() + ESCAPE +
        START_OF_TEXT + (tracks[1]).encode() + ESCAPE + END_OF_TEXT + (tracks[2]).encode()  + FILE_SEPERATOR)
        
        print ("\nWRITING TO DEVICE/CARD")
        
        print ("DATA TO WRITE: " , dataToWrite)
        
        #complete command code when writing to magstripe card
        self.__serialConn.write(ESCAPE + WRITE + dataToWrite)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.CardWriteError("[Datablock] WRITE ERROR, R/W Data Field, "
                                                      "looking for ESCAPE(\x1B)")
        
        #this doesn't usually return anything for me, its supposed to return the Status Byte
        #i've added an option just incase it's not returning anything
        if (statusByteCheck):
            self.status_read()
        else:            
            print ("Status (not checking byte):" , self.__serialConn.read())
        
        print ("DATA HAS BEEN SUCCESSFULLY WRITTEN TO THE CARD")
        
        return None


    def erase_card(self, trackSelect):
        """This command is used to erase the card data when card swipe.
        
            NOTE** THAT ERASED CARDS CANNOT BE READ

        Args:
            trackSelect: is an integer between 0-7, this dictates which track(s) to delete
            
            
            ex:
                The [Select Byte] is what goes at the end of the command code, after the
                ESCAPE and 0x6C
            
                Binary:
                    *[Select Byte] format:
                                            00000000: Track 1 only
                                            00000010: Track 2 only
                                            00000100: Track 3 only
                                            00000011: Track 1 & 2
                                            00000101: Track 1 & 3
                                            00000110: Track 2 & 3
                                            00000111: Track 1, 2 & 3
                
                Decimal:
                    *[Select Byte] format:
                                            0: Track 1 only
                                            2: Track 2 only
                                            4: Track 3 only
                                            3: Track 1 & 2
                                            5: Track 1 & 3
                                            6: Track 2 & 3
                                            7: Track 1, 2 & 3
                
                
        Returns:
            Nothing
    
        Raises:
            EraseCardError: An error occurred while erasing the magstripe card
        """
        
        #checks if the track(s) that was choosen to be erased is/are valid track(s)
        if not(trackSelect >= 0 and trackSelect <=7 and trackSelect != 1):
            raise cardReaderExceptions.EraseCardError("Track selection provided is invalid, has to "
                                                        "between 0-7")
        
        print ("\nERASING CARD (SWIPE NOW)")
        
        #command code for erasing a magstripe card
        self.__serialConn.write(ESCAPE + ERASE_CARD + (str(trackSelect)).encode())
        self.__serialConn.flush()
        
        
        #response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.EraseCardError("ERASE CARD ERROR, looking for ESCAPE(\x1B)")
        
        eraseCardResponse = self.__serialConn.read()
        if eraseCardResponse != b'0':
            if eraseCardResponse != b'A':            
                raise cardReaderExceptions.EraseCardError("ERASE CARD ERROR, looking for A(\x41), "
                                                "the card was not erased but the erasing "
                                                "didn't fail, so this is a weird case")
            else:
                raise cardReaderExceptions.EraseCardError("ERASE CARD ERROR, the card might have not "
                                                "been erased")
        
        
        print ("CARD HAS BEEN SUCCESSFULLY ERASED")
        
        return None

    
    # **********************************
    #
    #        LED Functions
    #
    # **********************************
    
    def led_off(self):
        """ This command is used to turn off all the LEDs.        

            Args:
               None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nLED'S OFF")
        
        #command code to turn off all the LED's, note that LED's turn on automatically based
        #on certain commands like read and write
        self.__serialConn.write(ESCAPE + ALL_LED_OFF)
        self.__serialConn.flush()
    
        #no response from the MSR605, just the LED change
        
        return None
    
    def led_on(self):
        """ This command is used to turn on all the LEDs.
        

            Args:
               None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nLED'S ON")
        
        #command code to turn on all the LED's, note that LED's turn on automatically based
        #on certain commands like read and write
        self.__serialConn.write(ESCAPE + ALL_LED_ON)
        self.__serialConn.flush()
    
        #no response from the MSR605, just the LED change
    
        return None
    
    def green_led_on(self):
        """ This command is used to turn on the green LEDs.
        
            Args:
               None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nGREEN LED ON")
        
        #command code to turn on the green LED, note that LED's turn on automatically based
        #on certain commands like read and write
        self.__serialConn.write(ESCAPE + GREEN_LED_ON)
        self.__serialConn.flush()
        
        #no response from the MSR605, just the LED change
    
        return None
    
    def yellow_led_on(self):
        """ This command is used to turn on the yellow LED.
        
            Args:
               None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nYELLOW LED ON")
        
        #command code to turn on the yellow LED, note that LED's turn on automatically based
        #on certain commands like read and write
        self.__serialConn.write(ESCAPE + YELLOW_LED_ON)
        self.__serialConn.flush()
    
        #no response from the MSR605, just the LED change
    
        return None
    
    def red_led_on(self):
        """ This command is used to turn on the red LED.
        
            Args:
               None
        
            Returns:
                Nothing
        
            Raises:
                Nothing
        """
        
        print ("\nRED LED ON")
        
        #command code to turn on the red LED, note that LED's turn on automatically based
        #on certain commands like read and write
        self.__serialConn.write(ESCAPE + RED_LED_ON)
        self.__serialConn.flush()
        
        #no response from the MSR605, just the LED change
        
        return None

    # ****************************************
    #
    #        MSR605 Hardware Test Functions
    #
    # ****************************************
    
    def communication_test(self):
        """This command is used to verify that the communication link between computer and
            MSR605 is up and good.
        
            Args:
                None
        
            Returns:
                None
        
            Raises:
                CommunicationTestError: An error occurred while testing the MSR605's communication
        """
        
        print ("\nCHECK COMMUNICATION LINK BETWEEN THE COMPUTER AND THE MSR605")
        
        #command code for testing the MSR605 Communication with the Computer 
        self.__serialConn.write(ESCAPE + COMMUNICATIONS_TEST)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.CommunicationTestError("COMMUNICATION ERROR, looking for "
                                                              "ESCAPE(\x1B)")
            return None
        
        if self.__serialConn.read() != b'y':
            raise cardReaderExceptions.CommunicationTestError("COMMUNICATION ERROR, looking for "
                                                              "y(\x79)")
    
        print ("COMMUNICATION IS GOOD")
    
        return None

    def sensor_test(self):
        """ This command is used to verify that the card sensing circuit of MSR605 is
            working properly. MSR605 will not response until a card is sensed or receive
            a RESET command.
        
            NOTE** A CARD NEEDS TO BE SWIPED AS STATED ABOVE
        
            Args:
               None
        
            Returns:
                Nothing
        
            Raises:
                SensorTestError: An error occurred while testing the MSR605's communication
        """
        
        print ("\nTESTING SENSOR'S")
        
        #command code for testing the card sensing circuit
        self.__serialConn.write(ESCAPE + SENSOR_TEST)
        self.__serialConn.flush()
        
        
        #response/output from the MSR605        
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.SensorTestError("SENSOR TEST ERROR, looking for ESCAPE(\x1B)")
        
        if self.__serialConn.read() != b'0':
            raise cardReaderExceptions.SensorTestError("SENSOR TEST ERROR, looking for 0(\x30)")
    
        print ("TESTS WERE SUCCESSFUL")
    
        return None
    
    def ram_test(self):
        """This command is used to request MSR605 to perform a test on its on board RAM.
    
        Args:
            Nothing
    
        Returns:
            Nothing
    
        Raises:
            RamTestError: An error occurred accessing the bigtable.Table object.
        """
        
        print ("\nTESTING THE RAM")
        
        #command code for testing the ram
        self.__serialConn.write(ESCAPE + RAM_TEST)
        self.__serialConn.flush()
        
        
        #response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.RamTestError("RAM TEST ERROR, looking for ESCAPE(\x1B)")
        
        ramTestResponse = self.__serialConn.read()
        
        if ramTestResponse != b'0':
            
            if ramTestResponse != b'A':
                raise cardReaderExceptions.RamTestError("RAM TEST ERROR, looking for A(\x41), the "
                                              "RAM is not ok but the RAM hasn't failed a "
                                              "test either, so this is a weird case")
            
            else:                
                raise cardReaderExceptions.RamTestError("RAM TEST ERROR, the RAM test has failed")
        
        print ("RAM TESTS SUCCESSFUL")
        
        return None
    
    
 
    # **********************************
    #
    #     MSR605 Coercivity functions 
    #
    # **********************************
    
    def set_hi_co(self):
        """This command is used to set MSR605 status to write Hi-Co card.
        
        Hi-Coercivity (Hi-Co) is just one kind of magstripe card, the other
        being Low-Coercivity (Low-Co), google for more info
    
        Args:
            None
            
        Returns:
            Nothing
    
        Raises:
            SetCoercivityError: An error occurred when setting the coercivity 
        """
        
        print ("\nSETTING THE MSR605 TO HI-COERCIVITY")
    
        #command code for setting the MSR605 to Hi-Coercivity
        
        self.__serialConn.write(ESCAPE + HI_CO)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        #for some reason i get this response before getting to the escape character EVU3.10
        
        #if this is false than move on to the next part of the response
        if self.__serialConn.read() != ESCAPE:
           
            #just read until the 0 of the EVU3.10 response
            self.read_until('0', 4, False)
            
            #after reading that weird response,i check if there is an ESCAPE character
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.SetCoercivityError("SETTING THE DEVICE TO HI-CO ERROR"
                                                            ", looking for ESCAPE(\x1B)", "high")
        
        
        
        
        
        if self.__serialConn.read() != b'0':
            raise cardReaderExceptions.SetCoercivityError("SETTING THE DEVICE TO HI-CO ERROR, looking "
                                                            "for 0(\x30), Device might have not been set "
                                                            "to Hi-Co", "high")
        
        print ("SUCCESSFULLY SET THE MSR605 TO HI-COERCIVITY")
        
        return None
    
    def set_low_co(self):
        """This command is used to set MSR605 status to write Low-Co card.
        
        Hi-Coercivity (Hi-Co) is just one kind of magstripe card, the other
        being Low-Coercivity (Low-Co), google for more info
    
        Args:
            None
            
        Returns:
            Nothing
    
        Raises:
            SetCoercivityError: An error occurred when setting the coercivity 
        """
        
        print ("\nSETTING THE MSR605 TO LOW-COERCIVITY")
    
        #command code for setting the MSR605 to Low-Coercivity
        self.__serialConn.write(ESCAPE + LOW_CO)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        #for some reason i get this response before getting to the escape character EVU3.10
        
        #if this is false than move on to the next part of the response        
        if self.__serialConn.read() != ESCAPE:

            #just read until the 0 of the EVU3.10 response
            self.read_until('0', 4, False)
            
            #after reading that weird response,i check if there is an ESCAPE character
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.SetCoercivityError("SETTING THE DEVICE TO LOW-CO "
                                                            "ERROR, looking for ESCAPE(\x1B)", "low")
        

        
        if self.__serialConn.read() != b'0':
            raise cardReaderExceptions.SetCoercivityError("SETTING THE DEVICE TO LOW-CO ERROR, "
                                                            "looking for 0(\x30), Device might have "
                                                            "not been set to Low-Co", "low")
        
        print ("SUCCESSFULLY SET THE MSR605 TO LOW-COERCIVITY")
        
        return None
    
    def get_hi_or_low_co(self):
        """This command is to get MSR605 write status, is it in Hi/Low Co
        
        Hi-Coercivity (Hi-Co) is just one kind of magstripe card, the other
        being Low-Coercivity (Low-Co), google for more info
    
        Args:
            None
            
        Returns:
            A String that contains what mode the MSR605 card reader/writer is in
            
            ex:            
                HI-CO
                LOW-CO
    
        Raises:
            GetCoercivityError: An error occurred when setting the coercivity 
        """
    
        print ("\nGETTING THE MSR60 COERCIVITY (HI OR LOW)")
    
        #command code for getting the MSR605 Coercivity
        self.__serialConn.write(ESCAPE + HI_OR_LOW_CO)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        #for some reason i get this response before getting to the escape character EVU3.10
        
        #if this is false than move on to the next part of the response                
        if self.__serialConn.read() != ESCAPE:
            
            #just read until the 0 of the EVU3.10 response        
            self.read_until('0', 4, False)
            
            #after reading that weird response,i check if there is an ESCAPE character
            if self.__serialConn.read() != ESCAPE:
                raise cardReaderExceptions.GetCoercivityError("HI-CO OR LOW-CO ERROR, looking"
                                                              "for ESCAPE(\x1B)")
        
        
        coMode = self.__serialConn.read()
        
        if coMode == b'h':
            print ("COERCIVITY: HI-CO")
            return "HI-CO"
        
        elif coMode == b'l':
            print ("COERCIVITY: LOW-CO")
            return "LOW-CO"
        
        else:
            raise cardReaderExceptions.GetCoercivityError("HI-CO OR LOW-CO ERROR, looking for H(\x48) "
                                                "or L(\x4C), don't know if its in superposition "
                                                "or what lol")


    # ***************************************************
    #
    #     Data Processing (lol idk what to call these)
    #
    # ***************************************************
    
    def read_until(self, endCharacter, trackNum, compareToISO):
        """This reads from the serial COM port and continues to read until it reaches
            the end character (endCharacter)

    
        Args:
            endCharacter: this is character (like a delimiter), the function returns all
                            the data up to this character, ex: ESCAPE, 's'
                            
                            
            trackNum: this is an integer between 1 and 3, the # represents a track #, it
                        is used to check if the track data fits the ISO standard, it is
                        sorta canonicalized, used in the iso_standard_track_check function
            
            compareToISO: this is a boolean that if True will use the trackNum provided and
                            compare the data provided with the ISO Standard for Magnetic Strip
                            cards, if False the ISO Standard check will not be run
                        
    
        Returns:
            A string that contains all the data of a track upto a certain character
            
            ex of track #1:
                A1234568^John Snow^           0123,
            
        Raises:
            Nothing
        """
        
        #counter
        i = 0
        
        #track 3 can contain more characters than track 1 or 2, it being 107 characters
        #this is just a small check, doesn't need to be there but i thought might as well
        #conform to the ISO standard and make sure we don't have an infinite loop
        if (trackNum == 1):
            cond = 79
        elif (trackNum == 2):
            cond = 40
        else:
            cond = 107
        
        string = ""
       
        while (i < cond): 
            strCompare = self.__serialConn.read()
            str = strCompare.decode()
            
            #only runs the ISO checks if required
            if (compareToISO):
                #checks if the track data is valid based on the track data 
                if not (strCompare == ESCAPE or strCompare == FILE_SEPERATOR or strCompare == ACKNOWLEDGE or                    
                        strCompare == START_OF_HEADING or strCompare == START_OF_TEXT or strCompare == END_OF_TEXT ):
                    
                    if (iso_standard_track_check(str,trackNum) == False):
                        continue
            
            #if the special End of Line character is read, usually is the control character (ex: ESCAPE)
            
            if (isinstance(endCharacter, bytes)):                
                if (str == endCharacter.decode()):
                    return string
                
            else:                
                if (str == endCharacter):
                    return string
            
            if (strCompare != ESCAPE):
                string += str #keeps accumlating the track data
                
            i += 1
            
        #some cards i tried didn't follow the format/standard they were suppposed to, so rather than
        #adding special cases, i just return the data
        return string
    
        
    def status_read(self):
        """This reads the Status Byte of the response from the MSR605

    
        Args:
           None
           
        Returns:
           Nothing
    
        Raises:
            StatusError: An error occurred when the MSR605 was performing the function you
                            requested
        """
        
        #reads in the Status Byte
        status = (self.__serialConn.read()).decode()
        print ("STATUS: " , status)
        #checks what the stauts byte coorelates with, based off of the info provided from the
        #MSR605  programming manual
        if (status == '0'):
            print ("CARD SUCCESSFULLY READ")
        
        elif (status == '1'):
            print ("[Datablock] Error: 1(0x30h), 'Error, Write, or read error'")
            raise cardReaderExceptions.StatusError("[Datablock] Error, 'Error, Write, or read error'", 1)
        
        elif (status == '2'):
            print ("[Datablock] Error: 2(0x32h), 'Command format error'")
            raise cardReaderExceptions.StatusError("[Datablock] Error, 'Command format error'", 2)
        
        elif (status == '4'):
            print ("[Datablock] Error: 4(0x34h), 'Invalid command'")
            raise cardReaderExceptions.StatusError("[Datablock] Error, 'Invalid command'", 4)
    
        elif (status == '9'):
            print ("[Datablock] Error: 9(0x39h), 'Invalid card swipe when in write MODE'")
            raise cardReaderExceptions.StatusError("[Datablock] Error, 'Invalid card swipe when in write "
                                                    "mode'", 9)
            
        else: 
            print ("UNKNOWN STATUS: " + status)
            
        return None
    
    
    # ***********************
    #
    #     Setter/Getters
    #
    # ***********************
    
       
    def get_device_model(self):
        """This command is used to get the model of MSR605.
       
        Args:
            None
    
        Returns:
            A string that contains the device model
            
            ex: 3
            
        Raises:
            GetDeviceModelError: An error occurred when obtaining the device model
        """
        
        print ("\nGETTING THE DEVICE MODEL")
    
        #command code for getting the device model
        self.__serialConn.write(ESCAPE + DEVICE_MODEL)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.GetDeviceModelError("GETTING DEVICE MODEL ERROR, looking "
                                                 "for ESCAPE(\x1B)")
        
        model = (self.__serialConn.read()).decode()
        print ("MODEL: " + model)
        
        if self.__serialConn.read() != b'S':
            raise cardReaderExceptions.GetDeviceModelError("GETTING DEVICE MODEL ERROR, looking for "
                                                            "S(\x53), check the response, the model "
                                                            "might be right")
        
        print ("SUCCESSFULLY RETRIEVED THE DEVICE MODEL")
        
        return model
    
    def get_firmware_version(self):
        """This command can get the firmware version of MSR605.
    
        Args:
            None
    
        Returns:
            A string that contains the firmware version
            
            ex: R
            
    
        Raises:
            GetFirmwareVersionError: An error occurred when getting the MSR605 firmware \
                                        version
        """
    
        print ("\nGETTING THE FIRMWARE VERSION OF THE MSR605")
    
        #command code for getting the firmware version of the MSR605
        self.__serialConn.write(ESCAPE + FIRMWARE)
        self.__serialConn.flush()
        
        #response/output from the MSR605
        if self.__serialConn.read() != ESCAPE:
            raise cardReaderExceptions.GetFirmwareVersionError("GETTING FIRMWARE VERSION ERROR, "
                                                    "looking for ESCAPE(\x1B)")
        
        firmware = (self.__serialConn.read()).decode()
        
        print ("FIRMWARE: " + firmware)
        
        print ("SUCCESSFULLY RETRIEVED THE FIRMWARE VERSION")
        return firmware
    
    
    def getSerialConn(self):
        return self.__serialConn
    
    def setSerialConn(self, serialConn):
        self.__serialConn = serialConn