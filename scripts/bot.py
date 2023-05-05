import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException,WebDriverException
import time
import json
import logging
import requests
import zipfile,os,subprocess
from scripts.dbHandeler import DBhandeler

Url = "https://meroshare.cdsc.com.np/#/login"


logger = logging.getLogger(__name__)

class Browser():
    def __init__(self) -> None:
        
        # Read browser to use:
        with open ("data/config.json","r") as read:
            data= json.load(read)
        read.close()
        
        # Chrome
        chromePath = data['chromedriverpath']

        try:

            self.driver = webdriver.Chrome(executable_path= chromePath)
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(Url)
            logger.info("Bot using Chrome browser.")
        
        except WebDriverException :
                # return web driver not working update
                logger.warning("Check This.")
                
                print("sadasdasd2")
        except Exception as e:
            logger.error("Exception raised while trying to open Chrome, with exception :\n\t{e}".format(e=e))
            
        return

    def run(self,nickname):
        data = DBhandeler().fetchdata(nickname=nickname)
        
        self.dpcode = data["dp_code"][3:8]
        self.username = data["dp_code"][8:]
        self.password = data["password"]
        self.units = data["units"]
        self.crn=data["crn_no"]
        self.pin = data["tran_pin"]
        
        logger.info("Applying for account with Nickname : {}".format(nickname))        
        
        # check if browser driver is working
        check_driver = self.checkDriver()
        if check_driver[0] == False :
            self.driver.quit()
            logger.info("Falied!, Browser Quit.")
            return [False,check_driver[1]]

        enter_dp_code = self.enterDpCode()
        if enter_dp_code[0] == False:
            self.driver.quit()
            logger.info("Falied!, Browser Quit.")
            return [False,enter_dp_code[1]]
        
        enter_username = self.enterUsername()
        if enter_username[0] == False:
            self.driver.quit()
            logger.info("Failed!, Browser Quit.")
            return [False,enter_username[1]]

        enter_password = self.enterPassword() 
        if  enter_password[0]== False:
            self.driver.quit()
            logger.info("Failed!, Browser Quit.")
            return [False,enter_password[1]]

        login = self.login() 
        if  login[0] == False:
            self.driver.quit()
            logger.info("Failed!, Browser Quit.")
            return [False,login[1]]

        move_to_asba = self.moveToAsba() 
        if  move_to_asba[0] == False:
            logger.info("Failed!, Browser Quit.")
            self.driver.quit()
            return [False,move_to_asba[1]]

        apply = self.apply() 
        if  apply[0] == False:
            logger.info("Failed!, Browser Quit.")
            self.driver.quit()
            return [False,apply[1]]
        logger.info("Success!, Browser Quit.")
        self.driver.quit()
        return [True,None]

    def checkDriver(self):
        """
            Checks wheather the driver is working or not. 
            Returns [True,None] if driver is working and returns [False, "error_code"] if any error occured.
        """
        
        try:
            self.driver.refresh()
        except WebDriverException:
            logger.error("Chrome web driver not working.")
            return [False,"0x0003"]
        except Exception as e:
            logger.error(f"Chrome web driver not working. With Exception :\n\t {e}")
            return [False,"0x0004"]
        logger.info("Browser checked.")

        return [True,None]

    def enterDpCode(self):
        # Selecting Demat provider.
        try:
            dp_code = self.driver.find_element(By.ID,"selectBranch")
            dp_code.click()
        
        except Exception as e:
            logger.error("Exception raised while clicking Demat provider tray, with exception :\n\t{e}".format(e=e))
            return [False,"0x000c"]
        
        try :
            dp_code_send = self.driver.find_element(By.CLASS_NAME,"select2-search__field")
            dp_code_send.send_keys(self.dpcode)
            dp_code_send.send_keys(Keys.RETURN)
        except Exception as e:
            logger.error("Exception raised while entering Demat provider code, with exception :\n\t{e}".format(e=e))
            return [False,"0x000c"]
        logger.info("Demat Provider selected.")
        return [True,None]

    def enterUsername(self):
        try:
            username = self.driver.find_element(By.ID,"username")
            username.send_keys(self.username)
        except Exception as e:
            logger.error("Exception raised while entering username, with exception :\n\t{e}".format(e=e))
            return [False,"0x000c"]
        logger.info("Username entered.")
        return [True,None]

    def enterPassword(self):
        try:
            password = self.driver.find_element(By.ID,"password")
            password.send_keys(self.password)
        except Exception as e:
            logger.error("Exception raised while entering password, with exception :\n\t{e}".format(e=e))
            return [False,"0x000c"]
        logger.info("Password entered.")
        return [True,None]

    def login(self):
        try:
            self.driver.implicitly_wait(10)
            login = self.driver.find_element(By.CLASS_NAME,"sign-in")
            login.click()
        except Exception as e:
            logger.error("Exception raised while clicking login button, with exception :\n\t{e}".format(e=e))
            return [False,"0x000c"]
        
        # check for toast message 
        try :
            message = self.driver.find_element(By.CLASS_NAME,"toast-message").get_attribute("innerHTML")
            message = message.replace("  ",'')
            message = message.replace("\n",'')
            message = (message.split('.'))[0]
            logger.warning(f"Toast message found after login : \n{message}")
            if message == "Invalid password":
                logger.warning("Password wrong for user : {u}".format(u=(str(self.dpcode)+str(self.username))))
                # return false for wrong password 
                return [False,"0x0001"]
            if message == "User is not authorized":
                logger.warning("User is not authorized error occured. Try again.")
                 
                return [False,"0x0002"]
        except:
            logger.info("No toast message found after login.")
            pass
        logger.info("Logged In.")
        return [True,None]

    def moveToAsba(self):
        # Checking browser window size for reactive nav tab
        width = self.driver.get_window_size()
        width = float(width['width'])

        if width > 992 : # landscape mode
            logger.info("Landscape mode on.")
            try:
                myAsbaBtn = self.driver.find_element(By.XPATH,"/html/body/app-dashboard/div/div[1]/nav/ul/li[8]/a")
                myAsbaBtn.click()
            except Exception as e:
                logger.error("Exception raised while moving to my asba page, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]
        else : # potrait mode
            logger.info("Potrait mode on.")
            
            # could find the element because of window width small.
            # now clicking sidebar minimizer first then hyper link
            try:
                sidebarMaximizer = self.driver.find_element(By.CLASS_NAME,"sidebar-minimizer")
                sidebarMaximizer.click()
                myAsbaBtn = self.driver.find_element(By.XPATH,"/html/body/app-dashboard/div/div[1]/nav/ul/li[8]/a")
                myAsbaBtn.click()
            except Exception as e:
                logger.error("Exception raised while finding sidebar minimizer, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]
            
        
        

        logger.info("Moved to My ASBA page.")
        
        return [True,None]

    def apply(self):
        # finding the parent element where companies are present.
        try:
            companyList = self.driver.find_elements(By.CLASS_NAME,"company-list")
        except Exception as e:
            logger.error("Exception raised while finding list of applicable company, with exception :\n\t{e}".format(e=e))

        
        # for (child) company in lists of companies
        for num in range(0,len(companyList)):
            # first parent is used for finding outs its child and second is for interacting with them
            companyList = self.driver.find_elements(By.CLASS_NAME,"company-list")

            self.driver.implicitly_wait(10)
            
            # checking type of apply for issue
            stockType = companyList[num].find_element(By.CLASS_NAME,"isin").get_attribute("innerHTML")
            stockType = str(stockType)
            stockType = stockType.replace("\n","")
            stockType = stockType.replace("  ","")
            stockType = stockType.replace(" ","")
            stockType = (stockType.split)("<")[0]

            
            # if the share type is not ipo or fpo continue with other company if any.
            if stockType not in ["OrdinaryShares"] :
                continue


            try:
                applyBtn = companyList[num].find_element(By.CLASS_NAME,"btn-issue")
            except NoSuchElementException:
                logger.warning("Apply button couldn't be found.")
                # This occurs when ipo already applied and been verified
                continue
            except Exception as e:
                logger.error("Exception raised while finding apply button, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]
            
            # Checking if the issue is already applied
            checkApplied = str(applyBtn.get_attribute("innerHTML"))
            checkApplied = checkApplied.split(">")
            checkApplied = checkApplied[1].split("<")
            checkApplied = checkApplied[0]

            if checkApplied == "Edit":
                continue  
        
            # apply if alredy not applied
            applyBtn.click()
            
            # select bank
            try:
                selectBankOPT = self.driver.find_element(By.ID,"selectBank")
                selectBankOPT.click()
                self.driver.implicitly_wait(10)
                selectBank = self.driver.find_element(By.XPATH,"/html/body/app-dashboard/div/main/div/app-issue/div/wizard/div/wizard-step[1]/form/div[2]/div/div[4]/div/div[2]/div/div/div[2]/div/select/option[2]")
                selectBank.click()
            except Exception as e:
                logger.error("Exception raised while selecting bank, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]

            # enter units
            try:
                applyKitta = self.driver.find_element(By.ID,"appliedKitta")
                applyKitta.send_keys(self.units)
            except Exception as e:
                logger.error("Exception raised while entering units, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]
            
            # enter crn
            try:
                crn = self.driver.find_element(By.ID,"crnNumber")
                crn.send_keys(self.crn)
            except Exception as e:
                logger.error("Exception raised while entering CRN number, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]

            # accept terms
            try:
                terms = self.driver.find_element(By.ID,"disclaimer")
                terms.click()
            except Exception as e:
                logger.error("Exception raised while accepting terms, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]

            # proceed to pin
            try:
                proceed = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[1]/form/div[2]/div/div[5]/div[2]/div/button[1]')
                proceed.click()
            except Exception as e:
                logger.error("Exception raised while proceeding to pin, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]
            
            self.driver.implicitly_wait(20)

            # entering transaction pin
            try:
                transactionPin = self.driver.find_element(By.ID,"transactionPIN")
                transactionPin.send_keys(self.pin)
            except Exception as e:
                logger.error("Exception raised while entering pin, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]

            # submit issues request
            try:
                submit = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[2]/div[2]/div/form/div[2]/div/div/div/button[1]')
                submit.click()
            except Exception as e:
                logger.error("Exception raised while submiting issue request, with exception :\n\t{e}".format(e=e))
                return [False,"0x000c"]
            continue
        time.sleep(5)
        logger.info("Applied !")
        return [True,None]

    def checkPassword(self,dpcode,password):
        
        self.dpcode = dpcode[3:8]
        self.username = dpcode[8:]
        self.password = password

        if self.checkDriver() == False:
            self.driver.quit()
            return [False,None]

        if self.enterDpCode() == False:
            self.driver.quit()
            return [False,None]

        if self.enterUsername() == False:
            self.driver.quit()
            return [False,None]

        if self.enterPassword() == False:
            self.driver.quit()
            return [False,None]

        
        login_check = self.login()
        if login_check[0] == False:
            self.driver.quit()
            return [False,login_check[1]]

        self.driver.quit()
        return [True,None]

    def updateDriver(self):

        chrome_browser_version=(self.driver.capabilities['browserVersion'].split("."))[0]
        self.driver.quit()
        latest_driver_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}"

        latest_driver_release_version = requests.get(latest_driver_release_url.format(chrome_browser_version)).text
        print(latest_driver_release_version)
        download_url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(latest_driver_release_version)


        # download new driver zip file 
        filename = "./chromedriver_win32.zip"
        subprocess.run(["curl", "-o", filename, download_url])

        # remove old chrome driver if exists
        try:
            os.remove("./lib/driver/chromedriver.exe")
        except: 
            pass
        
        extract_to = "./lib/driver/"
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    

        os.remove(filename)

        return True
