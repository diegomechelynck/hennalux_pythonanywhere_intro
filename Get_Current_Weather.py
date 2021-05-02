import requests
import json


def Get_Current_Weather(City, Open_Weather_Api_Key):

    Url="http://api.openweathermap.org/data/2.5/weather?q=" + City + "&appid=" + Open_Weather_Api_Key
    Response_As_Dict = json.loads(requests.get(Url).text)

    return Response_As_Dict


if __name__ == "__main__":

    import configparser

    # Reading credentials from config file:
    config = configparser.RawConfigParser()
    config.read("/home/henallux/Weather_Prediction/Credentials.conf")
    Open_Weather_Api_Key = config.get('DEFAULT', 'Open_Weather_Api_Key')

    # retrieve weather in Brussels:
    City = "Brussels"
    Result = Get_Current_Weather(City=City, Open_Weather_Api_Key=Open_Weather_Api_Key)
    print(Result)



