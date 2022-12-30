import json
from tkinter import *
from tkinter import messagebox, ttk,filedialog
from PIL import Image,ImageTk
import logging
from scripts.dbHandeler import DBhandeler
from scripts.bot import Browser
import threading
#from tkinter import scrolledtext

# Config file
class Config():
    """
        This class reads and writes value of keys from config file.
    """
    def __init__(self) -> None:
        
        with open("data/config.json","r") as read:
            self.readConfig = json.load(read)

        pass

    def updateBrowser(self,value):
        # check if browser is already running
        browser = self.readRunning()
        if browser == True:
            
            logging.warning("Cannot update browser while the process is already running.")
            
            return


        self.readConfig['browser'] = value
        
        with open("data/config.json","w") as write:
            json.dump(self.readConfig,write,indent=4)
        
        logging.info("Updated Value of key : (browser) \n\t value : {}".format(value))
        return
    def readBrowser(self):
        value = self.readConfig['browser']
        logging.info("Value of key (browser) read as ({})".format(value))
        return value

    def updateDoNotShowAgain(self,value):
        
        self.readConfig['donotshowagain'] = value

        with open("data/config.json","w") as write:
            json.dump(self.readConfig,write,indent=4)
        
        logging.info("Updated Value of key : (donotshowagain) \n\t value : {}".format(value))
        return
    def readDoNotShowAgain(self):
        value = self.readConfig['donotshowagain']
        logging.info("Value of key (donotshowagain) read as ({})".format(value))
        return value

    def updateChromePath(self,value):
        # check if browser is already running
        browser = self.readRunning()
        if browser == True:
            
            logging.warning("Cannot update Chrome driver path while the process is already running.")
            
            return
        self.readConfig['chromedriverpath'] = value

        with open("data/config.json","w") as write:
            json.dump(self.readConfig,write,indent=4)
        
        logging.info("Updated Value of key : (chromedriverpath) \n\t value : {}".format(value))
        return
    def readChromePath(self):
        value = self.readConfig['chromedriverpath']
        logging.info("Value of key (chromedriverpath) read as ({})".format(value))
        return value

    def updateMozilaPath(self,value):
        # check if browser is already running
        browser = self.readRunning()
        if browser == True:
            
            logging.warning("Cannot update Mozilla driver path while the process is already running.")
            
            return
        self.readConfig['moziladriverpath'] = value

        with open("data/config.json","w") as write:
            json.dump(self.readConfig,write,indent=4)
        
        logging.info("Updated Value of key : (moziladriverpath) \n\t value : {}".format(value))
        return
    def readMozilaPath(self):
        value = self.readConfig['moziladriverpath']
        logging.info("Value of key (moziladriverpath) read as ({})".format(value))
        return value

    def updateAutoStart(self,value):
        
        self.readConfig['autoStart'] = value

        with open("data/config.json","w") as write:
            json.dump(self.readConfig,write,indent=4)
        
        logging.info("Updated Value of key : (autoStart) \n\t value : {}".format(value))
        return
    def readAutoStart(self):
        value = self.readConfig['autoStart']
        logging.info("Value of key (autoStart) read as ({})".format(value))
        return value

    def updateRunning(self,value):
        self.readConfig['running'] = value

        with open("data/config.json","w") as write:
            json.dump(self.readConfig,write,indent=4)
        
        logging.info("Updated Value of key : (running) \n\t value : {}".format(value))
        return
    def readRunning(self):
        value = self.readConfig['running']
        logging.info("Value of key (running) read as ({})".format(value))
        return value


# Root window
Root = Tk()

# Root window properties
Root.title("IPO Tool")
Root.iconbitmap("./lib/img/logo.ico")
Root.geometry("700x500")

# logging setup
if True:
    
    logging.basicConfig(level=logging.INFO,filename=f"./data/log.log",filemode="w",
                        format = """
    %(levelname)s 
    %(name)s
    Function : %(funcName)s
    Line     : %(lineno)d
    Message  : %(message)s
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx""")
    '''logging.basicConfig(level=logging.INFO,filename=f"./lib/log/{counter}.log",filemode="w",
                        format = """
    Time : %(asctime)s
    %(levelname)s 
    %(name)s
    Function Name : %(funcName)s
    Line No : %(lineno)d
    Message : %(message)s
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx""")'''

