#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 00:14:11 2024

@author: arthurweidmann
"""

import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib
from matplotlib import gridspec
import itertools

# MATPLOTLIB CONFIGURATIONS
matplotlib.rcParams['font.family'] = "Arial"  # change the default font
matplotlib.rcParams['xtick.direction'] = 'in'  # change the ticks direction
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams["xtick.bottom"] = False

font = FontProperties()
font.set_family('sans-serif')  # 'serif', 'sans-serif', 'cursive', 'fantasy', or 'monospace'
font.set_name('Arial')
font.set_weight('bold')
font.set_style('normal')  # 'normal', 'italic' or 'oblique'
font.set_size('large')  # xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'

font_tick = FontProperties()
font_tick.set_family('sans-serif')  # 'serif', 'sans-serif', 'cursive', 'fantasy', or 'monospace'
font_tick.set_name('Arial')
font_tick.set_weight('normal')
font_tick.set_style('normal')  # 'normal', 'italic' or 'oblique'
font_tick.set_size('medium')  # xx-small','x-small','small','medium','large','x-large','xx-large'

plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

def main():

    simlist = ['183','188','189']
    complist = ['1:1','1:2','2:1']

    tlist183 = list(np.arange(0,3001,100))
    tlist188 = list(np.arange(0,8001,1))
    tlist189 = list(np.arange(0,3001,1))
    timelists = [tlist183, tlist188, tlist189]

    #prdlist183 = ['1','2','3','4','5','7','8','9','10']
    prdlist183 = ['1']
    prdlist188 = ['4','5','8','10']
    prdlist189 = ['1','2','4','5','8','9','10']
    productionlists = [prdlist183, prdlist188, prdlist189]

    #labels183 = ['S1','S2','S3','S4','S5','S7','S8','S9','S10']
    labels183 = ['S1']
    labels188 = ['S4','S5','S8','S10']
    labels189 = ['S1','S2','S4','S5', 'S8', 'S9', 'S10']
    labelslist = [labels183, labels188, labels189]


    for (sim, tlist, prdlist, labels, comp) in zip(simlist, timelists, productionlists, labelslist, complist):

        # Defining the lists to store the domain size of the last frame of each simulation
        # Chen et al., 2021
        sIfinal_sizelist  = []
        sIIfinal_sizelist = []

        for prd in prdlist:
            # Defining the lists to store the domain size of each simulation through time
            # Chen et al., 2021
            sIsizetlist     = []
            sIIsizetlist    = []

            # Defining the lists to store the degree of crystalinity of each simulation through time
            degree_cryst_sI_list  = []
            degree_cryst_sII_list = []

            if sim == "188":

                file1 = f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_1_dictionary.csv'
                file2 = f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_2_dictionary.csv'
                file3 = f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_3_dictionary.csv'
                files = [file1,file2,file3]
                print(f'SIM{sim}_{prd}')

                for fileindex,file in enumerate(files):
                    entrada = file

                    with open(entrada, 'r') as f:
                        csv = f.readlines()

                    with open("Dictionary_Files/csvvalues.csv", "w") as outfile:
                        with open("Dictionary_Files/tvalues.csv", "w") as times:
                            print(f'Reading dictionary files of SIM{sim}_{prd}_{fileindex+1}.')
                            with tqdm(total=len(csv)) as pbar:
                                for line in csv:
                                    if line.find('Time') != -1:
                                        times.write(line)
                                    elif ((line.find('Empty') == 1) or (line.find('C3H8') == 1) or (line.find(',CO2,') == 1)):
                                        outfile.write(line)

                                    pbar.update(1)

                    # Time and Number of Cages
                    column_names = ['Tname', 'Time', 'Ncagesname', 'NCages']
                    dftime = pd.read_csv('Dictionary_Files/tvalues.csv', header=None, \
                                         skiprows=0, delim_whitespace=False, names=column_names)
                    dftime = dftime.drop(['Tname', 'Ncagesname'], axis=1)

                    dftimecage = dftime[dftime['NCages'] != 0]
                    timeinit = []
                    timeinit = dftimecage['Time']*0.001
                    ncages = []
                    ncages = dftimecage['NCages']

                    timelist = []
                    ncageslist = []
                    print(f'Analyzing frame times and total number of cages per frame of SIM{sim}_{prd}_{fileindex+1}.')

                    with tqdm(total= (len(timeinit))) as pbar:
                        for t,nc in zip(timeinit,ncages):
                            for i in range(0,nc,1):
                                timelist.append(t)
                                ncageslist.append(nc)
                            pbar.update(1)

                    # Main Dataframe
                    column_names = ['Cage ID','Water Molecules','Cage Type','Guest',\
                                    'Guest number']
                    dfx = pd.read_csv(file, header=None, skiprows=0, delim_whitespace=False, names=column_names)

                    dfx = dfx[dfx['Cage ID'] != 'Cage ID']
                    dfx = dfx[dfx['Cage ID'] != 'Time']

                    dfx['Time (ns)'] = timelist
                    dfx['Number of Cages in frame'] = ncageslist
                    dfx.reset_index(inplace=True, drop=True)
                    dfx = dfx.iloc[:, [5,6,0,1,2,3,4]]
                    if fileindex == 0:
                        df = dfx[dfx['Time (ns)'] != 3000]
                    elif fileindex == 1:
                        dfx = dfx[dfx['Time (ns)'] != 6000]
                        df = df._append(dfx)
                    elif fileindex == 2:
                        df = df._append(dfx)

            else:
                file = f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_dictionary.csv'

                print(f'SIM{sim}_{prd}')
                entrada = file

                with open(entrada, 'r') as f:
                    csv = f.readlines()

                with open("Dictionary_Files/csvvalues.csv", "w") as outfile:
                    with open("Dictionary_Files/tvalues.csv", "w") as times:
                        print(f'Reading dictionary files of SIM{sim}_{prd}.')
                        with tqdm(total=len(csv)) as pbar:
                            for line in csv:
                                if line.find('Time') != -1:
                                    times.write(line)
                                elif ((line.find('Empty') == 1) or (line.find('C3H8') == 1) or (line.find(',CO2,') == 1)):
                                    outfile.write(line)

                                pbar.update(1)

                # Time and Number of Cages
                column_names = ['Tname', 'Time', 'Ncagesname', 'NCages']
                dftime = pd.read_csv('Dictionary_Files/tvalues.csv', header=None, \
                                     skiprows=0, delim_whitespace=False, names=column_names)
                dftime = dftime.drop(['Tname', 'Ncagesname'], axis=1)

                dftimecage = dftime[dftime['NCages'] != 0]
                timeinit = []
                timeinit = dftimecage['Time']*0.001
                ncages = []
                ncages = dftimecage['NCages']

                timelist = []
                ncageslist = []
                print(f'Analyzing frame times and total number of cages per frame of SIM{sim}_{prd}.')
                with tqdm(total= (len(timeinit))) as pbar:
                    for t,nc in zip(timeinit,ncages):
                        for i in range(0,nc,1):
                            timelist.append(t)
                            ncageslist.append(nc)
                        pbar.update(1)

                # Main Dataframe
                column_names = ['Cage ID','Water Molecules','Cage Type','Guest',\
                                'Guest number']

                dtype = {'Cage ID':str,'Water Molecules':object,'Cage Type':str,'Guest':str,\
                                'Guest number':str}

                df = pd.read_csv(file, header=None, skiprows=0, delim_whitespace=False, \
                                 names=column_names, dtype=dtype)

                df = df[df['Cage ID'] != 'Cage ID']
                df = df[df['Cage ID'] != 'Time']

                df['Time (ns)'] = timelist
                df['Number of Cages in frame'] = ncageslist
                df.reset_index(inplace=True, drop=True)
                df = df.iloc[:, [5,6,0,1,2,3,4]]

            ###############################################################################
            ################## ANALYSIS OF CAGE CONNECTIVITIES ############################
            ###############################################################################
            
            print(f'Analyzing all frames of SIM{sim}_{prd}.')
            with tqdm(total=len(tlist)) as pbar:
                for t in tlist:

                    #PARTE 1  ######################################################################################
                    dft = df[df['Time (ns)'] == t]
                    cagewaterlist = []

                    for lista in dft['Water Molecules']:
                        lista.replace("[","")
                        lista.replace("]","")
                        lista.split(", ")
                        cagewaterlist.append(lista)

                    alist      = []
                    index1list = []
                    index2list = []
                    facelist   = []

                    for index, i in enumerate(cagewaterlist):
                        for index2,j in enumerate(cagewaterlist):
                            listtest = (list(set(i) & set(j)))
                            if index < index2:
                                if listtest != []:
                                    index1list.append(index)
                                    index2list.append(index2)
                                    #alist.append(str(index)+'&'+str(index2))
                                    alist.append(list(set(i) & set(j)))
                                    facelist.append(len(list(set(i) & set(j))))

                    #PARTE 2  ######################################################################################

                    dfcc = pd.DataFrame()
                    dfcc['1st Cage ID'] = index1list
                    dfcc['2nd Cage ID'] = index2list
                    dfcc['Common H2O mol'] = alist
                    dfcc['Face'] = facelist

                    type1list  = []
                    guest1list = []
                    type2list  = []
                    guest2list = []

                    for id in dfcc['1st Cage ID']:
                        type1  = dft.loc[dft['Cage ID'] == str(id),'Cage Type'].values[0]
                        guest1 = dft.loc[dft['Cage ID'] == str(id),'Guest'].values[0]
                        type1list.append(type1)
                        guest1list.append(guest1)

                    for id in dfcc['2nd Cage ID']:
                        type2  = dft.loc[dft['Cage ID'] == str(id),'Cage Type'].values[0]
                        guest2 = dft.loc[dft['Cage ID'] == str(id),'Guest'].values[0]
                        type2list.append(type2)
                        guest2list.append(guest2)

                    dfcc['1st Cage Type']  = type1list
                    dfcc['2nd Cage Type']  = type2list
                    dfcc['1st Cage Guest'] = guest1list
                    dfcc['2nd Cage Guest'] = guest2list

                    ###############################################################################
                    ###########################  STRUCTURES DOMAINS (CHEN 2021) ###################
                    ###############################################################################

                    ### sI Domain

                    # Build a dataframe with only connections between hexagonal faces of 5¹²6² cages
                    dfcc666  = dfcc[((dfcc['Face'] == 6) & (dfcc['1st Cage Type'] == str(6)) & \
                                    (dfcc['2nd Cage Type'] == str(6)))]

                    # Make a list of connected 5¹²6² cages IDs
                    cageid666list = []
                    for id666 in dfcc666['1st Cage ID']:
                        if id666 not in cageid666list:
                            cageid666list.append(id666)
                    for id666 in dfcc666['2nd Cage ID']:
                        if id666 not in cageid666list:
                            cageid666list.append(id666)



                    # Build a dataframe with the connections of the cages in the list
                    dfccsI = dfcc[((dfcc['1st Cage ID'].isin(cageid666list)) | \
                                   (dfcc['2nd Cage ID'].isin(cageid666list)))]

                    dfccsI = dfccsI[((dfccsI['Face'] == 6) & (dfccsI['1st Cage Type'] == '6') & \
                                    (dfccsI['2nd Cage Type'] == '6')) | \
                                   ((dfccsI['Face'] == 5) & (dfccsI['1st Cage Type'] == '4') & \
                                    (dfccsI['2nd Cage Type'] == '6'))| \
                                   ((dfccsI['Face'] == 5) & (dfccsI['1st Cage Type'] == '6') & \
                                    (dfccsI['2nd Cage Type'] == '4'))]

                    cageidsIlist = []

                    for idsI in dfccsI['1st Cage ID']:
                        if idsI not in cageidsIlist:
                            cageidsIlist.append(idsI)
                    for idsI in dfccsI['2nd Cage ID']:
                        if idsI not in cageidsIlist:
                            cageidsIlist.append(idsI)
                    sIsizetlist.append(len(cageidsIlist))

                    # Count 5¹² and 5¹²6² cages in the detected domain for degree of crystallinity
                    cagedoclist = []
                    for iddoc in dfccsI['1st Cage ID']:
                        if iddoc not in cagedoclist:
                            cagedoclist.append(iddoc)
                    for iddoc in dfccsI['2nd Cage ID']:
                        if iddoc not in cagedoclist:
                            cagedoclist.append(iddoc)
                    NsI512list = []
                    NsI51262list = []
                    for iddoc in cagedoclist:
                        type  = dft.loc[dft['Cage ID'] == str(iddoc),'Cage Type'].values[0]
                        if type == '4':
                            NsI512list.append(iddoc)
                        elif type == '6':
                            NsI51262list.append(iddoc)

                    NsI512 = len(NsI512list)
                    NsI51262 = len(NsI51262list)


                    # Get the cages from dft4 that have water molecules in common with the list created

                    ### sII Domain

                    # Build a dataframe with only connections between hexagonal faces of 5¹²6² cages
                    dfcc6610  = dfcc[((dfcc['Face'] == 6) & (dfcc['1st Cage Type'] == str(10)) & \
                                    (dfcc['2nd Cage Type'] == str(10)))]

                    # Make a list of connected 5¹²6² cages IDs
                    cageid6610list = []
                    for id6610 in dfcc6610['1st Cage ID']:
                        if id6610 not in cageid6610list:
                            cageid6610list.append(id6610)
                    for id6610 in dfcc6610['2nd Cage ID']:
                        if id6610 not in cageid6610list:
                            cageid6610list.append(id6610)

                    dfccsII = dfcc[((dfcc['1st Cage ID'].isin(cageid6610list)) | \
                                   (dfcc['2nd Cage ID'].isin(cageid6610list)))]

                    dfccsII = dfccsII[((dfccsII['Face'] == 6) & (dfccsII['1st Cage Type'] == '10') & \
                                    (dfccsII['2nd Cage Type'] == '10')) | \
                                   ((dfccsII['Face'] == 5) & (dfccsII['1st Cage Type'] == '4') & \
                                    (dfccsII['2nd Cage Type'] == '10'))| \
                                   ((dfccsII['Face'] == 5) & (dfccsII['1st Cage Type'] == '10') & \
                                    (dfccsII['2nd Cage Type'] == '4'))]

                    cageidsIIlist = []
                    for idsII in dfccsII['1st Cage ID']:
                        if idsII not in cageidsIIlist:
                            cageidsIIlist.append(idsII)
                    for idsII in dfccsII['2nd Cage ID']:
                        if idsII not in cageidsIIlist:
                            cageidsIIlist.append(idsII)

                    sIIsizetlist.append(len(cageidsIIlist))

                    # Count 5¹² and 5¹²6⁴ cages in the detected domain for degree of crystallinity
                    cagedoclist = []
                    for iddoc in dfccsII['1st Cage ID']:
                        if iddoc not in cagedoclist:
                            cagedoclist.append(iddoc)
                    for iddoc in dfccsII['2nd Cage ID']:
                        if iddoc not in cagedoclist:
                            cagedoclist.append(iddoc)
                    NsII512list = []
                    NsII51264list = []
                    for iddoc in cagedoclist:
                        type  = dft.loc[dft['Cage ID'] == str(iddoc),'Cage Type'].values[0]
                        if type == '4':
                            NsII512list.append(iddoc)
                        elif type == '10':
                            NsII51264list.append(iddoc)

                    NsII512 = len(NsII512list)
                    NsII51264 = len(NsII51264list)

                    if NsI51262 > 0:
                        degree_cryst_sI  = NsI512/(12*NsI51262)
                    else:
                        degree_cryst_sI  = 0

                    if NsII51264 > 0:
                        degree_cryst_sII = NsII512/(12*NsII51264)
                    else:
                        degree_cryst_sII  = 0

                    degree_cryst_sI_list.append(degree_cryst_sI)
                    degree_cryst_sII_list.append(degree_cryst_sII)

                    if t == tlist[-1]:

                        ############################## OUTSIDE CAGE LAYER OF THE DOMAIN################
                        dflayersI = dfcc[((dfcc['1st Cage ID'].isin(cageidsIlist)) | \
                                   (dfcc['2nd Cage ID'].isin(cageidsIlist)))]
                        layersIlist = []
                        for layeridsI in dflayersI['1st Cage ID']:
                            if layeridsI not in cageidsIlist:
                                layersIlist.append(layeridsI)
                        for layeridsI in dflayersI['2nd Cage ID']:
                            if layeridsI not in cageidsIlist:
                                layersIlist.append(layeridsI)

                        layersIcagetypes = []
                        for i in layersIlist:
                            layertype = dft.loc[dft['Cage ID'] == str(i),'Cage Type'].values[0]
                            if layertype not in layersIcagetypes:
                                layersIcagetypes.append(layertype)


                        dflayersII = dfcc[((dfcc['1st Cage ID'].isin(cageidsIIlist)) | \
                                   (dfcc['2nd Cage ID'].isin(cageidsIIlist)))]
                        layersIIlist = []
                        for layeridsII in dflayersII['1st Cage ID']:
                            if layeridsII not in cageidsIIlist:
                                layersIIlist.append(layeridsII)
                        for layeridsII in dflayersII['2nd Cage ID']:
                            if layeridsII not in cageidsIIlist:
                                layersIIlist.append(layeridsII)

                        layersIIcagetypes = []
                        for i in layersIIlist:
                            layertype = dft.loc[dft['Cage ID'] == str(i),'Cage Type'].values[0]
                            if layertype not in layersIIcagetypes:
                                layersIIcagetypes.append(layertype)

                        ############################## OUTSIDE CAGE LAYER OF THE DOMAIN################

                        print(f'cageidsIlist = {cageidsIlist}')
                        print(f'cageidsIIlist = {cageidsIIlist}')
                        sImollist = []
                        for i in cageidsIlist:
                            watermol = dft.loc[dft['Cage ID'] == str(i),'Water Molecules'].values[0]
                            watermol.replace("[","")
                            watermol.replace("]","")
                            watermol.split(", ")
                            for j in watermol:
                                if j not in sImollist:
                                    sImollist.append(j)

                        sIImollist = []
                        for i in cageidsIIlist:
                            watermol = dft.loc[dft['Cage ID'] == str(i),'Water Molecules'].values[0]
                            watermol.replace("[","")
                            watermol.replace("]","")
                            watermol.split(", ")
                            for j in watermol:
                                if j not in sIImollist:
                                    sIImollist.append(j)

                        interfacecagelist = []
                        interfacecagelist.append(list(set(cageidsIlist) & set(cageidsIIlist)))
                        interfacemollist = []
                        for i in interfacecagelist[0]:
                            watermol = dft.loc[dft['Cage ID'] == str(i),'Water Molecules'].values[0]
                            watermol.replace("[","")
                            watermol.replace("]","")
                            watermol.split(", ")
                            for j in watermol:
                                if j not in interfacemollist:
                                    interfacemollist.append(j)

                        layersImollist = []
                        for i in layersIlist:
                            watermol = dft.loc[dft['Cage ID'] == str(i),'Water Molecules'].values[0]
                            watermol.replace("[","")
                            watermol.replace("]","")
                            watermol.split(", ")
                            for j in watermol:
                                if j not in layersImollist:
                                    layersImollist.append(j)

                        layersIImollist = []
                        for i in layersIIlist:
                            watermol = dft.loc[dft['Cage ID'] == str(i),'Water Molecules'].values[0]
                            watermol.replace("[","")
                            watermol.replace("]","")
                            watermol.split(", ")
                            for j in watermol:
                                if j not in layersIImollist:
                                    layersIImollist.append(j)

                        sImol = str(sImollist)
                        sImol.replace(',', '')
                        sImol.replace("'", '')
                        sImol.replace('[', '')
                        sImol.replace(']', '')

                        sIImol = str(sIImollist)
                        sIImol.replace(',', '')
                        sIImol.replace("'", '')
                        sIImol.replace('[', '')
                        sIImol.replace(']', '')

                        interfacemol = str(interfacemollist)
                        interfacemol.replace(',', '')
                        interfacemol.replace("'", '')
                        interfacemol.replace('[', '')
                        interfacemol.replace(']', '')

                        layersImol = str(layersImollist)
                        layersImol.replace(',', '')
                        layersImol.replace("'", '')
                        layersImol.replace('[', '')
                        layersImol.replace(']', '')

                        layersIImol = str(layersIImollist)
                        layersIImol.replace(',', '')
                        layersIImol.replace("'", '')
                        layersIImol.replace('[', '')
                        layersIImol.replace(']', '')


                        #SALVAR NA PASTA DO ARQUIVO XTC
                        '''with open(f"SIM{sim}_TRAJ/{prd}/{sim}_{prd}.vmd", 'w') as f:
                            f.write(f"# Current simulation time : {t} ns\n")
                            f.write(f'# sI domain size :  {len(cageidsIlist)} cages\n')
                            f.write('\n')
                            f.write(f'atomselect macro f{t}_sI {{resid {sImol} and name OW}}\n')
                            f.write('\n')
                            f.write('\n')
                            f.write(f'# sII domain size :  {len(cageidsIIlist)} cages\n')
                            f.write('\n')
                            f.write(f'atomselect macro f{t}_sII {{resid {sIImol} and name OW}}\n')
                            f.write('\n')
                            f.write('\n')
                            f.write(f'# sI domain layer size :  {len(layersIlist)} cages\n')
                            f.write(f'# sI domain layer cage types :  {layersIcagetypes} cages\n')
                            f.write('\n')
                            f.write(f'atomselect macro f{t}_sI_Layer {{resid {layersImol} and name OW}}\n')
                            f.write('\n')
                            f.write('\n')
                            f.write(f'# sII domain layer size :  {len(layersIIlist)} cages\n')
                            f.write(f'# sII domain layer cage types :  {layersIIcagetypes} cages\n')
                            f.write('\n')
                            f.write(f'atomselect macro f{t}_sII_Layer {{resid {layersIImol} and name OW}}\n')
                            f.write('\n')
                            f.write('\n')
                            f.write(f'# sI - sII Interface :  {len(interfacecagelist[0])} cages\n')
                            f.write('\n')
                            f.write(f'atomselect macro f{t}_interface {{resid {interfacemol} and name OW}}\n')
                            f.write('\n')'''

                        sIfinal_sizelist.append(len(cageidsIlist))
                        sIIfinal_sizelist.append(len(cageidsIIlist))
                    pbar.update(1)

            # Graphs for Chen et al, 2021 domains

            window_size = 10
            tlist2 = tlist
            del tlist2[0:window_size-1]

            numbers_series = pd.Series(sIsizetlist)
            windows = numbers_series.rolling(window_size)
            moving_averages = windows.mean()
            moving_averages_list = moving_averages.tolist()
            sIsizeMA = moving_averages_list[window_size - 1:]

            numbers_series = pd.Series(sIIsizetlist)
            windows = numbers_series.rolling(window_size)
            moving_averages = windows.mean()
            moving_averages_list = moving_averages.tolist()
            sIIsizeMA = moving_averages_list[window_size - 1:]

            numbers_series = pd.Series(degree_cryst_sI_list)
            windows = numbers_series.rolling(window_size)
            moving_averages = windows.mean()
            moving_averages_list = moving_averages.tolist()
            degree_cryst_sI_list_MA = moving_averages_list[window_size - 1:]

            numbers_series = pd.Series(degree_cryst_sII_list)
            windows = numbers_series.rolling(window_size)
            moving_averages = windows.mean()
            moving_averages_list = moving_averages.tolist()
            degree_cryst_sII_list_MA = moving_averages_list[window_size - 1:]

            color_cycle = itertools.cycle(['#2964A4', '#AC383A', '#449351', '#DC933B', '#626262', \
                                       "purple", "black",  "teal", "pink", "brown", "yellow"])

            plt.figure(figsize=(4, 4))
            gs = gridspec.GridSpec(1, 1, height_ratios=[1])
            ax0 = plt.subplot(gs[0])
            ax0.plot(tlist2, sIsizeMA, label=f'sI Size',color=next(color_cycle))
            ax0.plot(tlist2, sIIsizeMA, label=f'sII Size',color=next(color_cycle))
            ax0.set_ylabel('Domain size [Nº of cages]', fontproperties=font)
            ax0.set_xlabel('Time [ns]', fontproperties=font)
            ax0.set_ylim(0,20)

            color_cycle = itertools.cycle(['#2964A4', '#AC383A', '#449351', '#DC933B', '#626262', \
                                           "purple", "black",  "teal", "pink", "brown", "yellow"])
            ax1 = ax0.twinx()
            ax1.plot(tlist2, degree_cryst_sI_list_MA, label=f'sI Degree', color="teal", linestyle = '--')
            ax1.plot(tlist2, degree_cryst_sII_list_MA, label=f'sII Degree', color="pink", linestyle = '--')
            ax1.set_ylabel('Degree of Crystallinity', fontproperties=font)
            ax1.set_ylim(0,1)
            if sim == '188':
                plt.xlim(0, 8000)
            else:
                plt.xlim(0, 3000)
            linesleg, labelsleg = ax0.get_legend_handles_labels()
            lines2leg, labels2leg = ax1.get_legend_handles_labels()
            leg = ax1.legend(linesleg + lines2leg, labelsleg + labels2leg, \
                             loc='center left', bbox_to_anchor=(1.2, 0.5))
            for line in leg.get_lines():
                line.set_linewidth(3.0)
            plt.title(f'Simulation {prd} ({comp})')
            '''plt.savefig(f'SIM{sim}_TRAJ/{sim}_{prd}_Domains_Time.png', format='png', bbox_inches='tight',
                        dpi=300, transparent=False)'''
            plt.show()

        # Bar plot graph for Chen et. al, 2021 method

        plt.figure(figsize=(4, 4))
        gs = gridspec.GridSpec(1, 1, height_ratios=[1])
        ax0 = plt.subplot(gs[0])
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        rects1 = ax0.bar(x - width/2, sIfinal_sizelist, width, label='sI Domain',color='#2964A4')
        rects2 = ax0.bar(x + width/2, sIIfinal_sizelist, width, label='sII Domain',color='#AC383A')
        ax0.set_ylabel('Number of Cages')
        ax0.set_xticks(x)
        ax0.set_xticklabels(labels)
        ax0.legend()
        plt.title(f'({comp})')
        '''plt.savefig(f'SIM{sim}_TRAJ/{sim}_Domains.png', format='png', bbox_inches='tight',
                        dpi=300, transparent=False)'''
        plt.show()

if __name__ == '__main__':
    main()
