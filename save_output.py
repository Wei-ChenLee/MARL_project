# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 18:10:27 2020

@author: Will
"""

import pickle

def save(d, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

def load(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        r = quick_fix(pickle.load(f))
        return r
    
def quick_fix(records):
    # Quick fix for missing initial Q-values in trial 0 before all states were established
    for agent_id in range(records['info']['num_players']):
            for state in records['q_values'][0][agent_id]:
                for action in records['q_values'][0][agent_id][state]:
                    diff = (records['info']['training_period'] + 1024 
                            - len(records['q_values'][0][agent_id][state][action]))
                    if diff > 0:
                        prepend = [records['q_values'][0][agent_id][state][action][0]] * diff
                        records['q_values'][0][agent_id][state][action] = (
                                prepend +
                                records['q_values'][0][agent_id][state][action])        
    return records