#Icons
if True: 

    AddIcon = Image.open("./lib/img/plus.ico").resize((30,30),Image.Resampling.LANCZOS)
    AddIcon = ImageTk.PhotoImage(AddIcon)
    UpdateIcon = Image.open("./lib/img/update.png").resize((30,30),Image.Resampling.LANCZOS)
    UpdateIcon = ImageTk.PhotoImage(UpdateIcon)
    CancelIcon = Image.open("./lib/img/cross.png").resize((25,25),Image.Resampling.LANCZOS)
    CancelIcon = ImageTk.PhotoImage(CancelIcon)
    OnIcon = Image.open("./lib/img/on.png").resize((70,40),Image.Resampling.LANCZOS)
    OnIcon = ImageTk.PhotoImage(OnIcon)
    OffIcon = Image.open("./lib/img/off.png").resize((70,40),Image.Resampling.LANCZOS)
    OffIcon = ImageTk.PhotoImage(OffIcon)
    DeleteIcon = Image.open("./lib/img/delete.png").resize((32,32),Image.Resampling.LANCZOS)
    DeleteIcon = ImageTk.PhotoImage(DeleteIcon)
    EditIcon = Image.open("./lib/img/edit.png").resize((32,32),Image.Resampling.LANCZOS)
    EditIcon = ImageTk.PhotoImage(EditIcon)
    StartIcon = Image.open("./lib/img/start.png").resize((125,35),Image.Resampling.LANCZOS)
    StartIcon = ImageTk.PhotoImage(StartIcon)
    MozillaIcon = Image.open("./lib/img/mozilla.png").resize((30,30),Image.Resampling.LANCZOS)
    MozillaIcon = ImageTk.PhotoImage(MozillaIcon)
    ChromeIcon = Image.open("./lib/img/chrome.png").resize((30,30),Image.Resampling.LANCZOS)
    ChromeIcon = ImageTk.PhotoImage(ChromeIcon)

# How to use this tool window
class HowToUse():
    """
        Initiats How to Use window and its widgets.
    """
    def __init__(self) -> None:
        logging.info("How To Use Window initiated.")

        self.newWindow = Toplevel(Root,bg="#FFF9A6")
        self.newWindow.title("How To Use ?")
        self.newWindow.geometry("500x500")
        self.newWindow.iconbitmap("lib/img/logo2.ico")

        self.frame = Frame(self.newWindow,bg="#FFF9A6")
        self.frame.pack(side=TOP,expand=True,fill=BOTH,pady=0)
        var = BooleanVar()
        self.checkbox = Checkbutton(self.newWindow,bg="#FFF9A6",text="Do not show again.", onvalue=True,offvalue=False,variable=var,command=lambda:Config().updateDoNotShowAgain(var.get()),font=("Times New Roman",9,"bold"))
        self.checkbox.pack(side=BOTTOM,pady=(15,30))
        self.text()
        pass

    def text(self):

        heading = Label(self.frame,text="How To Use",font=("arial",18,"bold"),bg="#FFF9A6")
        heading.pack(pady=(10,10))
    
        textboxFrame = Frame(self.frame)
        textboxFrame.pack(side=BOTTOM,fill=BOTH,expand=1,padx=10,pady=10)
        textboxFrame.pack_propagate(False)
        textbox = Text(textboxFrame,font = ("Times New Roman",15),cursor="arrow",relief=SUNKEN,bg="#ffffe0")
        textbox.pack()

        textvar = """
1. Download accurate driver for your prefered browser and replace it's path.
2. Choose your prefered browser.
3. Add meroshare accounts.
4. Click manual start.
        """

        textbox.insert(END,textvar)
        textbox.configure(state = DISABLED)

