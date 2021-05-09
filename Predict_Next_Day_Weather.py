from sqlalchemy import create_engine
import configparser
import os
Dir_Path = os.path.dirname(os.path.realpath(__file__))

# Reading credentials from config file:
Config = configparser.RawConfigParser()
Config.read(Dir_Path + "/Credentials.conf")
MySQL_DataBase_Name = Config.get('DEFAULT', 'MySQL_DataBase_Name')
MySQL_DataBase_User = Config.get('DEFAULT', 'MySQL_DataBase_User')
MySQL_DataBase_Password = Config.get('DEFAULT', 'MySQL_DataBase_Password')


# Create Database Connection Pool:
Database_Connection_Url = "mysql+mysqldb://" + MySQL_DataBase_User + ":" + MySQL_DataBase_Password + "@" + MySQL_DataBase_User + ".mysql.pythonanywhere-services.com/" + MySQL_DataBase_User + "$" + MySQL_DataBase_Name +"?charset=utf8"
Engine = create_engine(Database_Connection_Url)

def Predict_Next_Day_Weather():
    # Make and retrieve dummy prediction:
    Conn = Engine.connect()
    Query="""
        SELECT City,
               avg(Temperature) as Predicted_Temperature
        from Temperature_History
        WHERE Date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
        GROUP BY City
        """
    Result = Conn.execute(Query).fetchall()
    Result_As_Dict = [dict(r) for r in Result]
    Conn.close()

    return Result_As_Dict

def Get_Weather_History():
    Conn = Engine.connect()
    Query="""
        SELECT concat(year(a.Date),"-",month(a.Date), "-", case when length(day(a.Date))=1 then concat('0', day(a.Date)) else day(a.Date) end) as Date, a.Temperature as Temp_Brussels, b.Temperature as Temp_Namur
        from Temperature_History a
        left join Temperature_History b on a.Date=b.Date
        WHERE a.City="Brussels" and b.City="Namur"
        """
    Result = Conn.execute(Query).fetchall()
    Result_As_Dict = [dict(r) for r in Result]
    Conn.close()

    return Result_As_Dict


if __name__ == "__main__":
    print("Predicted Temp:")
    print(Predict_Next_Day_Weather())

    print("History:")
    print(Get_Weather_History())
