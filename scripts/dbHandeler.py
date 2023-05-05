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
                transPin TEXT,
                nickname TEXT
            )""")
        
        pass

    def addUser(self,dpCode,password,units,crn,transPin,nickname):
        try:
            self.cursor.execute("""
                INSERT INTO users VALUES(?,?,?,?,?,?)
            """,(dpCode,password,units,crn,transPin,nickname))
            self.connection.commit()
            logger.info(("Added Account into database, with values: Nickname :{nickname} \n\tDP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}").format(nickname=nickname,dp=dpCode,password=password,units=units,crn=crn,trans=transPin))
            return True
        except Exception as e:
            logger.error(("Failed to add Account into database, with values: Nickname :{nickname} \n\tDP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}\nwith exception :\n\t{e}").format(nickname=nickname,dp=dpCode,password=password,units=units,crn=crn,trans=transPin,e=e))
            return False

    def editUser(self,prev_nickname,nickname,dpCode,password,units,crn,transPin):
        try:
            self.cursor.execute("""
                UPDATE users SET 
                
                dpCode = :dpCode,
                password = :password,
                units = :units,
                crn = :crn,
                transPin = :transPin,
                nickname = :nickname
                
                WHERE nickname = :prev_nickname

            """,{
                "prev_nickname"  : prev_nickname,
                
                "dpCode" : dpCode,
                "password" : password,
                "units" : units,
                "crn" : crn,
                "transPin" : transPin,
                "nickname" : nickname

            })
            self.connection.commit()    
            logger.info(("Edited Account with Nickname ({prev_nickname}) from database, with values: Nickname : {nickname}\n\tDP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}").format(prev_nickname=prev_nickname,nickname=nickname,dp=dpCode,password=password,units=units,crn=crn,trans=transPin))    
            return True
        except Exception as e:
            logger.error(("Failed to edit Account with Nickname ({prev_nickname}) from database, with values: Nickname : {nickname}\n\tDP Code : {dp} \n\tPassword : {password}\n\tUnits : {units}\n\tCRN No : {crn}]\n\t Transaction Pin : {trans}\nwith exception :\n\t{e}").format(prev_nickname=prev_nickname,nickname=nickname,dp=dpCode,password=password,units=units,crn=crn,trans=transPin,e=e))    
            return False

    def deleteUser(self,oID=None,dpCode=None,nickname=None,all=None):

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
    
        if nickname != None:
            try:
                self.cursor.execute("DELETE FROM users WHERE nickname = :nickname",{"nickname":nickname})
                self.connection.commit()
                logger.info("Deleted Account from database with Nickname : {nickname} ".format(nickname=nickname))
                return True

            except Exception as e:
                logger.error("Failed to deleted Account from database with Nickname : {nickname}, with exception :\n\t{e}.".format(nickname=nickname,e=e))
                return False

        return False

    def fetchdata(self,oID = None,all=False,dpCode=None,nickname=None):

        if oID != None:
            try:
                self.cursor.execute("SELECT *,oid FROM users WHERE oid = :oid",{"oid":oID})
                data = self.cursor.fetchall()
                
            except Exception as e:
                logger.error("Failed to fetch account from database with oid ({oid}), with exception:\n\t{e}".format(oid=oID,e=e))
                return False
        
            dp_code = data[0][0]
            password = data[0][1]
            units = data[0][2]
            crn_no = data[0][3]
            tran_pin = data[0][4]
            temp_nickname = data[0][5]
            oid = data[0][6]
            return_data = {
                'dp_code':dp_code,
                "password": password,
                "units": units,
                "crn_no":crn_no,
                "tran_pin": tran_pin,
                "nickname":temp_nickname,
                "oid":oid
            }
            logger.info("Fetched account from database with Nickname : {}".format(temp_nickname))
            return return_data

        if dpCode != None:
            try:
                self.cursor.execute("SELECT *,oid FROM users WHERE dpCode = :dpCode",{"dpCode":dpCode})
                data = self.cursor.fetchall()
            except Exception as e:
                logger.error("Failed to fetch account from database with DP Code ({dp}), with exception:\n\t{e}".format(dp=dpCode,e=e))
                return False
            dp_code = data[0][0]
            password = data[0][1]
            units = data[0][2]
            crn_no = data[0][3]
            tran_pin = data[0][4]
            temp_nickname = data[0][5]
            oid = data[0][6]
            return_data = {
                'dp_code':dp_code,
                "password": password,
                "units": units,
                "crn_no":crn_no,
                "tran_pin": tran_pin,
                "nickname":temp_nickname,
                "oid":oid
            }
            logger.info("Fetched account from database with Nickname : {}".format(temp_nickname))
            return return_data

        if nickname != None:
            try:
                self.cursor.execute("SELECT *,oid FROM users WHERE nickname = :nickname",{"nickname":nickname})
                data = self.cursor.fetchall()
                logger.info("Fetched account from database with Nickname : {}".format(nickname))
                
            except Exception as e:
                logger.error("Failed to fetch account from database with Nickname ({nickname}), with exception:\n\t{e}".format(nickname=nickname,e=e))
                return False
            dp_code = data[0][0]
            password = data[0][1]
            units = data[0][2]
            crn_no = data[0][3]
            tran_pin = data[0][4]
            temp_nickname = data[0][5]
            oid = data[0][6]
            return_data = {
                'dp_code':dp_code,
                "password": password,
                "units": units,
                "crn_no":crn_no,
                "tran_pin": tran_pin,
                "nickname":temp_nickname,
                "oid":oid
            }
            logger.info("Fetched account from database with Nickname : {}".format(temp_nickname))
            return return_data


        if all == True:
            try:

                self.cursor.execute("SELECT *,oid FROM users")
                data = self.cursor.fetchall()
                logger.info("Fetched every account from database")
                return_data = []
                for profile in data:
                    dp_code = profile[0]
                    password = profile[1]
                    units = profile[2]
                    crn_no = profile[3]
                    tran_pin = profile[4]
                    temp_nickname = profile[5]
                    oid = profile[6]
                    temp_data = {
                        'dp_code':dp_code,
                        "password": password,
                        "units": units,
                        "crn_no":crn_no,
                        "tran_pin": tran_pin,
                        "nickname":temp_nickname,
                        "oid":oid
                    }
                    return_data.append(temp_data)
                return return_data

            except Exception as e:
                logger.error("Failed to fetch every account from database, with exception:\n\t{}".format(e))
                return False

        return False

    def manual(self,prev_dpCode,password):
        self.cursor.execute("""
                UPDATE users SET 
                
                password =:password
                
                WHERE dpCode = :prev_dpCode

            """,{
                "prev_dpCode"  : prev_dpCode,
                
                "password" : password

            })
        self.connection.commit()
        return True
#print(DBhandeler().addUser("891","pass","90","98123","6969"))
#print(DBhandeler().editUser("2","891","pass","69","98123","6969"))
#print(DBhandeler().fetchdata(all=True))

#print((DBhandeler().manual(13010400007asda11,"adsad")))