# Menu bar
class MenuBar():
    """
        Initiates menu bar and its widgets.
    """

    def __init__(self) -> None:
        logging.info("Initiated Menu bar.")
        self.menuBar = Menu(Root,tearoff=False)
        Root.config(menu=self.menuBar)
        self.howToUse()
        self.selectBrowser()
        self.exit()
        pass

    def howToUse(self):
        self.menuBar.add_command(label="How to use",command=HowToUse)
        return
        
    def selectBrowser(self):
        browserMenu = Menu(self.menuBar,tearoff=False)
        browserVar = IntVar()
        
        # Config file select
        temp = Config().readBrowser()
        if temp == 0 :
            browserVar.set(0)
        if temp == 1 :
            browserVar.set(1)
        if temp == None :
            browserVar.set(NONE)
        browserMenu.add_radiobutton(label="Chrome",variable=browserVar,value=0,command=lambda:Config().updateBrowser(browserVar.get()))
        browserMenu.add_radiobutton(label="Firefox",variable=browserVar,value=1,command=lambda:Config().updateBrowser(browserVar.get()))

        # adding update browers path hyperlink
        browserMenu.add_separator()
        browserMenu.add_command(label="Update Driver Path",command=UpdateDriverPath)
        self.menuBar.add_cascade(label="Browser",menu=browserMenu)
        return

    def exit(self):
        self.menuBar.add_command(label="Exit",command=Root.destroy)
        return

class UpdateDriverPath():
    """
        Displays update browser driver path window. Only one window can be active at a time.
    """
    def __init__(self) -> None:
        # checking if a new window is already opened or not
        windowTitle = "None"
        try:
            windowTitle = Root.winfo_children()[len(Root.winfo_children())-1].title()
        except:
            # last child widget is not a window so it doesn't have title.
            pass


        if windowTitle != "Update Driver Path":
            # Doing this to prevent many windows to be created and sit in background

            # Creating new window if it is not created previosly.
            self.newWindow = Toplevel(Root)
            self.newWindow.iconbitmap("./lib/img/driver.ico")
            self.newWindow.geometry("400x200")
            self.newWindow.title("Update Driver Path")
            self.widget()
    
    def widget(self):
        # fresh page 
        for widget in self.newWindow.winfo_children():
            widget.destroy()
        

        # fetching current driver paths
        chromePath = Config().readChromePath()
        mozilaPath = Config().readMozilaPath()
        
        # Increase window width according to path length
        longerPath = len(mozilaPath)
        if len(chromePath) > len(mozilaPath):
            longerPath = len(chromePath)

        if longerPath % 10 != 0:
            while longerPath % 10 != 0:
                longerPath += 1 

        self.newWindow.geometry(f"{400+longerPath}x200")

        # Chrome
        chromeFrame = Frame(self.newWindow,height=99)
        chromeFrame.pack(side=TOP,fill=BOTH,expand=1)

        chromeLB = Label(chromeFrame,text="Chrome Driver Path : {path}".format(path= chromePath))
        chromeLB.pack(pady=(20,5))
        chromeBTN = Button(chromeFrame,image=ChromeIcon,command=lambda: self.updateChrome(chromePath),border=0)
        chromeBTN.pack()
        
        # Splitter 
        spliterFrame = Frame(self.newWindow,height=2,bg="#000000")
        spliterFrame.pack(side=TOP,fill=X,expand=1)

        # Mozila
        mozilaFrame = Frame(self.newWindow,height=99)
        mozilaFrame.pack(side=TOP,fill=BOTH,expand=1)

        mozilaLB = Label(mozilaFrame,text="Mozila Driver Path : {path}".format(path= mozilaPath))
        mozilaLB.pack(pady=(20,5))
        mozilaBTN = Button(mozilaFrame,image=MozillaIcon,border=0,command=lambda: self.updateMozila(mozilaPath))
        mozilaBTN.pack()
        return  
        
    def updateChrome(self,currentPath):
        driver = filedialog.askopenfilename(filetypes=[('Executable File','*.exe')],initialdir=currentPath,title="Select Chrome Driver")
        Config().updateChromePath(driver)
        self.widget()
        return
    def updateMozila(self,currentPath):
        driver = filedialog.askopenfilename(filetypes=[('Executable File','*.exe')],initialdir=currentPath,title="Select Mozila Driver")
        Config().updateMozilaPath(driver)
        self.widget()        
        return

