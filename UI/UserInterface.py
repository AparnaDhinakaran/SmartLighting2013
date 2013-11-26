"""
User Interface Outline:

Pre-install: INSTALL TKINTER!

**** SOFTWARE SETUP *****
1. Pretty Title : Smart Lighting 2013 
2. Tiny-OS Installation : "Installing Tiny-OS" Still Image (Loading Bar)
    BACKEND (terminal commands):
    > Pre-Tiny OS: Open Terminal, install nesc, install several other packages, Github Source Code, Install downloaded software
    > Tiny-OS installation: Github source code, Install software, set environment variables
    
3. Data Collection Set-Up
    Part A (sMAP):
    USER:
        1. Enter name for sMAP folder (ex: 'echeng')
    BACKEND (terminal commands):
    > Create subdirectory in sMAP for user's data collection
    > Install software on local computer
    > Install sMAP drivers
    > Pause in Installation: Run check to see if all drivers are present
    USER: IF SOMETHING MISSING, quit installation and Show error message and say try again, contact or re-install
    Part B (local database):
    BACKEND:
    > Run python Database.py to create data.db
    
    *guidelines for sMAP folder names (Ex: 'SL_echeng')
    

****** SENSOR AND BASE-STATION SET-UP *****
4. Wireless sensor Set-UP
    > USER: Interface that says put two batteries and plug each sensor into USB port
        1. Use a diagram for the sensor and batteries
    > Backend: 
    1. Check what mote the device is plugged into (telosb)
    2. make telosb install, NUMBER
    USER: User inputs sensor number (pre-numbered)
        > Prior to shipping packages, we should number the sensors.
        > WARNING message: already registered sensor (if user makes a mistake and inputs the wrong number)
        > Please unplug device (once we see the line 'Reset device...')
        > Click 'Next' button when finished installing each sensor
        > Install pre-labeled 'BASE' sensor (the base-station mote)
        > Click 'Finish' button when finished installing last sensor
    3. Room layout GUI for sensor placement
    USER:
        > Drag shapes over to window to draw a rough layout of the room
        > Drag sensor dots to window to place sensors around the room
        > WARNING message if layout does not seem ideal
            - "Try to spread sensors evenly about the room."
            - "Make sure to place atleast one sensor at the window."
        > Need to extract data for our backend -> which sensor is at the window (will be a regressor)
        
    *sensor names? set sensor ID, match sensor numbers to sMAP sensor names: put in metadata
    *chandrayee had sensor id code, map user input sensor id to metadata id number
    *user sensor input: directory name + sensor + NUM
    
    *page 13.5, confirm sensor names, numbers, etc. ALLOW CHANGES.
    
    *when naming sensors, categorize as 'WINDOW SENSOR' or 'LIGHT SENSOR' 'ARTIFICIAL LIGHT' 'WORKPLANE' (can do a dropdown menu)
    *sensor placement guidelines: if you have 10, place 3 on windows, etc.
    
    *FINAL CONFIRMATION: would you like to make any corrections??
    
        
****** WIRELESS SENSOR NETWORK SET-UP *****
5. WSN Set-Up
    > BACKEND:
        1. Run terminal commands
    > USER:
        1. Final confirmation:
            a. Total number of light sensors (do not include base): ___
    > BACKEND:
        1. Check number of light sensors with internal count
        
"""

