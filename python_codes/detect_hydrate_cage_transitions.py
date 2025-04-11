#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 00:14:11 2024

@author: arthurweidmann
"""

from tqdm import tqdm
import pandas as pd
import numpy as np
import subprocess
import os
import itertools



def main():
    cage_life_limit = 1.0 # ns

    simlist = ['183','188','189']
    complist = ['1:1','1:2','2:1']

    tlist183 = list(np.arange(0,3001,1))
    tlist188 = list(np.arange(0,8001,1))
    tlist189 = list(np.arange(0,3001,1))
    timelists = [tlist183, tlist188, tlist189]

    prdlist183 = ['1','2','3','4','5','7','8','9','10']
    prdlist188 = ['4','5','8','10']
    prdlist189 = ['1','2','4','5','8','9','10']

    productionlists = [prdlist183, prdlist188, prdlist189]

    for (sim, tlist, prdlist, comp) in zip(simlist, timelists, productionlists, complist):
        for prd in prdlist:

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

                #df.to_csv("test_transition.csv")


            #Obter lista dos guests sem repetições em df
            guest_list = []

            for guest_number in df['Guest number']:
                if guest_number not in guest_list:
                    guest_list.append(guest_number)

            guest_list.remove('Empty')

            print(f'Analyzing all guests of SIM{sim}_{prd}.')
            #For each prd
            df_transitions = pd.DataFrame()
            cagetype1_list = []
            cagetype2_list = []
            watermol1_dflist = []
            watermol2_dflist = []
            time1_list = []
            time2_list = []
            guest_number_list = []
            guest_type_list = []
            diff_list = []
            common_water_list = []
            added_list = []
            remove_list = []
            cage_life_list = []
            cage1size = []
            cage2size = []

            with tqdm(total=len(guest_list)) as pbar:
                for i,guest_number in enumerate(guest_list):

                    dfguest = df[df['Guest number'] == guest_number]

                    dead_cage = False
                    watermollist = []
                    frame1_watermollist = []
                    common_water = []
                    z = 0

                    final_cage_time = 0
                    init_cage_time = 0
                    transition_count = 0
                    for index, row in dfguest.iterrows():
                        cagetype2           = row['Cage Type']
                        time2               = row['Time (ns)']
                        frame2_watermollist = []
                        # If first row on dataframe, get the same cage type since there is no transition
                        if z == 0:
                            cagetype1 = row['Cage Type']
                            guest_type = row['Guest']
                            time1 = 0
                            frame1_watermollist = []

                        watermol = row['Water Molecules'] #.values[0]
                        watermol = watermol.replace("[","")
                        watermol = watermol.replace("]","")
                        watermol = watermol.split(", ")
                        for j in watermol:
                            frame2_watermollist.append(j)
                            if j not in watermollist:
                                watermollist.append(j)
                        common_list = set(frame1_watermollist) & set(frame2_watermollist)
                        diff_mol    = list(set(frame1_watermollist).symmetric_difference(set(frame2_watermollist)))
                        added_mol  = list(set(diff_mol) & set(frame2_watermollist))
                        remove_mol = list(set(diff_mol) & set(frame1_watermollist))
                        # Get list of removed and added H2O molecules!!!!!!!
                        common_water.append(len(common_list))
                        if z > 0:
                            # Here we verify if, in case the two cages are of the same type,
                            # the time that elapsed between them being verified is larger than
                            # the limit set by "cage_life_limit". If it is, we consider that
                            # the previous cage "died" (has dissociated) and then we save
                            # its lifetime.

                            if cagetype2 == cagetype1:
                                if ((time2 - time1) > cage_life_limit) & (dead_cage == False):

                                    final_cage_time = time1
                                    cage_life = final_cage_time - init_cage_time
                                    cage_life_list.append(cage_life)
                                    dead_cage = True

                            # Checking if the cages are different
                            else: #if cagetype2 != cagetype1:
                                # Considering that it is the same cage if it keeps at least 14 water
                                # molecules from the last frame
                                # UPDATE: By not considering this we comment the next line:
                                #if len(common_list) >= 14:
                                # If the cage is different, a possible transition is detected.
                                # To follow the end cage and evaluate it is longevity, we
                                # store it's initial simulation time in the variable init_cage_time
                                # When the next possible transition is verified,
                                # we store the its final time in the variable final_cage_time
                                # Then the cage lifetime is calculated.
                                # We only save the lifetime of the cage here if the end cage of the last
                                # transition wasn't verified to have "died" (dissociated) in the last IF.

                                if dead_cage == False:
                                    if transition_count > 0:
                                        final_cage_time = time1
                                        cage_life = final_cage_time - init_cage_time
                                        cage_life_list.append(cage_life)
                                    transition_count = transition_count + 1

                                init_cage_time = time2
                                cagetype1_list.append(cagetype1)
                                cagetype2_list.append(cagetype2)
                                watermol1_dflist.append(frame1_watermollist)
                                watermol2_dflist.append(frame2_watermollist)
                                time1_list.append(time1)
                                time2_list.append(time2)
                                guest_number_list.append(guest_number)
                                guest_type_list.append(guest_type)
                                diff_list.append(diff_mol)
                                common_water_list.append(len(common_list))
                                added_list.append(added_mol)
                                remove_list.append(remove_mol)
                                cage1size.append(len(list(set(frame1_watermollist))))
                                cage2size.append(len(list(set(frame2_watermollist))))
                                dead_cage = False
                        frame1_watermollist = []
                        frame1_watermollist.extend(frame2_watermollist)

                        cagetype1 = cagetype2
                        time1 = time2
                        z = z+1
                    pbar.update(1)
            columns_names = ['Initial Cage Type','Final Cage Type',  'Guest Type', 'Guest', \
                             'Added H2O','Removed H2O','Number of Common H2O','Different H2O','Initial Time',\
                             'Final Time','Initial Water Molecules', 'Final Water Molecules','Size Cage 1', \
                             'Size Cage 2','Cage Life Time']
            df_transitions = pd.DataFrame(list(zip(cagetype1_list,cagetype2_list,guest_type_list, \
                                                   guest_number_list, added_list, remove_list, \
                                                   common_water_list,diff_list,time1_list,time2_list, \
                                                    watermol1_dflist,watermol2_dflist,cage1size,\
                                                   cage2size,cage_life_list)),columns=columns_names)
            df_transitions['Cage Transition'] = df_transitions['Initial Cage Type'].astype(str) + \
                                                    df_transitions['Final Cage Type'].astype(str)

            df_transitions['Transition Time'] = df_transitions['Final Time'] - \
                                                    df_transitions['Initial Time']
            df_transitions['Number of cages difference'] = df_transitions['Size Cage 2'] - df_transitions['Size Cage 1']

            df_transitions.to_csv(f'SIM{sim}_TRAJ/SIM{sim}_{prd}_Cage_Transitions_UPDATED.csv')

if __name__ == '__main__':
    main()