class AddWindow():
    """
        Initiates add/edit profile window and its elements. 
        Use add or update method. 
    """
    
    def __init__(self) -> None:
        # checking if a new window is already opened or not
        windowTitle = "None"
        try:
            windowTitle = Root.winfo_children()[len(Root.winfo_children())-1].title()
        except:
            # last child widget is not a window so it doesn't have title.
            pass


        if windowTitle != "Add Account":
            # Doing this to prevent many windows to be created and sit in background

            # Creating new window if it is not created previosly.
            self.newWindow = Toplevel(Root)
            self.newWindow.iconbitmap("./lib/img/plus.ico")
            self.newWindow.geometry("400x200")
      
    def add(self):
        # checking if window is created or not:
        # doing this to prevent exception in further code in condition where the new window is not created but the code tries to pack widgets inside it
        try:
            test = Label(self.newWindow,text="test")
        except:
            logging.error("Couldn't create new Add profile window. Window already exists")
            return
        
        self.newWindow.title("Add Account")
        self.widgets()
        return

    def update(self,dpCode):
        try:
            test = Label(self.newWindow,text="test")
        except:
            logging.error("Couldn't create new Edit profile window. Window already exists")
            return

        self.newWindow.title("Edit Account")
        self.updateWidgets(dpCode=dpCode)
        return

    def widgets(self):
        logging.info("Add profile window initiated.")

        # DPcode password units crn trans pin
        frame1 = Frame(self.newWindow,width=400,height=33,)
        frame1.pack()
        frame1.pack_propagate(False)
        self.dpcodeVar = StringVar()
        dpcodeLB = Label(frame1,text="Enter DP Code : ")
        dpcodeLB.pack(side=LEFT,padx=20)
        dpcodeETR = Entry(frame1,width=30,textvariable=self.dpcodeVar)
        dpcodeETR.pack(side=LEFT,padx=(20,20))

        frame2 = Frame(self.newWindow,width=400,height=33)
        frame2.pack()
        frame2.pack_propagate(False)
        self.passwordVar = StringVar()
        passwordLB = Label(frame2,text="Enter Password :")
        passwordLB.pack(side=LEFT,padx=20)
        passwordETR = Entry(frame2,width=30,textvariable=self.passwordVar)
        passwordETR.pack(side=LEFT,padx=(20,20))

        frame3 = Frame(self.newWindow,width=400,height=33)
        frame3.pack()
        frame3.pack_propagate(False)
        self.unitsVar = StringVar()
        unitsLB = Label(frame3,text="Enter Units :       ")
        unitsLB.pack(side=LEFT,padx=20)
        unitsETR = Entry(frame3,width=30,textvariable=self.unitsVar)
        unitsETR.pack(side=LEFT,padx=(20,20))

        frame4 = Frame(self.newWindow,width=400,height=33)
        frame4.pack()
        frame4.pack_propagate(False)
        self.crnVar = StringVar()
        crnLB = Label(frame4,text="Enter CRN No. : ")
        crnLB.pack(side=LEFT,padx=20)
        crnETR = Entry(frame4,width=30,textvariable=self.crnVar)
        crnETR.pack(side=LEFT,padx=(20,20))

        frame5 = Frame(self.newWindow,width=400,height=33)
        frame5.pack()
        frame5.pack_propagate(False)
        self.transPinVar = StringVar()
        transPinLB = Label(frame5,text="Enter Trans PIN :")
        transPinLB.pack(side=LEFT,padx=20)
        transPinETR = Entry(frame5,width=30,textvariable=self.transPinVar)
        transPinETR.pack(side=LEFT,padx=(20,20))

        frame6 = Frame(self.newWindow,width=400,height=33)
        frame6.pack()
        frame6.pack_propagate(False)
        # Add image 
        
        addBTN = Button(frame6,image=AddIcon,border=0,command=self.addToDB)
        addBTN.pack(side=LEFT,padx=(100,20))
        
        cancelBTN = Button(frame6,image=CancelIcon,border=0,command=self.newWindow.destroy)
        cancelBTN.pack(side=LEFT,padx=(100,100))
        return

    def updateWidgets(self,dpCode = None):
        logging.info("Edit profile window initiated.")
        
        self.prevDPCode = dpCode
        
        if dpCode != None:
            data = DBhandeler().fetchdata(dpCode=dpCode)
        

        frame1 = Frame(self.newWindow,width=400,height=33,)
        frame1.pack()
        frame1.pack_propagate(False)
        self.dpcodeVar = StringVar()
        self.dpcodeVar.set(data[0])
        dpcodeLB = Label(frame1,text="Enter DP Code : ")
        dpcodeLB.pack(side=LEFT,padx=20)
        dpcodeETR = Entry(frame1,width=30,textvariable=self.dpcodeVar)
        dpcodeETR.pack(side=LEFT,padx=(20,20))

        frame2 = Frame(self.newWindow,width=400,height=33)
        frame2.pack()
        frame2.pack_propagate(False)
        self.passwordVar = StringVar()
        self.passwordVar.set(data[1])
        passwordLB = Label(frame2,text="Enter Password :")
        passwordLB.pack(side=LEFT,padx=20)
        passwordETR = Entry(frame2,width=30,textvariable=self.passwordVar)
        passwordETR.pack(side=LEFT,padx=(20,20))

        frame3 = Frame(self.newWindow,width=400,height=33)
        frame3.pack()
        frame3.pack_propagate(False)
        self.unitsVar = StringVar()
        self.unitsVar.set(data[2])
        unitsLB = Label(frame3,text="Enter Units :       ")
        unitsLB.pack(side=LEFT,padx=20)
        unitsETR = Entry(frame3,width=30,textvariable=self.unitsVar)
        unitsETR.pack(side=LEFT,padx=(20,20))

        frame4 = Frame(self.newWindow,width=400,height=33)
        frame4.pack()
        frame4.pack_propagate(False)
        self.crnVar = StringVar()
        self.crnVar.set(data[3])
        crnLB = Label(frame4,text="Enter CRN No. : ")
        crnLB.pack(side=LEFT,padx=20)
        crnETR = Entry(frame4,width=30,textvariable=self.crnVar)
        crnETR.pack(side=LEFT,padx=(20,20))

        frame5 = Frame(self.newWindow,width=400,height=33)
        frame5.pack()
        frame5.pack_propagate(False)
        self.transPinVar = StringVar()
        self.transPinVar.set(data[4])
        transPinLB = Label(frame5,text="Enter Trans PIN :")
        transPinLB.pack(side=LEFT,padx=20)
        transPinETR = Entry(frame5,width=30,textvariable=self.transPinVar)
        transPinETR.pack(side=LEFT,padx=(20,20))

        frame6 = Frame(self.newWindow,width=400,height=33)
        frame6.pack()
        frame6.pack_propagate(False)
        # Add image 
        
        addBTN = Button(frame6,image=UpdateIcon,border=0,command=self.updateToDB)
        addBTN.pack(side=LEFT,padx=(100,20))
        
        cancelBTN = Button(frame6,image=CancelIcon,border=0,command=self.newWindow.destroy)
        cancelBTN.pack(side=LEFT,padx=(100,100))
        return

    def verify(self):
        
        #dpcode 
        try:
            dpcode = int(self.dpcodeVar.get())
        except:
            messagebox.showerror("Error !","DP Code must be number")
            return False
        if len(str(dpcode)) != 16 :
            messagebox.showerror("Error !","DP Code must be 16 digits")
            return False

        # Password 
        
        #At Least 3 Number of lowercase letters in password
        #Password Maximum Length is 15
        #Password Minimum Length is 4
        try:
            password = str(self.passwordVar.get())
        except:
            messagebox.showerror("Error !","Password Error !.")
            return False
        if len(password) > 15 or len(password) < 4:
            messagebox.showerror("Error !","Maybe you have entered the wrong password.")
            return False
        #lowercase checker
        checker = 0
        lowercase = ["a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z"]
        for letter in password:
            if letter in lowercase:
                checker += 1
                continue
        if checker < 3 :
            messagebox.showwarning("Maybe you have entered the wrong password.")
            return False

        # units
        try:
            units = int(self.unitsVar.get())
        except Exception as e:
            print(e)
            print(self.unitsVar.get())
            messagebox.showerror("Error !","Units must be number")
            return False
        if (units) > 50 :
            messagebox.showwarning("Question ?","10 kitta ni parxa ra?")
        # crn

        # trans pin
        try:
            transpin = int(self.transPinVar.get())
        except:
            messagebox.showerror("Error !","Transaction Pin must be number")
            return False
        if len(str(transpin)) != 4 :
            messagebox.showerror("Error !","Maybe you have entered the wrong pin")
            return False

        return True

    def addToDB(self):
        
        if self.verify() != True: 
            return False
        
        if self.duplicateChecker(self.dpcodeVar.get()) == False:
            messagebox.showerror("Error !","Account with same DP Code already exists !")
            return False

        DBhandeler().addUser(self.dpcodeVar.get(),self.passwordVar.get(),self.unitsVar.get(),self.crnVar.get(),self.transPinVar.get())
        messagebox.showinfo("Success !","Account added successfully !")
        self.newWindow.destroy()
        
        HomeWindow()
        return True

    def updateToDB(self):
        if self.verify() != True: 
            return False
        
        DBhandeler().editUser(self.prevDPCode,self.dpcodeVar.get(),self.passwordVar.get(),self.unitsVar.get(),self.crnVar.get(),self.transPinVar.get())
        messagebox.showinfo("Success !","Account edited successfully !")
        self.newWindow.destroy()
        HomeWindow()
        return True

    def duplicateChecker(self,dpcode):
        storedData = DBhandeler().fetchdata(all=True)

        for profile in storedData:
            if profile[0] == dpcode:
                return False
        return True

