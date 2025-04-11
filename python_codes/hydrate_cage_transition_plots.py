#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 16:11:05 2025

@author: arthurweidmann
"""

# In this code I sum the total number of transitions and the total number of cage
# occurrences (each frame occurrence is counted) to generate a probability of transition

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib
from matplotlib import gridspec
from operator import add
import math
import csv

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

    transition_time_limit = 0.5  # ns
    transition_number_limit = 4  # water molecules
    cage_life_minimum = 0.5  # ns

    simlist = ['188', '183', '189']
    complist = ['1:2', '1:1', '2:1']

    tlist183 = list(np.arange(0, 3001, 1))
    tlist188 = list(np.arange(0, 8001, 1))
    tlist189 = list(np.arange(0, 3001, 1))
    timelists = [tlist188, tlist183,  tlist189]

    prdlist183 = ['1', '2', '3', '4', '5', '7', '8', '9', '10']
    prdlist188 = ['4', '5', '8', '10']
    prdlist189 = ['1', '2', '4', '5', '8', '9', '10']

    productionlists = [prdlist188, prdlist183,  prdlist189]

    guest_list = ['Total', 'CO2', 'C3H8']

    df_column_names = ['Time(ns)', 'type', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                       'Empty', 'Occupied', 'LCC', 'N_cluster', 'Ncages', '2nd', '3rd']

    df_transitions_columns_names = ['Initial Cage Type', 'Final Cage Type', 'Guest Type', 'Guest',
                                    'Added H2O', 'Removed H2O', 'Number of Common H2O',
                                    'Different H2O', 'Initial Time', 'Final Time',
                                    'Initial Water Molecules', 'Final Water Molecules',
                                    'Size Cage 1', 'Size Cage 2', 'Cage Life Time',
                                    'Cage Transition', 'Transition time',
                                    'Number of cages difference']

    df_transitions_dtype = {'Initial Cage Type': str, 'Final Cage Type': str, 'Guest Type': str,
                            'Guest': str, 'Added H2O': object, 'Removed H2O': object,
                            'Number of Common H2O': str, 'Different H2O': object,
                            'Initial Time': float, 'Final Time': float,
                            'Initial Water Molecules': object, 'Final Water Molecules': object,
                            'Size Cage 1': int, 'Size Cage 2': int, 'Cage Transition': str,
                            'Cage Life Time': float, 'Transition time': float,
                            'Number of cages difference': int}

    for guest in guest_list:
        flat_list_total = []
        cages = []
        for cage in np.arange(0, 11, 1):
            cages.append([])
        for (sim, tlist, prdlist, comp) in zip(simlist, timelists, productionlists, complist):
            transition_list_backup = []
            print(f"{sim}")

            for prd in prdlist:
                file = f'SIM{sim}_TRAJ/SIM{sim}_{prd}_Cage_Transitions_UPDATED.csv'
                df_transitions_test = pd.read_csv(file, header=None, skiprows=1,
                                                  delim_whitespace=False,
                                                  names=df_transitions_columns_names,
                                                  dtype=df_transitions_dtype)

                df_transitions_test['Cage Transition'] = \
                    df_transitions_test['Initial Cage Type'].astype(str) + \
                    u'\u2192' + \
                    df_transitions_test['Final Cage Type'].astype(str)

                transition_list_backup.extend(df_transitions_test['Cage Transition'].unique())

            transition_list = list(set(transition_list_backup))
            transition_list.sort()
            transition_countlist = []
            for i, transition in enumerate(transition_list):
                transition_countlist.append([])

            for prd in prdlist:
                print(prd)

                # Obter listas das moléculas de água sem repetições que formaram cavidades 
                # ao redor de cada guest
                if sim == '188':

                    df1 = pd.read_csv(f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_1.csv', skiprows=1,
                                      names=df_column_names)
                    df2 = pd.read_csv(f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_2.csv', skiprows=1,
                                      names=df_column_names)
                    df3 = pd.read_csv(f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}_3.csv', skiprows=1,
                                      names=df_column_names)

                    frames = [df1, df2, df3]
                    df = pd.concat(frames)
                    df = df.dropna(how='any', axis=0)

                    file = f'SIM{sim}_TRAJ/SIM{sim}_{prd}_Cage_Transitions_UPDATED.csv'
                    df_initial = pd.read_csv(file, header=None, skiprows=1, delim_whitespace=False,
                                             dtype=df_transitions_dtype,
                                             names=df_transitions_columns_names)

                    df_initial2 = df_initial[df_initial['Transition time'] < transition_time_limit].copy()
                    df_initial22 = df_initial2[df_initial2['Cage Life Time'] >= cage_life_minimum].copy()
                    df_initial3 = df_initial22[df_initial22['Number of cages difference'] <= transition_number_limit].copy()

                    if guest == 'C3H8':
                        df_transitions_initial = df_initial3[df_initial3['Number of cages difference'] >= -transition_number_limit].copy()
                        df_transitions = df_transitions_initial[df_transitions_initial['Guest Type'] == 'C3H8'].copy()
                    elif guest == 'CO2':
                        df_transitions_initial = df_initial3[df_initial3['Number of cages difference'] >= -transition_number_limit].copy()
                        df_transitions = df_transitions_initial[df_transitions_initial['Guest Type'] == 'CO2'].copy()
                    else:
                        df_transitions = df_initial3[df_initial3['Number of cages difference'] >= -transition_number_limit].copy()

                    df_transitions['Cage Transition'] = df_transitions['Initial Cage Type'].astype(str) + u'\u2192' +\
                                                            df_transitions['Final Cage Type'].astype(str)

                    time_list = list(np.arange(0, 8001, 500))
                else:
                    columnnames = ['Time(ns)', 'type', '0', '1', '2', '3', '4', '5', '6', '7', '8',
                                   '9', '10', 'Empty', 'Occupied', 'LCC', 'N_cluster', 'Ncages',
                                   '2nd', '3rd']

                    df   = pd.read_csv(f'SIM{sim}_TRAJ/LCC_Data/SIM{sim}_{prd}.csv', skiprows=1, names=df_column_names)
                    df   = df.dropna(how='any', axis=0)


                    file = f'SIM{sim}_TRAJ/SIM{sim}_{prd}_Cage_Transitions_UPDATED.csv'
                    df_initial = pd.read_csv(file, header=None, skiprows=1, delim_whitespace=False, \
                                                 dtype=df_transitions_dtype, names=df_transitions_columns_names)

                    df_initial2 = df_initial[df_initial['Transition time'] < transition_time_limit].copy()
                    df_initial22 = df_initial2[df_initial2['Cage Life Time'] >= cage_life_minimum].copy()
                    df_initial3 = df_initial22[df_initial22['Number of cages difference'] <= transition_number_limit].copy()

                    if guest == 'C3H8':
                        df_transitions_initial = df_initial3[df_initial3['Number of cages difference'] >= -transition_number_limit].copy()
                        df_transitions = df_transitions_initial[df_transitions_initial['Guest Type'] == 'C3H8'].copy()
                    elif guest == 'CO2':
                        df_transitions_initial = df_initial3[df_initial3['Number of cages difference'] >= -transition_number_limit].copy()
                        df_transitions = df_transitions_initial[df_transitions_initial['Guest Type'] == 'CO2'].copy()
                    else:
                        df_transitions = df_initial3[df_initial3['Number of cages difference'] >= -transition_number_limit].copy()

                    df_transitions['Cage Transition'] = df_transitions['Initial Cage Type'].astype(str) + u'\u2192' +\
                                                            df_transitions['Final Cage Type'].astype(str)
                    time_list = list(np.arange(0,3001,500))

                for i,transition in enumerate(transition_list):
                    df_transitions2 = df_transitions[df_transitions['Cage Transition'] == transition]
                    transition_countlist[i].append(df_transitions2.shape[0])

                for cage in np.arange(0,11,1):
                    cages[cage].append(df[f'{str(cage)}'].sum())

            sumlist = []
            dict_list = []

            for i,transition in enumerate(transition_list):
                dict_list.append([])
                init, after = transition.split('→')

                transition_sum = sum(transition_countlist[i])

                if math.isfinite(sum(cages[int(init)])) & math.isfinite(transition_sum) & (sum(cages[int(init)]) != 0):
                    dict_list[i].append((transition_sum)/sum(cages[int(init)]))
                else:
                    dict_list[i].append(0)

                dict_list[i].append(transition_countlist[i])

            transition_dict = dict(zip(transition_list, dict_list))
            sorted_transition = sorted(transition_dict.items(),key=lambda x:x[1], reverse=True)
            sorted_transition_dict = dict(sorted_transition)

            ##############################################################################################
            filename = f"SIM{sim}_{guest}_Probabilities.csv"
            fields = ['Initial Cage', 'Final Cage', 'Probability']
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)

            for transition, probability in zip(sorted_transition_dict.keys(),sorted_transition_dict.values()):
                init, after = transition.split('→')
                row = [[init,after,str(probability[0])]]
                with open(filename, 'a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(row)
            ##############################################################################################

            labels = list(sorted_transition_dict.keys())
            ydata = []
            transitions_t = []
            for i,transition in enumerate(transition_list):
                ydatai = list(sorted_transition_dict.values())[i][0]
                ydata.append(ydatai)
                transitions_ti = list(sorted_transition_dict.values())[i][1]
                transitions_t.append(transitions_ti)

            size = len(labels)-1

            after_list = []
            flat_list = []

            for i in [0,1,2,3,4,5,6,7,8,9,10]:
                after_list.append([])
                flat_list.append([])
                for j in [0,1,2,3,4,5,6,7,8,9,10]:
                    after_list[i].append([])

            for key, value in transition_dict.items():
                init, after = key.split('→')
                after_list[int(after)][int(init)].append(value[0])
            for i in [0,1,2,3,4,5,6,7,8,9,10]:
                for j in [0,1,2,3,4,5,6,7,8,9,10]:
                    if not after_list[i][j]:
                        after_list[i][j] = [0]

            for i in [0,1,2,3,4,5,6,7,8,9,10]:
                flat_list[i] = np.concatenate(after_list[i]).tolist()

            flat_list_total.append(flat_list)

            color0 = '#AC383A'
            color1 = '#AC383A'
            color2 = '#AC383A'
            color3 = '#AC383A'
            color4 = '#449351'
            color5 = "gold"
            color6 = '#DC933B'
            color7 = 'cyan'
            color8 = '#2964A4'
            color9 = "purple"
            color10 = "black"

            color_list_updated = [color0, color1, color2, color3, color4, color5, color6, color7,
                                  color8, color9, color10]

            labels = ['4$^{3}$5$^{6}$', '4$^{3}$5$^{6}$6$^{1}$', '4$^{2}$5$^{8}$',
                      '4$^{2}$5$^{8}$6$^{1}$', '5$^{12}$', '4$^{1}$5$^{10}$6$^{2}$',
                      '5$^{12}$6$^{2}$', '4$^{1}$5$^{10}$6$^{3}$', '5$^{12}$6$^{3}$',
                      '4$^{1}$5$^{10}$6$^{4}$', '5$^{12}$6$^{4}$']

        figure_width = 3.5
        plt.figure(figsize=(figure_width, (figure_width*(2/3))))
        plt.tight_layout()
        params = {'mathtext.default': 'regular'}
        plt.rcParams.update(params)

        gs = gridspec.GridSpec(1, 1, height_ratios=[1])
        ax0 = plt.subplot(gs[0])
        x = np.arange(11)  # the label locations
        width = 0.25  # the width of the bars
        bottom_sum0 = [0,0,0,0,0,0,0,0,0,0,0]
        bottom_sum1 = [0,0,0,0,0,0,0,0,0,0,0]
        bottom_sum2 = [0,0,0,0,0,0,0,0,0,0,0]
        for i,j in zip([0,1,2,3,4,5,6,7,8,9,10],labels):
            if i < 3:
                ax0.bar(x - width, flat_list_total[0][i], width,bottom=bottom_sum0,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)
                ax0.bar(x, flat_list_total[1][i], width,bottom=bottom_sum1,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)
                ax0.bar(x + width, flat_list_total[2][i], width,bottom=bottom_sum2,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)
            elif i==3:
                ax0.bar(x - width, flat_list_total[0][i], width,bottom=bottom_sum0,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1, label='<5$^{12}$')
                ax0.bar(x, flat_list_total[1][i], width,bottom=bottom_sum1,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)
                ax0.bar(x + width, flat_list_total[2][i], width,bottom=bottom_sum2,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)
            elif i>3:
                ax0.bar(x -  width, flat_list_total[0][i], width,bottom=bottom_sum0,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1, label=j)
                ax0.bar(x, flat_list_total[1][i], width,bottom=bottom_sum1,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)
                ax0.bar(x + width, flat_list_total[2][i], width,bottom=bottom_sum2,color=color_list_updated[i],\
                    edgecolor = 'white',linewidth=1)

            bottom_sum0 = list(map(add, flat_list_total[0][i],bottom_sum0))
            bottom_sum1 = list(map(add, flat_list_total[1][i],bottom_sum1))
            bottom_sum2 = list(map(add, flat_list_total[2][i],bottom_sum2))

        if guest == 'Total':
            ax0.set_ylabel(f'Transition probability of \n occupied cages', fontproperties=font)
        elif guest == 'CO2':
            ax0.set_ylabel(f'Transition probability of \n $CO_{2}$ occupied cages', fontproperties=font)
        elif guest == 'C3H8':
            ax0.set_ylabel(f'Transition probability of \n $C_{3}$$H_{8}$ occupied cages', fontproperties=font)
        ax0.set_xticks(x)
        ax0.set_xticklabels(labels, rotation=60,fontproperties=font_tick,ha="right",rotation_mode="anchor")
        plt.ylim(0, 0.00032)
        plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(0, 0),useMathText=True)

        plt.savefig(f'{guest}_Cage_Transitions_Probability_ALL.png', format='png', \
                    bbox_inches='tight', dpi=600, transparent=False)
        plt.savefig(f'{guest}_Cage_Transitions_Probability_ALL.pdf', format='pdf', \
                    bbox_inches='tight', dpi=600, transparent=False) #SIM{sim}_TRAJ/
        plt.savefig(f'{guest}_Cage_Transitions_Probability_ALL.tiff', format='tiff', \
                    bbox_inches='tight', dpi=600, transparent=False)
        plt.show()

if __name__ == '__main__':
    main()