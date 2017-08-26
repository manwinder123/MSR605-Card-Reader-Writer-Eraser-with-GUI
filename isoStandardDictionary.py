#!/usr/bin/env python3

""" isoStandardDictionary.py
    
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

    Description: This file contains 2 dictionaries and 1 function, this is used to check if
                    track data conforms to ISO Standard for magstripe cards 
    
                The characters were obtained from this website:
                    http://www.abacus21.com/magnetic-strip-encoding-1586.html
                
"""


#1st track ISO standard character set dictionary
#i take advantage of the values and use them as return values for the
#function that checks if the track data meets the ISO standard
isoDictionaryTrackOne ={
                            ' ': True,
                            '!': True,
                            '\"': True,
                            '#': True,
                            '$': True,
                            '%': True,
                            '&': True,
                            '\'': True,
                            '(': True,
                            ')': True,
                            '*': True,
                            '+': True,
                            ',': True,
                            '-': True,
                            '.': True,
                            '/': True,
                            '0': True,
                            '1': True,
                            '2': True,
                            '3': True,
                            '4': True,
                            '5': True,
                            '6': True,
                            '7': True,
                            '8': True,
                            '9': True,
                            ':': True,
                            ';': True,
                            '<': True,
                            '=': True,
                            '>': True,
                            '?': True,
                            '@': True,
                            'A': True,
                            'B': True,
                            'C': True,
                            'D': True,
                            'E': True,
                            'F': True,
                            'G': True,
                            'H': True,
                            'I': True,
                            'J': True,
                            'K': True,
                            'L': True,
                            'M': True,
                            'N': True,
                            'O': True,
                            'P': True,
                            'Q': True,
                            'R': True,
                            'S': True,
                            'T': True,
                            'U': True,
                            'V': True,
                            'W': True,
                            'X': True,
                            'Y': True,
                            'Z': True,
                            '[': True,
                            '\\': True,
                            ']': True,
                            '^': True,
                            '_': True
                        };

#2nd and 3rd track ISO standard character set dictionary
#i take advantage of the values and use them as return values for the
#function that checks if the track data meets the ISO standard
isoDictionaryTrackTwoThree = {
                            '0': True,
                            '1': True,
                            '2': True,
                            '3': True,
                            '4': True,
                            '5': True,
                            '6': True,
                            '7': True,
                            '8': True,
                            '9': True,
                            ':': True,
                            ';': True,
                            '<': True,
                            '=': True,
                            '>': True,
                            '?': True,
                        };



    
def iso_standard_track_check(char, trackNum):
    """This checks if the character provided meets the ISO Standards for Magnetic Stripe Cards
    
        Args:
            char: this is a single character, it is from the track data and it will be
                    checked to see if if fits the ISO standard
            
        Returns:
            False: if the character provided is not in the ISO standard character set
            
            True: if the character provided is in the ISO standard character set, and also
                    it returns true if the trackNum is invalid, i do this because i don't want
                    to lose information
    
        Raises:
            Nothing
    """
    
    char = str(char)
    
    #checks the track # to find out which dictionary to use to check if the character is in the
    #ISO standard character set
    if trackNum == 1:
        return isoDictionaryTrackOne.get(char, False)
    
    elif trackNum == 2 or trackNum == 3:
        return isoDictionaryTrackTwoThree.get(char, False)
    
    #if a valid track # is not provided, just return true, no data is lost this way
    else:
        print ("ISO STANDARD CHECK, TRACK # IS INVALID, IT IS:" , trackNum)
        return true;
       