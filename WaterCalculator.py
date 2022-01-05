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

model = keras.models.load_model('WaterUVT.h5')
scaler = load(open('scaler.pkl', 'rb'))

#scaler.inverse_transform
#scaler.transform

def getWaterVector(TargetUVT=90):
    # TargetUVT is in[%-1cm]
    WavelengthRange = np.linspace(0.190,0.500,311)
    TargetVector = [[wl, TargetUVT/100] for wl in WavelengthRange]
    PredictionT = model.predict(scaler.transform(pd.DataFrame(TargetVector)))

    plt.scatter(WavelengthRange, PredictionT,s=1)
    plt.savefig('UVTvsWavelength.png', bbox_inches='tight')
    #plt.show()