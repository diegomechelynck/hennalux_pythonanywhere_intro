from sqlalchemy import create_engine
from datetime import datetime
import configparser
from Get_Current_Weather import Get_Current_Weather
import hashlib
import os
Dir_Path = os.path.dirname(os.path.realpath(__file__))

# Reading credentials from config file:
Config = configparser.RawConfigParser()
Config.read(Dir_Path + "/Credentials.conf")
Open_Weather_Api_Key = Config.get('DEFAULT', 'Open_Weather_Api_Key')
MySQL_DataBase_Name = Config.get('DEFAULT', 'MySQL_DataBase_Name')
MySQL_DataBase_User = Config.get('DEFAULT', 'MySQL_DataBase_User')
MySQL_DataBase_Password = Config.get('DEFAULT', 'MySQL_DataBase_Password')

# Create Database Connection and create table if not exists:
Database_Connection_Url = "mysql+mysqldb://" + MySQL_DataBase_User + ":" + MySQL_DataBase_Password + "@" + MySQL_DataBase_User + ".mysql.pythonanywhere-services.com/" + MySQL_DataBase_User + "$" + MySQL_DataBase_Name +"?charset=utf8"
Engine = create_engine(Database_Connection_Url)

Query = """
    CREATE TABLE IF NOT EXISTS Temperature_History (
    Id varchar(100),
    Date date,
    City varchar(70),
    Temperature float,
    PRIMARY KEY (Id)
    )
    """
Engine.execute(Query)


# Retrieve today's temperature an push into table:
Cities=["Brussels", "Namur"]
for City in Cities:
    Conn = Engine.connect()

    Current_Weather=Get_Current_Weather(City=City, Open_Weather_Api_Key=Open_Weather_Api_Key)
    Temperature=Current_Weather["main"]["temp"]
    Date_Unix_Timestamp=Current_Weather["dt"]
    Date = datetime.utcfromtimestamp(int(Date_Unix_Timestamp)).strftime('%Y-%m-%d')
    Id=hashlib.md5((City+Date).encode('utf-8')).hexdigest()


    Query="REPLACE INTO Temperature_History SET Id='" + str(Id) + "',Date='" + Date + "',City='" + City + "',Temperature="+str(Temperature)
    Conn.execute(Query)
    Conn.close()
Engine.dispose()




