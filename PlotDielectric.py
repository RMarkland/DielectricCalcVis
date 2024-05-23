#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 12:55:44 2023

@author: reidmarkland
"""

import os
import pandas as pd

# Input path to folder inside quotes for path and file name in quotes for file, like below
path = r'/Users/reidmarkland/Documents/Research/SULI23/Work For Di/Dielectric Calculations/AC1065/1065d'
file = r'D97_-7-7V_1kHz_1.lvm'

#Loads Data
tempDF = pd.read_csv(os.path.join(path,file), sep = '\t',\
                     skiprows = 21)

#Plots Data
tempDF.plot('DC Voltage (V)  ','    Cp (F)    ')

# Gives max, min, and ratio between the two
print('Max Val:  ',tempDF.loc[:,'    Cp (F)    '].max())
print('Min Val:  ',tempDF.loc[:,'    Cp (F)    '].min())
print('Ratio:  ',tempDF.loc[:,'    Cp (F)    '].max()/tempDF.loc[:,'    Cp (F)    '].min())