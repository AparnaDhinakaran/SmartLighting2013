import Tkinter as tk
import tkFont
import time

from time import mktime, localtime, gmtime, strftime
from Tkinter import *
from PIL import Image, ImageTk
from subprocess import call

class Meter(tk.Frame):
    def __init__(self, master, width=300, height=20, bg='white', fillcolor='orchid1',value=0.0, text=None, font=None, textcolor='black', *args, **kw):
        tk.Frame.__init__(self, master, bg=bg, width=width, height=height, *args, **kw)
        self._value = value
        self._canv = tk.Canvas(self, bg=self['bg'], width=self['width'], height=self['height'],highlightthickness=0, relief='flat', bd=0)
        self._canv.pack(fill='both', expand=1)
        self._rect = self._canv.create_rectangle(0, 0, 0, self._canv.winfo_reqheight(), fill=fillcolor, width=0)
        self._text = self._canv.create_text(self._canv.winfo_reqwidth()/2, self._canv.winfo_reqheight()/2,text='', fill=textcolor)
        if font:
            self._canv.itemconfigure(self._text, font=font)
            self.set(value, text)
            self.bind('<Configure>', self._update_coords)
    
    def _update_coords(self, event):
        '''Updates the position of the text and rectangle inside the canvas when the size of
            the widget gets changed.'''
        # looks like we have to call update_idletasks() twice to make sure
        # to get the results we expect
        self._canv.update_idletasks()
        self._canv.coords(self._text, self._canv.winfo_width()/2, self._canv.winfo_height()/2)
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*self._value, self._canv.winfo_height())
        self._canv.update_idletasks()
        
    def get(self):
        return self._value, self._canv.itemcget(self._text, 'text')
    
    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        self._value = value
        if text == None:
            #if no text is specified use the default percentage string:
            text = str(int(round(100 * value))) + ' %'
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*value, self._canv.winfo_height())
        self._canv.itemconfigure(self._text, text=text)
        self._canv.update_idletasks()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # Set initial page to 1
        self.page = 1
        # Boolean keeping track of entering sensor ID loop
        self.loop = True 
        # Path for image on first page
        self.imgPath = './moel.gif'
        # Font for 'SmartLighting2013 title text'
        self.titleFont = tkFont.Font(family="Times", size=36, weight="bold", \
            slant="italic")
        # Font for regular text
        self.textFont = tkFont.Font(family="Helvetica", size=14)
        # Variable to store entry box text (Sensor #, etc.)
        self.entryText = StringVar()
        # List of light sensor names
        self.sensors = []
        # Current date in unixtime
        self.currentDate = ""
        # Create Layout for Page 1
        self.columnconfigure(0, minsize="350")
        self.columnconfigure(1, minsize="120")
        self.columnconfigure(2, minsize="120")
        self.rowconfigure(0, minsize="120", pad="20")
        self.rowconfigure(1, minsize="50")
        self.rowconfigure(2, minsize="60")
        self.rowconfigure(3, minsize="150", pad="20")
        # Create application window
        self.grid()
        # Create widgets for first page
        self.titlePage()
    
    def make_unix_timestamp(date_string, time_string):
        """This command converts string format of date into unix timstamps."""
        format = '%Y %m %d %H %M %S'
        return time.mktime(time.strptime(date_string + " " + time_string, format))

    def demo(self, meter, value):
        meter.set(value)
        if value < 1.0:
            value = value + 0.005 
            meter.after(50, lambda: self.demo(meter, value))
        else:
            meter.set(value, 'Demo successfully finished')

    def titlePage(self):
        # Create the SmartLighting2013 title
        self.title = tk.Label(self, text = "SmartLighting2013", font = self.titleFont)
        self.title.grid(column = 0, row = 0, columnspan = 3, ipadx = "20", \
                ipady="10", sticky=tk.W)
        # Add photo image to first page
        #self.img = ImageTk.PhotoImage(Image.open(self.imgPath))
        #self.image = tk.Label(self, image = self.img)
        #self.image.grid(column = 0, row = 1, columnspan=3, rowspan=1, sticky=tk.N)
        # Add text widget
        self.text = tk.Label(self, text = "The SmartLighting Installation wizard " + \
            "will step through the software installation and light sensor set-up. " + \
            "Please click 'Next' to continue.", wraplength = "450", justify = LEFT, \
            anchor = W, font=self.textFont) 
        self.text.grid(column=0, row=1, columnspan=3, rowspan=2, ipady=".5i")
        # Create the 'Cancel' button, which exits the application when pressed
        # Doubles as the 'Finish' button on the last page
        self.quitButton = tk.Button(self, text='Cancel', command=self.quit)
        # Create the 'Next' button, which calls self.next() and takes user to next page
        # Doubles as the 'Next Sensor' button
        self.nextButton = tk.Button(self, text = 'Next', command = self.next)
        # Create the 'Last Sensor' button, which indicates that user is finished inputting light sensors
        self.finishButton = tk.Button(self, text = 'Finish', command = self.lastSensor)
        self.nextButton.grid(column=1, row=3)
        self.quitButton.grid(column=2, row=3)
        # Increment page count (needed in self.next method)

    def tinyOSInstallPage(self):
        #self.image.grid_forget()
        self.nextButton.config(state='disabled')
        self.text['text'] = "Please wait while the wizard installs TinyOS software"
        self.text.grid(row=1, column=0, columnspan=3, rowspan=2)
        self.m = Meter(self, relief='ridge', bd=3)
        self.m.grid(row=2, column=0, columnspan=3)
        self.m.set(0.0, 'Starting demo...')
        self.m.after(10, lambda: self.demo(self.m, 0.0))
        # Call backend function here!
        #self.installTinyOS()
        self.nextButton.config(state='normal')

    def smapFolderPage(self):
        self.m.grid_forget()
        self.text['text'] = "Enter a name for your sMAP data folder:"
        self.text.grid(column=0, row=1, columnspan=3, rowspan=2)
        self.entry = tk.Entry(self, cursor="xterm", exportselection=0, \
            textvariable=self.entryText)
        self.entry.grid(column=0, row=2, columnspan=3)

    def smapInstallPage(self):
        self.entry.grid_forget()
        self.text['text'] = "Please wait while the wizard sets up sMAP."
        self.text.grid(row=1, column=0, columnspan=3, rowspan=2)
        self.m = Meter(self, relief='ridge', bd=3)
        self.m.grid(row=2, column=0, columnspan=3)
        self.m.set(0.0, 'Starting demo...')
        self.m.after(10, lambda: self.demo(self.m, 0.0))
        # Call backend function here!
        #self.installSmap()
        #If successful, change text to: "sMAP successfully installed."

    def datePage(self):
        self.text['text'] = "Please enter the current date (Ex: MM/DD/YYYY)"
        self.entry.grid(column=0, row=2, columnspan=3)

    def sensorPlugPage(self):
        self.text['text'] = "Pick a light sensor and put two batteries in it"
        self.text2 = tk.Label(self, text = "Plug the light sensor into a USB port." +\
            " Click 'Next' when you are finished.", wraplength = "450", justify = LEFT, \
            anchor = W, font=self.textFont) 
        self.text2.grid(column=0, row=3, columnspan=3)

    def sensorIDPage(self):
        self.m.grid_forget()
        self.text2.grid_forget()
        self.text['text'] = "Please input the sensor ID of the sensor plugged into " + \
                "your computer. (Ex: '1', '4', etc.)."
        self.entry.grid(column=0, row=2, columnspan=3)

    def sensorConfigurePage(self):
        self.entry.grid_forget()
        self.text['text'] = "Please wait while we configure the light sensor" 
        self.text.grid(row=1, column=0, columnspan=3)
        self.m = Meter(self, relief='ridge', bd=3)
        self.m.grid(row=2, column=0, columnspan=3)
        self.m.set(0.0, 'Starting demo...')
        self.m.after(10, lambda: self.demo(self.m, 0.0))
        self.configureSensor()
        #If successful, change text to: "Light sensor successfully installed"
        self.text['text'] = "Light sensor 4 successfully installed"

    def congratzPage(self):
        self.m.grid_forget()
        self.text['text'] = "Congratulations! You have successfully installed " + \
            "SmartLighting. Click 'Finish' to exit the installation wizard."
        self.quitButton['text'] = "Finish"
        #If successful, change text to: "Light sensor successfully installed"

    def next(self):
        # Set the correct page number
        if self.loop == True and self.page == 9:
            self.page = 7 
        else:
            self.page += 1
        self.generatePage()

    def lastSensor(self):
        self.loop = False 
        self.next()

    def generatePage(self):
        if self.page == 2:
            self.tinyOSInstallPage()
        elif self.page == 3:
            self.smapFolderPage()
        elif self.page == 4:
            self.smapInstallPage()
        elif self.page == 5:
            self.datePage()
        elif self.page == 6:
            self.sensorPlugPage()
        elif self.page == 7:
            self.sensorIDPage()
        elif self.page == 8:
            self.sensorConfigurePage()
        elif self.page == 9:
            self.congratzPage()

    def installTinyOS(self):
        #run terminal command here
        call(["ls"])
        call(["sh", "tinyos_install.sh"])

    def installSmap(self):
        folderName = self.entryText.get()
        print folderName
        #run terminal commands here
        call(["ls"])
        call(["sh", "smap_install.sh"])

    def configureSensor(self):
        sensorNum = self.entryText.get()
        print sensorNum
        self.sensors.append("light" + str(sensorNum))
        #run terminal commands here


app = Application()
app.master.title('Smart Lighting')
app.mainloop()
