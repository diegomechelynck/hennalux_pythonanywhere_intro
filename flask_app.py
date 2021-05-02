
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
from Predict_Next_Day_Weather import Predict_Next_Day_Weather, Get_Weather_History

app = Flask(__name__)

@app.route("/temperature")
def Show_Temp_Data():
    #test=Get_Weather_History()
    #resultlistofdict=[dict(r) for r in test]
    Temperature_History = Get_Weather_History()
    Temperature_Predictions = Predict_Next_Day_Weather()

    return render_template('Temperature_Page.html', data=Temperature_History, preditcions = Temperature_Predictions)