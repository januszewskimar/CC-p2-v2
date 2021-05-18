from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import pmdarima as pm

app = Flask(__name__)
api = Api(app)

def prediccion(periodo):
    temperature = prediccionTemperature(periodo)
    humidity = prediccionHumidity(periodo)
    
    data = []
    
    for i in range(periodo):
        item = {}
        item['hour'] = i
        item['temp'] = temperature[i]
        item['hum'] = humidity[i]
        data.append(item)
        

    return data

def prediccionTemperature(periodo):
    df = pd.read_csv('temperature.csv', header=0)
        
    df = df.fillna(df.mean())

    model = pm.auto_arima(df['San Francisco'], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=True,    # To convert it into SARIMA
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)


    # Forecast
    fc, confint = model.predict(n_periods=periodo, return_conf_int=True)
    
    return fc.tolist()

def prediccionHumidity(periodo):
    df = pd.read_csv('humidity.csv', header=0)
    
    df = df.fillna(df.mean())

    model = pm.auto_arima(df['San Francisco'], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=True,    # To convert it into SARIMA
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)


    # Forecast
    fc, confint = model.predict(n_periods=periodo, return_conf_int=True)
   
    return fc.tolist()

class Prediccion24h(Resource):
    def get(self):
        return prediccion(24)
        
class Prediccion48h(Resource):
    def get(self):
        return prediccion(48)

class Prediccion72h(Resource):
    def get(self):
        return prediccion(72)

api.add_resource(Prediccion24h, '/servicio/v2/prediccion/24horas/')
api.add_resource(Prediccion48h, '/servicio/v2/prediccion/48horas/')
api.add_resource(Prediccion72h, '/servicio/v2/prediccion/72horas/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
