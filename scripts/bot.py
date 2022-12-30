import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException,WebDriverException
import time
import json
import logging
Url = "https://meroshare.cdsc.com.np/#/login"


logger = logging.getLogger(__name__)

class Browser():
    def __init__(self) -> None:
        
        # Read browser to use:
        with open ("data/config.json","r") as read:
            data= json.load(read)
        read.close()
        
        self.browser = data['browser']   

        if self.browser == 1 :
            #Mozilla 
            firefoxPath = data['moziladriverpath']

            try:
                self.driver = webdriver.Firefox(executable_path= firefoxPath)
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                self.driver.get(Url)
                logger.info("Bot using Mozilla Firefox browser.")
            except Exception as e :
                logger.error("Exception raised while trying to open Mozilla, with exception :\n\t{e}".format(e=e))
            return
        
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
                print("sadasdasd2")
        except Exception as e:
            logger.error("Exception raised while trying to open Chrome, with exception :\n\t{e}".format(e=e))
            
        return

    def run(self,dpcode,password,units,crn,tranPin):
        self.dpcode = dpcode[3:8]
        self.username = dpcode[8:]
        self.password = password
        self.units = units
        self.crn=crn
        self.pin = tranPin
        
        logger.info("Applying for account with DP Code : {}".format(dpcode))        
        
        # check if browser driver is working
        if self.checkDriver() == False:
            return "Driver error"

        if self.enterDpCode() == False:
            self.driver.quit()
            logger.info("Browser Quit.")
            return False

        if self.enterUsername() == False:
            self.driver.quit()
            logger.info("Browser Quit.")
            return False

        if self.enterPassword() == False:
            self.driver.quit()
            logger.info("Browser Quit.")
            return False

        if self.login() == False:
            self.driver.quit()
            logger.info("Browser Quit.")
            return "Invalid Password"

        if self.moveToAsba() == False:
            logger.info("Browser Quit.")
            self.driver.quit()
            return False

        if self.apply() == False:
            logger.info("Browser Quit.")
            self.driver.quit()
            return False
        logger.info("Success! Browser Quit.")
        self.driver.quit()
        return True

    def checkDriver(self):
        
        if self.browser == 1:
            # Check Mozila browser driver
            try:
                self.driver.refresh()
            except WebDriverException:
                logger.error("Mozila web driver not working.")
                return False
            except Exception as e:
                logger.error(f"Mozila web driver not working. With Exception :\n\t {e}")
                return False
        else:
            try:
                self.driver.refresh()
            except WebDriverException:
                logger.error("Chrome web driver not working.")
                return False
            except Exception as e:
                logger.error(f"Chrome web driver not working. With Exception :\n\t {e}")
                return False

        return True

    def enterDpCode(self):
        # Selecting Demat provider.
        try:
            dp_code = self.driver.find_element(By.ID,"selectBranch")
            dp_code.click()
        
        except Exception as e:
            logger.error("Exception raised while clicking Demat provider tray, with exception :\n\t{e}".format(e=e))
            return False
        
        try :
            dp_code_send = self.driver.find_element(By.CLASS_NAME,"select2-search__field")
            dp_code_send.send_keys(self.dpcode)
            dp_code_send.send_keys(Keys.RETURN)
        except Exception as e:
            logger.error("Exception raised while entering Demat provider code, with exception :\n\t{e}".format(e=e))
            return False
        logger.info("Demat Provider selected.")
        return True

    def enterUsername(self):
        try:
            username = self.driver.find_element(By.ID,"username")
            username.send_keys(self.username)
        except Exception as e:
            logger.error("Exception raised while entering username, with exception :\n\t{e}".format(e=e))
            return False
        logger.info("Username entered.")
        return True

    def enterPassword(self):
        try:
            password = self.driver.find_element(By.ID,"password")
            password.send_keys(self.password)
        except Exception as e:
            logger.error("Exception raised while entering password, with exception :\n\t{e}".format(e=e))
            return False
        logger.info("Password entered.")
        return True

    def login(self):
        try:
            self.driver.implicitly_wait(10)
            login = self.driver.find_element(By.CLASS_NAME,"sign-in")
            login.click()
        except Exception as e:
            logger.error("Exception raised while clicking login button, with exception :\n\t{e}".format(e=e))
            return False
        
        # check for toast message 
        try :
            #self.driver.implicitly_wait(10)
            message = self.driver.find_element(By.CLASS_NAME,"toast-message").get_attribute("innerHTML")
            message = message.replace("  ",'')
            message = message.replace("\n",'')
            message = (message.split('.'))[0]
            if message == "Invalid password":
                logger.warning("Password wrong for user : {u}".format(u=(str(self.dpcode)+str(self.username))))
                # return false for wrong password 
                return False
        except:
            
            pass
        logger.info("Logged In.")
        return True

    def moveToAsba(self):
        try:
            myAsbaBtn = self.driver.find_element(By.XPATH,"/html/body/app-dashboard/div/div[1]/nav/ul/li[8]/a")
            myAsbaBtn.click()
        except NoSuchElementException as e:
            print(e,"\n\n",self.driver.get_window_size())
            # could find the element because of window width small.
            # now clicking sidebar minimizer first then hyper link
            try:
                sidebarMaximizer = self.driver.find_element(By.CLASS_NAME,"sidebar-minimizer")
                sidebarMaximizer.click()
                myAsbaBtn = self.driver.find_element(By.XPATH,"/html/body/app-dashboard/div/div[1]/nav/ul/li[8]/a")
                myAsbaBtn.click()
            except Exception as e:
                logger.error("Exception raised while finding sidebar minimizer, with exception :\n\t{e}".format(e=e))
                return False
            
        except Exception as e:
            logger.error("Exception raised while moving to my asba page, with exception :\n\t{e}".format(e=e))
            return False
        logger.info("Moved to My ASBA page.")
        return True

    def apply(self):
        # finding the parent element where companies are present.
        companyList = self.driver.find_elements(By.CLASS_NAME,"company-list")
        
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
            if stockType not in ["Ordinary Shares"] :
                continue


            try:
                applyBtn = companyList[num].find_element(By.CLASS_NAME,"btn-issue")
            except NoSuchElementException:
                logger.warning("Apply button couldn't be found.")
                # This occurs when ipo already applied and been verified
                continue
            except Exception as e:
                logger.error("Exception raised while finding apply button, with exception :\n\t{e}".format(e=e))
                return False
            
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
                return False

            # enter units
            try:
                applyKitta = self.driver.find_element(By.ID,"appliedKitta")
                applyKitta.send_keys(self.units)
            except Exception as e:
                logger.error("Exception raised while entering units, with exception :\n\t{e}".format(e=e))
                return False
            
            # enter crn
            try:
                crn = self.driver.find_element(By.ID,"crnNumber")
                crn.send_keys(self.crn)
            except Exception as e:
                logger.error("Exception raised while entering CRN number, with exception :\n\t{e}".format(e=e))
                return False

            # accept terms
            try:
                terms = self.driver.find_element(By.ID,"disclaimer")
                terms.click()
            except Exception as e:
                logger.error("Exception raised while accepting terms, with exception :\n\t{e}".format(e=e))
                return False

            # proceed to pin
            try:
                proceed = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[1]/form/div[2]/div/div[5]/div[2]/div/button[1]')
                proceed.click()
            except Exception as e:
                logger.error("Exception raised while proceeding to pin, with exception :\n\t{e}".format(e=e))
                return False
            
            self.driver.implicitly_wait(20)

            # entering transaction pin
            try:
                transactionPin = self.driver.find_element(By.ID,"transactionPIN")
                transactionPin.send_keys(self.pin)
            except Exception as e:
                logger.error("Exception raised while entering pin, with exception :\n\t{e}".format(e=e))
                return False

            # submit issues request
            try:
                submit = self.driver.find_element(By.XPATH,'//*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[2]/div[2]/div/form/div[2]/div/div/div/button[1]')
                submit.click()
            except Exception as e:
                logger.error("Exception raised while submiting issue request, with exception :\n\t{e}".format(e=e))
                return False
            continue
        logger.info("Applied !")
        return True



