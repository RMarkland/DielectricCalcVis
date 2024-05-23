#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

Script by yours truly - Reid Markland

Developed to calculate dielectric constant from capacitance data given folder
path and file names.

DielectricDF = CalcEnergyEfficiency(fPath, fNames)
    
Inputs:
    path:           path to folders containing data
    file1064:       File of spot data for 1064
    file1065:       File of spot data for 1065
    
Outputs:
    Dielectrics:    DataFrame of dielectric values (
                    col1: Scan File Name;
                    col2: Dielectric value calc using spot size found or 
                            avg spot for associated sample
                    col3: Dielectric value calc using repeat spot size data
                    )

03/31/23
"""

import os
import pandas as pd
import numpy as np
import re

# C-V Data Directory
path = r'/Users/reidmarkland/Documents/Research/SULI23/Work For Di/Dielectric Calculations'
# Spot Size Data Directory
file1064 = r'/Users/reidmarkland/Documents/Research/SULI23/Work For Di/Dielectric Calculations/AC_1064.txt'
file1065 = r'/Users/reidmarkland/Documents/Research/SULI23/Work For Di/Dielectric Calculations/AC_1065.txt'

def CalcDielectric(path, file1064, file1065):
    #init
    dielectricMaxDF = pd.DataFrame()
    dielectricMinDF = pd.DataFrame()
    identifiers = ['']
    ep0 = 8.85418782*10**-12
    
    # Load Contact Size Data
    spot1064 = pd.read_csv(file1064, sep = '\t', index_col = 'spot')
    spot1065 = pd.read_csv(file1065, sep = '\t', index_col = 'spot')
    
    #Calc Avg Contact Sizes (No switch-case for python 3.8)
    a=np.array([[1,2,3]]); e=d=c=b=a;
    for spot in spot1064.index:
        if 'A' in spot:
            a = np.append(a,[spot1064.loc[spot,:].values], axis=0)
        elif 'B' in spot:
            b = np.append(a,[spot1064.loc[spot,:].values], axis=0)
        elif 'C' in spot:
            c = np.append(a,[spot1064.loc[spot,:].values], axis=0)
        elif 'D' in spot:
            d = np.append(a,[spot1064.loc[spot,:].values], axis=0)
        elif 'E' in spot:
            e = np.append(a,[spot1064.loc[spot,:].values], axis=0)
    avg_1064 = np.array([[np.average(a[1:,0]),np.average(a[1:,1])],\
                       [np.average(b[1:,0]),np.average(b[1:,1])],\
                           [np.average(c[1:,0]),np.average(c[1:,1])],\
                               [np.average(d[1:,0]),np.average(d[1:,1])],\
                                   [np.average(e[1:,0]),np.average(e[1:,1])]])
    a=np.array([[1,2,3]]); e=d=c=b=a;
    for spot in spot1065.index:
        if 'A' in spot:
            a = np.append(a,[spot1065.loc[spot,:].values], axis=0)
        elif 'B' in spot:
            b = np.append(a,[spot1065.loc[spot,:].values], axis=0)
        elif 'C' in spot:
            c = np.append(a,[spot1065.loc[spot,:].values], axis=0)
        elif 'D' in spot:
            d = np.append(a,[spot1065.loc[spot,:].values], axis=0)
        elif 'E' in spot:
            e = np.append(a,[spot1065.loc[spot,:].values], axis=0)
    avg_1065 = np.array([[np.average(a[1:,0]),np.average(a[1:,1])],\
                       [np.average(b[1:,0]),np.average(b[1:,1])],\
                           [np.average(c[1:,0]),np.average(c[1:,1])],\
                               [np.average(d[1:,0]),np.average(d[1:,1])],\
                                   [np.average(e[1:,0]),np.average(e[1:,1])]])
    
    #Main
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if '.lvm' in file:
                ids = re.split('_|\.',file)
                for names in ids:
                    if 'kHz' in names:
                        freq = names
                        break
                    else:
                        freq = ''
                # Dumb way to ID files bc naming system isn't consistent
                if ids[0] in identifiers[-1]:
                    if freq == '':
                        identifiers.append(ids[0]+'_'+ids[-2])
                    elif freq == ids[-2]:
                        identifiers.append(ids[0]+'_'+freq)
                    elif freq in file:
                        identifiers.append(ids[0]+'_'+freq+'_'+ids[-2])
                    else:
                        identifiers.append(ids[0])                    
                elif freq == '':
                    identifiers.append(ids[0])
                else:
                    identifiers.append(ids[0]+'_'+freq)
                    
                # Pulling Max Capacitance/loss
                tempDF = pd.read_csv(os.path.join(dirpath,file), sep = '\t',\
                                     skiprows = 21)
                Cmax = tempDF.loc[:,'    Cp (F)    '].max()
                Cmin = tempDF.loc[:,'    Cp (F)    '].min()
                Dmax = tempDF.loc[:,'    D       '].mean()
                
                # Calculating Dielectric        
                pathDat = dirpath.split('/')
                    # pulling params = [axis1, axis2, % missing, thickness]
                if '1064' in pathDat[-2]:
                    try:
                        params = spot1064.loc[ids[0]].to_numpy()
                        params = np.append(params, 130*10**(-9))
                    except KeyError:
                        if 'A' in ids[0]:
                            params = np.append(avg_1064[0,:], [0, 130*10**-9])
                        elif 'B' in ids[0]:
                            params = np.append(avg_1064[1,:], [0, 130*10**-9])
                        elif 'C' in ids[0]:
                            params = np.append(avg_1064[2,:], [0, 130*10**-9])
                        elif 'D' in spot:
                            params = np.append(avg_1064[3,:], [0, 130*10**-9])
                        elif 'E' in ids[0]:
                            params = np.append(avg_1064[4,:], [0, 130*10**-9])
                elif '1065' in pathDat[-2]:
                    try:
                        params = spot1065.loc[ids[0]].to_numpy()
                        params = np.append(params, 190*10**(-9))
                    except KeyError:
                        if 'A' in ids[0]:
                            params = np.append(avg_1065[0,:], [0, 190*10**-9])
                        elif 'B' in ids[0]:
                            params = np.append(avg_1065[1,:], [0, 190*10**-9])
                        elif 'C' in ids[0]:
                            params = np.append(avg_1065[2,:], [0, 190*10**-9])
                        elif 'D' in spot:
                            params = np.append(avg_1065[3,:], [0, 190*10**-9])
                        elif 'E' in ids[0]:
                            params = np.append(avg_1065[4,:], [0, 190*10**-9])
                    # Calculating
                spotSize = np.pi*params[0]*params[1]*(1-params[2]/100)/4
                dielectric1 = (Cmax*100**2/spotSize)*params[3]/(spotSize*ep0)*10**12
                dielectricMin1 = (Cmin*100**2/spotSize)*params[3]/(spotSize*ep0)*10**12
                
                # Checking additional spot info
                if '1064'in pathDat[-2]:
                    identifiers[-1] = identifiers[-1]+'_1064'
                    if ids[0]+'_1' in spot1064.index:
                        params = spot1064.loc[ids[0]+'_1'].to_numpy()
                        params = np.append(params, 130*10**(-9))
                    else:
                        Cmax = 0
                        Cmin = 0
                elif '1065' in pathDat[-2]:
                    identifiers[-1] = identifiers[-1]+'_1065'
                    if ids[0]+'_1' in spot1065.index:
                        params = spot1065.loc[ids[0]+'_1'].to_numpy()
                        params = np.append(params, 190*10**(-9))
                    else:
                        Cmax = 0
                        Cmin = 0
                    
                spotSize = np.pi*params[0]*params[1]*(1-params[2]/100)/4
                dielectric2 = (Cmax*100**2/spotSize)*params[3]/(spotSize*ep0)*10**12
                dielectricMin2 = (Cmin*100**2/spotSize)*params[3]/(spotSize*ep0)*10**12
                
                # Collecting
                temp = pd.DataFrame([identifiers[-1], dielectric1, dielectric2, Dmax]).T
                temp2 = pd.DataFrame([identifiers[-1], dielectricMin1, dielectricMin2]).T
                dielectricMaxDF = pd.concat([dielectricMaxDF,temp],axis=0)
                dielectricMinDF = pd.concat([dielectricMinDF,temp2],axis=0)
    
    dielectricMaxDF.columns = ["Scan", "SpotSize 1", "SpotSize 2", "Loss"]
    return dielectricMaxDF, dielectricMinDF
                
Dielectrics, DielectricsMin = CalcDielectric(path, file1064, file1065)
