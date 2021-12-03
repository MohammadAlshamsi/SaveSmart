# Ploting packages
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Date wrangling
from datetime import datetime, timedelta

# Data wrangling
import pandas as pd 

# The deep learning class
from AI import DeepModelTS

# Reading the configuration file
import yaml

# Directory managment 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# Module needed to create file to save the outputs
import csv

# Reading the hyper parameters for the pipeline

with open(f'{os.getcwd()}\\conf.yml') as file:
    conf = yaml.load(file, Loader=yaml.FullLoader)

# Reading the data 
d = pd.read_csv('C:/Users/mohad/SDP/input/DAYTON_hourly.csv')
d['Datetime'] = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in d['Datetime']]

# Making sure there are no duplicated data
# If there are some duplicates we average the data during those duplicated days
d = d.groupby('Datetime', as_index=False)['DAYTON_MW'].mean()

# Sorting the values
d.sort_values('Datetime', inplace=True)

# Initiating the class 
deep_learner = DeepModelTS(
    data=d, 
    Y_var='DAYTON_MW',
    lag=conf.get('lag'),
    LSTM_layer_depth=conf.get('LSTM_layer_depth'),
    epochs=conf.get('epochs'),
    train_test_split=conf.get('train_test_split') # The share of data that will be used for validation
)

# Fitting the model 
model = deep_learner.LSTModel()

# Making the prediction on the validation set
# Only applicable if train_test_split in the conf.yml > 0
yhat = deep_learner.predict()

if len(yhat) > 0:

    # Constructing the forecast dataframe
    fc = d.tail(len(yhat)).copy()
    fc.reset_index(inplace=True)
    fc['forecast'] = yhat

    # # Ploting the forecasts
    # plt.figure(figsize=(12, 8))
    # for dtype in ['DAYTON_MW', 'forecast']:
    #      plt.plot(
    #          'Datetime',
    #          dtype,
    #          data=fc,
    #          label=dtype,
    #          alpha=0.8
    #      )
    # plt.legend()
    # plt.grid()
    # plt.show()   
    
# Forecasting n steps ahead   

# Creating the model using full data and forecasting n steps ahead
deep_learner = DeepModelTS(
    data=d, 
    Y_var='DAYTON_MW',
    lag=24,
    LSTM_layer_depth=64,
    epochs=10,
    train_test_split=0 
)

# Fitting the model 
deep_learner.LSTModel()

# Forecasting n steps ahead
n_ahead = 168
yhat = deep_learner.predict_n_ahead(n_ahead)
yhat = [y[0][0] for y in yhat]
print(yhat)

# Constructing the forecast dataframe
fc = d.tail(400).copy() 
fc['type'] = 'original'

last_date = max(fc['Datetime'])
hat_frame = pd.DataFrame({
    'Datetime': [last_date + timedelta(hours=x + 1) for x in range(n_ahead)], 
    'DAYTON_MW': yhat,
    'type': 'forecast'
})

fc = fc.append(hat_frame)
fc.reset_index(inplace=True, drop=True)

 #Ploting the forecasts 
# plt.figure(figsize=(12, 8))
# for col_type in ['original', 'forecast']:
#      plt.plot(
#          'Datetime', 
#          'DAYTON_MW', 
#          data=fc[fc['type']==col_type],
#          label=col_type
#          )

# plt.legend()
# plt.grid()
# plt.show() 
if os.path.exists('predictions.csv'):
    os.remove('predictions.csv')
csv_columns = ['Datetime', 'DAYTON_MW']
i = 0
with open ('predictions.csv' , 'w') as f:
    for y in yhat:
        time = datetime.now() + timedelta(hours=i)
        current_time= time.strftime('%Y-%m-%d %H:%M:%S')
        # dictionary = {"Datetime": current_time, "DAYTON_MW":y}
        f.write("%s,%s\n"%(current_time, int(y)))
        i = i + 1
# try:
#     with open ('predictions.csv' , 'w') as f:
#         # for data in dictionary.items():
#         for x in yhat:
#             f.write("%s,%s\n"%(data,dictionary[data]))