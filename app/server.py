from flask import Flask, render_template, request
import requests
import pandas as pd 
import matplotlib.pyplot as plt
from prophet import Prophet
import plotly.graph_objects as go
import plotly
import json
import os
import datetime

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def forex():
    if request.method=='POST':
        currency_one = request.form.get('currecy_one')
        currency_two = request.form.get('currecy_two')
        
        #prediction(currency_one,currency_two)
        
        filename = f'./app/static/csv/{datetime.date.today()}_{currency_one}_{currency_two}.csv'
        if os.path.exists(filename):
            final_df = pd.read_csv(filename)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=final_df["ds"], y=final_df['yhat'],
                                mode='lines+markers',
                                name='Previous Data'))
            fig.add_trace(go.Scatter(x=final_df['ds'][-10:], y=final_df['yhat'][-10:],
                                mode='lines+markers',
                                name='Forecast'))
            
            fig.update_layout(
            # title="Plot Title",
            xaxis_title="Date",
            yaxis_title="Price",
            # legend_title="Legend Title",
            )

            final_list = final_df.values.tolist()
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        else:
            url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol='+currency_one+'&to_symbol='+currency_two+'&outputsize=full&apikey=AZ89X01V07YVYBDH'
            r = requests.get(url)
            data = r.json() 
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
            fig.update_layout(
            # title="Plot Title",
            xaxis_title="Date",
            yaxis_title="Price",
            # legend_title="Legend Title",
            )
            final_df = final_df.astype(str)
            final_df['ds'] = final_df['ds'].apply(lambda x : x.replace('00:00:00',"").strip())
            final_df.to_csv(filename,index=False)
            final_list = final_df.values.tolist()
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('home.html',graphJSON=graphJSON,df = final_list)
    return render_template('home.html')
    


