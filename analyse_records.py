# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:20:03 2020

@author: Will
"""

from collections import defaultdict
from save_output import save, load
from experiments import Experiment
from setting import Setting
from plots import plot_q, plot_action
from games import PD, SignalPD
from stats import *
from joint_strategy import find_JS, find_trial

['A00', 'A01', 'A02', 'A03']
['A11', 'A12', 'A13']
['B00', 'B01', 'B02', 'B03']
['B11', 'B12', 'B13']
['A13b', 'A13c']
['B11b', 'B12b', 'B13b']
['B11c', 'B12c', 'B13c']
['B11d', 'B12d', 'B13d']

for x in ['B00', 'B01', 'B02', 'B03']:
    r = load(x)
    print('Experiment:', x)
    a = aggr_avg_rewards(calc_avg_rewards(r))
    print('Avg. rewards:', a)
    o = aggr_outcome_prob(calc_outcome_prob(r))
    print('Outcome prob:', o)
    
    plot_action(r)

    #print(find_JS(r), '\n')

#k = []
#for i in range(len(r['outcomes'])):
#    if r['outcomes'][i][-1][-1][-1] == ('c'):
#        print(i)
#        k.append(i)

#plot_q(r, trial = k[1])



# Record strategies in experiment 2b
#find_JS(r)