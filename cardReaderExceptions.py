#!/usr/bin/env python3

""" cardReaderExceptions.py
    
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

    Description: This contains custom exception classes for the cardReader interface 
    
                Could've combined some exceptions but I did some research and found it's
                better to not use generic exceptions, but i might be interpreting that wrong.
                
                I'll keep the docstrings out of this class cause I think its fairly simple to
                understand 
"""

class MSR605ConnectError(Exception):
    def __init__(self, arg):
        super(MSR605ConnectError, self).__init__(arg)
        
class CardReadError(Exception):
    #also stores the tracks so some card track data is provided if this error occurs
    def __init__(self, arg, tracks): 
        super(CardReadError, self).__init__(arg)
        self.tracks = tracks
        
class CardWriteError(Exception):
    def __init__(self, arg):
        super(CardWriteError, self).__init__(arg)
                
class EraseCardError(Exception):
    def __init__(self, arg):
        super(EraseCardError, self).__init__(arg)
        
class StatusError(Exception):
    #also stores the error number from the status, which is important in finding out what went wrong
    def __init__(self, arg, errorNum):
        super(StatusError, self).__init__(arg)
        self.errorNum = errorNum

class CommunicationTestError(Exception):
    def __init__(self, arg):
        super(CommunicationTestError, self).__init__(arg)
        
class SensorTestError(Exception):
    def __init__(self, arg):
        super(SensorTestError, self).__init__(arg)
        
class RamTestError(Exception):
    def __init__(self, arg):
        super(RamTestError, self).__init__(arg)

class GetDeviceModelError(Exception):
    def __init__(self, arg):
        super(GetDeviceModelError, self).__init__(arg)
        
class GetFirmwareVersionError(Exception):
    def __init__(self, arg):
        super(GetFirmwareVersionError, self).__init__(arg)
        
class SetCoercivityError(Exception):
    #also stores the coercivity, since this is a little more generic than the the other exceptions
    def __init__(self, arg, coercivity):
        super(SetCoercivityError, self).__init__(arg)
        self.coercivity = coercivity #hi or low coercivity
        
class GetCoercivityError(Exception):
    def __init__(self, arg):
        super(GetCoercivityError, self).__init__(arg)