def manualRunCheck():
    # check if the proccess is already running 
    if Config().readRunning() == True:
        messagebox.showerror("Error !", "The process is already being runned.")
        return
    run = threading.Thread(target = manualRun)
    run.start()
    
    return

def manualRun():

    browser = Config().readBrowser()
    if browser == None:
        messagebox.showerror("Error !","Browser not selected !")
        return False

    Config().updateRunning(True)
        
    data = DBhandeler().fetchdata(all=True)
    for profile in data:
        dpcode = profile[0]
        password = profile[1]
        units = profile[2]
        crn = profile[3]
        transPin = profile[4]

        run = Browser().run(dpcode,password,units,crn,transPin)

        if run == "Invalid Password":
            messagebox.showwarning("Warning !","Password incorrect for user : {u}\nPlease try again.".format(u = dpcode))
            break
        if run == "Driver error":
            messagebox.showerror("Error !","Driver is not working properly. Please try updating your driver.")
            break
        if run == False:
            messagebox.showerror("Error !","Error occured please check log file. And try again later.")
            break
    
    # Showing success
    if run == True:
        messagebox.showinfo("Success !","Applied successfully.")

    Config().updateRunning(False)

    return

class HomeWindow():
    def __init__(self) -> None:
        
        # destorying all widgets in Root
        for widgets in Root.winfo_children():
            widgets.destroy()

        self.window = Frame(Root)
        self.window.config(background="#ffc9bb")
        self.window.pack(fill=BOTH,expand=1)
        self.window.pack_propagate(False)
        self.startMenu()
        self.accountWindow()

        MenuBar()

        return

    def startMenu (self):
        topWindow = Frame(self.window)
        topWindow.config(height=200)
        topWindow.pack(side=TOP,fill=X,expand=1)


        autoStartLB = Label(topWindow,text="Auto Start ")
        autoStartLB.pack(side=LEFT,padx=(200,0))

        self.on_off_BTN = Button(topWindow,command=self.changeBtnStatus,border=0)
        self.on_off_BTN.pack(side=LEFT,padx=(10,0))

        value = Config().readAutoStart()
        if value == True:
            self.on_off_BTN.config(image=OnIcon)
        if value == False:
            self.on_off_BTN.config(image=OffIcon)

        manualRunBTN = Button(topWindow,image=StartIcon,border=0,command=manualRunCheck)
        manualRunBTN.pack(side=LEFT,padx=(50,0))
        
    def changeBtnStatus(self):
        
        value = Config().readAutoStart()
        if value == True:
            Config().updateAutoStart(False)
            self.on_off_BTN.config(image = OffIcon)
            return
        Config().updateAutoStart(True)
        self.on_off_BTN.config(image = OnIcon)
        return

    def accountWindow(self):
        
        bottomWindow = Frame(self.window)
        bottomWindow.config(background="#00BFFF",height=500)
        bottomWindow.pack(side=TOP,fill=BOTH,expand=1)
        bottomWindow.pack_propagate(False)
        
        # Add accounts button
        btnFrame = Frame(bottomWindow)
        btnFrame.config(height=50,bg="#CFEE11")
        btnFrame.pack(side=TOP,fill=X,expand=1)
        btnFrame.pack_propagate(False)
        addBTN = Button(btnFrame,image=AddIcon,command=lambda: AddWindow().add(),border=0)
        addBTN.pack(side=LEFT,fill=BOTH,expand=1,anchor=W)
        # Edit accounts button
        editBTN = Button(btnFrame,image=EditIcon,command=lambda: self.editItem(),border=0)
        editBTN.pack(side=LEFT,fill=BOTH,expand=1,anchor=CENTER)
        # Delete accounts button
        delBTN = Button(btnFrame,image=DeleteIcon,command=lambda: self.deleteItem(),border=0)
        delBTN.pack(side=LEFT,fill=BOTH,expand=1,anchor=E)

        # account lists

        accountFrame = Frame(bottomWindow)
        accountFrame.config(height=450,background="#CFEED1")
        accountFrame.pack(side=TOP,fill=X,expand=1)
        accountFrame.pack_propagate(False)


        

        # Tree view for accounts list
        
        self.tree = ttk.Treeview(accountFrame,takefocus=False )
        self.tree.pack(side=LEFT,fill=BOTH,expand=1)

        # Style
        style = ttk.Style()

        # Disable resizing
        self.tree.bind('<Motion>', 'break')

        # defining columns
        self.tree["columns"] = ("dpCode","password","crn","transPin","units")
        
        self.tree.column("#0", width=0,stretch=NO)
        self.tree.column("dpCode",anchor=CENTER, width=150,minwidth=150)
        self.tree.column("password",anchor=CENTER, width=150,minwidth=150)
        self.tree.column("crn",anchor=CENTER, width=125,minwidth=125)
        self.tree.column("transPin",anchor=CENTER, width=100,minwidth=100)
        self.tree.column("units",anchor=CENTER, width=75,minwidth=75)
        
        # headings
        self.tree.heading("#0",text= "")
        self.tree.heading("dpCode",text= "DP Code")
        self.tree.heading("password",text= "Password")
        self.tree.heading("crn",text= "CRN No.")
        self.tree.heading("transPin",text= "Transaction Pin")
        self.tree.heading("units",text= "Units")

        # set odd even tag for diffrent bg
        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="#ffffe0")

        # Add data
        data = DBhandeler().fetchdata(all=True)

        tagCounter = 1
        for profile in data:

            if tagCounter % 2 != 0:
                tag = "oddrow"
            else:
                tag = "evenrow"

            tagCounter += 1

            dpcode = profile[0]
            password = profile[1]
            units = profile[2]
            crn = profile[3]
            transPin = profile[4]
            self.tree.insert(parent="",index=END,values=(dpcode,password,units,crn,transPin),tags=tag)

        # Increase row height
        style.configure("Treeview",rowheight=35)
        style.configure('.',borderwidth = 0)

    def deleteItem(self):
        
        # show error message box if any row is not selected
        try:
            selectedRecord = self.tree.selection()[0]
        except:
            messagebox.showerror("Error !", "Select an account before deleting it.")
        else:
            dpCode = (self.tree.item(selectedRecord))['values'][0]

            # delete from DB
            DBhandeler().deletUser(dpCode=dpCode)
            
            # delete from screen/ treeview
            self.tree.delete(selectedRecord)

            HomeWindow()
        return

    def editItem(self):
        
        # show error message box if any row is not selected
        try:
            selectedRecord = self.tree.selection()[0]
        except:
            messagebox.showerror("Error !", "Select an account before editing it.")
        else:
            dpCode = (self.tree.item(selectedRecord))['values'][0]
            AddWindow().update(dpCode)

            
        return

def reset():
    print("Reseted everything !")
    Config().updateBrowser(None)
    Config().updateDoNotShowAgain(False)
    Config().updateAutoStart(False)
    Config().updateChromePath("lib\driver\chromedriver.exe")
    Config().updateMozilaPath("lib\driver\geckodriver.exe")

    return


#reset()


# Starting Home Screen
HomeWindow()
# set default value of run as false
Config().updateRunning(False)
# Starting How to use window if do not show again hasn't been ticked off.
if Config().readDoNotShowAgain() !=True:
    HowToUse()
Root.mainloop()
