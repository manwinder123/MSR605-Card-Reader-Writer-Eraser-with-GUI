  **MSR605 Card Reader python interface and GUI**

  -------------------------
  Edited: 25  August 2017
  -----------------------
  Author: Manwinder Sidhu
  --------------------------------
  Contact: manwindersapps@gmail.com
  --------------------------------
  Platform: Windows
  ---------------------------------------------------------------------------------------------
  Python: 3.5.2 (I originally wrote this in 2.7 but I think I had issues with Tkinter)
  -------------------------------------------------------------------
  Legal Documentation: LICENSE (file) and also in some of the classes

  ------------------  
  Libraries Required
  ------------------
  PySerial for communication between the PC and MSR605 (https://github.com/pyserial/pyserial)
  
  Tkinter for the GUI
  

  --------------------
  Hardware Description
  --------------------
  The MSR605 is a card reader/writer, its writes to the standard magstripe cards
  that most people are used to using (Credit Cards, Debit Cards, pretty much any
  card with a colored stripe on the back, its usually black). I purchased mine
  on ebay. I choose to buy this card reader because it had good documentation
  online


  -------------------
  Project Description
  -------------------
  So there are a few MSR605 projects online and there is a great programmer manual
  for the device (https://www.triades.net/downloads/MSR605%20Programmer's%20Manual.pdf).
  The only reason I actually created this project was because my parents wanted a points
  card at their business and I didn't want them to spend a large amount of money on it. I
  did successfully create the application and it has been working great for a few years now.
  I started this project in April 2015 and had thought it was ready to go but it had a few bugs
  and I left for work in May 2015 and wasn't able to access the device. I finished it in late
  August 2015 and thought I'd throw it on github cause the MSR605 projects I seen didn't have a
  GUI included with them. A nice GUI comes with the MSR605 device I got but all it does is
  read, write and erase cards.
    
  So the files you guys will have will read, write and erase cards. There are also some other
  things it can do such as diagnostic tests on the device as well as lighting up the LED's. The
  cards can be stored in a database, I added this functionality cause I assumed anybody using this
  project would most likely want to store their cards.
  
  You can take the backend and use it to build your own GUI, you can take what I have and modify it.
  
  Just as an example for a points card, you could generate one or all of the tracks randomly, store
  those values in the database, hash and salt the generated values and put those generated values on
  the tracks (most magstripe cards have 3 tracks).
  
  The Magstripe card tracks have an ISO Standard that you can follow if you want too. I have included a
  isoStandardDictionary class that contains a dictionary with all the allowed characters for each of the
  tracks.
  
  I haven't implemented all the functionality that is in the programmers manual, such as raw read and raw
  write. I did not implement this because I was able to cover all the core functionality I needed and thought
  others would need. If you desire this functionality I can add it but it should not be too hard to implement
  yourself after reading the programmers manual

  
  ----------------
  File Description
  ----------------
  GUI.py - the graphical interface that allows you to control the MSR605
  
  MSR605Test.py - this tests the devices different functions, it's pretty much tests all the functions that
                  the device can perform

  cardReader.py - the interface between python and the MSR605, this class sends the command over serial and
                  returns any info requested
                  
  isoStandardDictionary.py - contains 2 dictionaries (track 2 and 3 have the same standard for what characters
                             are allowed) and a function that tells you if a character is valid for a given track
                             
                             
  cardReaderExceptions.py - The MSR605 provides feed back in the case errors arise, this information can be useful
                            and this class contains exceptions for each of the functions the MSR605 can preform



  ----
  Bugs
  ----
  
  
