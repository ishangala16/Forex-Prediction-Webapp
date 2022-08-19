import requests
import pandas as pd
# pd.options.plotting.backend = "plotly"
import matplotlib.pyplot as plt
from prophet import Prophet
import plotly.graph_objects as go
import sys
import os
import datetime
import csv
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

# USD-EUR
# USD-AUD
# USD-NOK
# NOK-AUD
# NOK-EUR
# USD-INR

def prediction(currency_one,currency_two):
    filename = f'./static/csv/{datetime.date.today()}_{currency_one}_{currency_two}.csv'
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        final_list = data.values.tolist()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    else:
        url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol='+currency_one+'&to_symbol='+currency_two+'&outputsize=full&apikey=AZ89X01V07YVYBDH'
        try:
            r = requests.get(url)
            print(currency_one,currency_two)
        except:
            return "error"
        data = r.json()
        # print(data.keys())
        
        closing_price = []
        for i in data['Time Series FX (Daily)']:
            closing_price.append([i,float(data['Time Series FX (Daily)'][i]['4. close'])])
        df = pd.DataFrame(closing_price)
        df = df.iloc[::-1]
        new_data = {'ds':df[0],'y':df[1]}
        new_data = pd.DataFrame(new_data)
        model = Prophet()
        model.fit(new_data)
        future = model.make_future_dataframe(periods=10)
        forecast = model.predict(future)
        forecast = forecast[['ds','yhat']]
        df.columns = ['ds','yhat']
        final_df = pd.concat([df,forecast[-10:]])
        final_df = final_df.round(4)
        final_df = final_df[-21:]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=final_df["ds"], y=final_df['yhat'],
                            mode='lines+markers',
                            name='Previous Data'))
        fig.add_trace(go.Scatter(x=final_df['ds'][-10:], y=final_df['yhat'][-10:],
                            mode='lines+markers',
                            name='Forecast'))
        final_df = final_df.astype(str)
        final_df['ds'] = final_df['ds'].apply(lambda x : x.replace('00:00:00',"").strip())
        final_df.to_csv(filename,index=False)
        # final_df['yhat'] = final_df['yhat'].apply(lambda x : x[:7]))
        final_list = final_df.values.tolist()


prediction('USD','INR')