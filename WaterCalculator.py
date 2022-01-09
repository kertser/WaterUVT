# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 09:48:57 2022

@author: Mike
"""

from pickle import load
from tensorflow.keras.models import load_model
from numpy import linspace as Linspace
from pandas import DataFrame as DataFrame
import matplotlib.pyplot as plt

# import plotly.express as px

def getWaterVector(TargetUVT=90, OutputToCSV=False):  # Calculate the TargetUVT is in[%-1cm]
    WavelengthRange = Linspace(0.180, 0.600, 421)

    # Calculate the Prediction
    TargetVector = [[wl, TargetUVT / 100] for wl in WavelengthRange]
    PredictionT = model.predict(scaler.transform(DataFrame(TargetVector)))

    # Make the plot
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_title('UVT of selected water type')
    ax1.set_xlabel('wavelength [nm]')
    ax1.set_ylabel('UVT[%-1cm]')
    ax1.grid(color='g', linestyle='--', linewidth=0.5)
    ax1.scatter(WavelengthRange*1000, PredictionT*100, s=1)

    ax1.annotate('UVT254 = ' + str(TargetUVT) + '[%-1cm]', xy=(1, 0), xycoords='axes fraction', style='italic',
                 fontsize=12,
                 horizontalalignment='right', verticalalignment='bottom',
                 bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 1})
    fig.savefig('static/UVTvsWavelength.png', bbox_inches='tight')

    """ Some interactive charts
    
    fig = px.scatter(df, x="wavelength [nm]", y="UVT [%-1cm]")
    fig = px.scatter(x=WavelengthRange, y=[item for sublist in PredictionT for item in sublist])
    fig.update_xaxes(title_text='wavelength[nm]')
    fig.update_yaxes(title_text='UVT[%-1cm]')
    fig.write_html("aaa.html")
    """
    # Output the model into CSV file
    if OutputToCSV is True:
        Output = DataFrame()
        Output['Wavelength'] = DataFrame(WavelengthRange*1000)
        Output['UVT'] = DataFrame(PredictionT*100)
        filename = 'UVT_output.csv'
        Output.to_csv(filename, index=False)


# %% Main script
# Load the model and the Scaler

# model = keras.models.load_model('WaterUVT.h5')
model = load_model('WaterUVT.h5')
scaler = load(open('scaler.pkl', 'rb'))

getWaterVector(90)
