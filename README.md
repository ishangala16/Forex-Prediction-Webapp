# Forex Price Prediction

This project is based on price prediction of currecy pairs. It is used to forecast price of the currency pair based on previous data. This can be used to forecast price for the next 10 days.


## Setup
### 1. Clone the repository first using this command
```
git clone https://github.com/ishangala16/forex-prediction.git
```

### 2. Install dependencies 
```
pip install -r requirements.txt
```

## How to run

Run in terminal
```
python gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Open browser and type
```
http://localhost:5000/
```

Create a new account or login into the existing account

Now just select the currency pair from the drop down and click submit.

