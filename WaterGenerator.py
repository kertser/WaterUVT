# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 14:21:15 2022
Water file generator
Generates Water transmittance file for UVT
@author: Mike
"""

#%% Imports and variables:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,InputLayer

from sklearn.preprocessing import StandardScaler

TargetUVT = 60 #[%-1cm]

#%% Load CSV form file
waterFile = 'Water.csv'
df = pd.read_csv(waterFile,index_col=0)
print(df.head())

#%% Preprare the data for the model

#Unfold the data into matrix of [Wavelength,UVT254,Transmittance(0-1)]
Data = pd.DataFrame([[index/1000,int(colName)/100,df.loc[index].at[colName]/100] 
                     for index in df.index for colName in df.columns.values], 
                    columns =['wavelength', 'UVT254%', 'T%'])#.set_index('wavelength')


X = Data.drop(['T%'],axis=1)
y = Data['T%']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)


#%% Build the Regressor model

Epochs = 100
Features = X_train.shape[1]
LearningRate = 0.0005
print(f'Number of Features = {Features}')


model = Sequential()
model.add(InputLayer(input_shape=(Features,)))
model.add(Dense(10, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Dense(1, activation='linear', name="Output_Layer"))

model.summary()
model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
#model.compile(optimizer='Adam', loss='mse', metrics=['mae'])

#%% Fit the model

history = model.fit(X_train_scaled,y_train, validation_data=(X_test_scaled, y_test), epochs=Epochs, verbose=2)

#%% Summarize history for accuracy

plt.plot(history.history['mae'])
plt.plot(history.history['val_mae'])
plt.title('model mean absolute error')
plt.ylabel('MAE')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()


#%% Predictor Vector

TargetUVT = 70 #[%-1cm]
WavelengthRange = np.linspace(0.190,0.500,311)
TargetVector = [[wl, TargetUVT/100] for wl in WavelengthRange]
UVT_Vector = pd.DataFrame(TargetVector)
PredictionT = model.predict(scaler.transform(pd.DataFrame(TargetVector)))
plt.scatter(WavelengthRange, PredictionT,s=1)
plt.show()

#%% Save model and scaler
from pickle import dump
model.save('WaterUVT.h5')
dump(scaler, open('scaler.pkl', 'wb'))

