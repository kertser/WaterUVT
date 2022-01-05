# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 09:48:57 2022

@author: Mike
"""

from pickle import load
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def getWaterVector(TargetUVT=90, OutputToCSV = False):
# Calculate the TargetUVT is in[%-1cm]
    WavelengthRange = np.linspace(0.190,0.500,311)

    # Calculate the Prediction
    TargetVector = [[wl, TargetUVT/100] for wl in WavelengthRange]
    PredictionT = model.predict(scaler.transform(pd.DataFrame(TargetVector)))

    # Make the plot
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_title('UVT of selected water type')
    ax1.set_xlabel('wavelength [nm]')
    ax1.set_ylabel('UVT[%-1cm]')
    ax1.grid(color='g', linestyle='--', linewidth=0.5)
    ax1.scatter(WavelengthRange, PredictionT,s=1)
    fig.savefig('static/UVTvsWavelength.png', bbox_inches='tight')

    # Output the model into CSV file
    if (OutputToCSV==True):
        Output = pd.DataFrame()
        Output['Wavelength'] = pd.DataFrame(WavelengthRange)
        Output['UVT'] = pd.DataFrame(PredictionT)
        filename = 'UVT='+str(TargetUVT)+'[%-1cm].csv'
        Output.to_csv(filename, index=False)

#%% Main script
# Load the model and the Scaler

model = keras.models.load_model('WaterUVT.h5')
scaler = load(open('scaler.pkl', 'rb'))

getWaterVector(90)
