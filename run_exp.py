# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 19:48:56 2020

@author: Will
"""

from collections import defaultdict
from save_output import save, load
from experiments import Experiment
from setting import Setting
from plots import plot_q, plot_action
from games import PD, SignalPD
from stats import *


['A00', 'A01', 'A02', 'A03', 'A04']
['A11', 'A12', 'A13', 'A14']
['B00', 'B01', 'B02', 'B03', 'B04']
['B11', 'B12', 'B13', 'B14']
['A13b', 'A13c']
['B11b', 'B12b', 'B13b']
['B11c', 'B12c', 'B13c']
['B11d', 'B12d', 'B13d']


for x in ['C1102']:
    
    e = Experiment(x)
    
    if x in ['A13b', 'A13c', 'B11b', 'B12b', 'B13b', 'B11d', 'B12d', 'B13d']:
        e.run_experiment(trials = 1000, training_period = 20000)    
            
    else:
        e.run_experiment(trials = 1000)
    
    # With 1000 trials, keep only the last 1024 q_values (to reduce file size)
#    for trial in e.records['q_values']:
#        for player in e.records['q_values'][trial]:
#            
#            e.records['explore'][trial][player] = e.records['explore'][trial][player][-1024:]
#            e.records['action'][trial][player] = e.records['action'][trial][player][-1024:]
#            
#            for state in e.records['q_values'][trial][player]:
#                for action in e.records['q_values'][trial][player][state]:
#                    e.records['q_values'][trial][player][state][action] = e.records['q_values'][trial][player][state][action][-1024:]
                    
    save(e.records, x)
    
    #plot_q(exp[x].records)
    #plot_action(exp[x].records)
    print('Experiment:', x)
    a = aggr_avg_rewards(calc_avg_rewards(e.records))
    print('Avg. rewards:', a)
    o = aggr_outcome_prob(calc_outcome_prob(e.records))
    print('Outcome prob:', o, '\n')
