import sqlite3
import logging

logger = logging.getLogger(__name__)

class DBhandeler():
    def __init__(self) -> None:
        
        try:
            self.connection = sqlite3.connect("data/user.db")

            self.cursor = self.connection.cursor()

            logger.info("Connection with database established.")
        except Exception as e:
            logger.error("Connection with database failed with exception {}".format(e))
            pass
        else:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                dpCode TEXT,
                password TEXT,
                units TEXT,
                crn TEXT,
                transPin TEXT
            )""")
        
        pass

    def addUser(self,dpCode,password,units,crn,transPin):
        try:
            self.cursor.execute("""
                INSERT INTO users VALUES(?,?,?,?,?)
            """,(dpCode,password,units,crn,transPin))
            self.connection.commit()
            logger.info(("Added Account into database, with values: DP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}").format(dp=dpCode,password=password,units=units,crn=crn,trans=transPin))
            return True
        except Exception as e:
            logger.error(("Failed to add Account into database, with values: DP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}\nwith exception :\n\t{e}").format(dp=dpCode,password=password,units=units,crn=crn,trans=transPin,e=e))
            return False

    def editUser(self,prevDPCode,dpCode,password,units,crn,transPin):
        try:
            self.cursor.execute("""
                UPDATE users SET 
                
                dpCode = :dpCode,
                password = :password,
                units = :units,
                crn = :crn,
                transPin = :transPin

                WHERE dpCode = :prevDPCode

            """,{
                "prevDPCode"  : prevDPCode,
                "dpCode" : dpCode,
                "password" : password,
                "units" : units,
                "crn" : crn,
                "transPin" : transPin

            })
            self.connection.commit()    
            logger.info(("Edited Account with dpcode ({prevdp}) from database, with values: DP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}").format(prevdp=prevDPCode,dp=dpCode,password=password,units=units,crn=crn,trans=transPin))    
            return True
        except Exception as e:
            logger.error(("Failed to edit Account with dpcode ({prevdp}) from database, with values: DP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}\nwith exception :\n\t{e}").format(prevdp=prevDPCode,dp=dpCode,password=password,units=units,crn=crn,trans=transPin,e=e))    
            return False

    def deletUser(self,oID=None,dpCode=None,all=None):

        if all == True:
            try:
                self.cursor.execute("DROP TABLE users")
                self.connection.commit()
                logger.info("Deleted every Account from database.")
                return True
            except Exception as e:
                logger.error("Failed to deleted every Account from database, with exception :\n\t{e}.".format(e=e))
                return False

        if oID != None:
            try:
                self.cursor.execute("DELETE FROM users WHERE oid = :oid",{"oid" : oID})
                self.connection.commit()
                logger.info("Deleted Account from database with oid : {oid} ".format(oid=oID))
                return True
            except Exception as e:
                logger.error("Failed to deleted Account from database with oid : {oid}, with exception :\n\t{e}.".format(oid=oID,e=e))
                return False


        if dpCode != None:
            try:
                self.cursor.execute("DELETE FROM users WHERE dpCode = :dpCode",{"dpCode":dpCode})
                self.connection.commit()
                logger.info("Deleted Account from database with DP Code : {dp} ".format(dp=dpCode))
                return True

            except Exception as e:
                logger.error("Failed to deleted Account from database with DP Code : {dp}, with exception :\n\t{e}.".format(dp=dpCode,e=e))
                return False

        return False

    def fetchdata(self,oID = None,all=False,dpCode=None):

        if oID != None:
            try:
                self.cursor.execute("SELECT *,oid FROM users WHERE oid = :oid",{"oid":oID})
                data = self.cursor.fetchall()
                logger.info("Fetched account from database with oid : {}".format(oID))
            except Exception as e:
                logger.error("Failed to fetch account from database with oid ({oid}), with exception:\n\t{e}".format(oid=oID,e=e))
            return data

        if dpCode != None:
            try:
                self.cursor.execute("SELECT *,oid FROM users WHERE dpCode = :dpCode",{"dpCode":dpCode})
                data = self.cursor.fetchall()
                logger.info("Fetched account from database with DP Code : {}".format(dpCode))
                return data[0]
            except Exception as e:
                logger.error("Failed to fetch account from database with DP Code ({dp}), with exception:\n\t{e}".format(dp=dpCode,e=e))
                return False

        if all == True:
            try:

                self.cursor.execute("SELECT *,oid FROM users")
                data = self.cursor.fetchall()
                logger.info("Fetched every account from database")

                return data

            except Exception as e:
                logger.error("Failed to fetch every account from database, with exception:\n\t{}".format(e))
                return False

        return False


#print(DBhandeler().addUser("891","pass","90","98123","6969"))
#print(DBhandeler().editUser("2","891","pass","69","98123","6969"))
#print(DBhandeler().deletUser(oID=2))

#print((DBhandeler().fetchdata(oID=1)))
