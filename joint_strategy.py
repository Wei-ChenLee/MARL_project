# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 19:17:31 2020

@author: Will
"""

import numpy as np
from NEv5 import *


def find_JS(r):
    ''' Find joint strategies learned given records r '''

    # Case: Experiment A01
    if r['info']['exp_id'] == 'A01':
        count = {}
        for i in range(1000):
            p = 0 # Only concerned with strategy of row player
            if r['q_values'][i][p][((0, 'c'),)]['c'][-1] > r['q_values'][i][p][((0, 'c'),)]['d'][-1]:
                if r['q_values'][i][p][((0, 'd'),)]['c'][-1] > r['q_values'][i][p][((0, 'd'),)]['d'][-1]:
                    a = 'ALC'
                else:
                    a = 'REP'
            else:
                if r['q_values'][i][p][((0, 'd'),)]['c'][-1] > r['q_values'][i][p][((0, 'd'),)]['d'][-1]:
                    a = 'SWI'
                else:
                    a = 'ALD'
            
            if a in count:
                count[a] += 1
            else:
                count[a] = 1
                
        return count
    
    # Case: Experiment B01
    elif r['info']['exp_id'] == 'B01':
        count = {}
        for i in range(1000):
            a = []
            for p in [0,1]:
                if r['q_values'][i][p][((0, 'c'),)]['c'][-1] > r['q_values'][i][p][((0, 'c'),)]['d'][-1]:
                    if r['q_values'][i][p][((0, 'd'),)]['c'][-1] > r['q_values'][i][p][((0, 'd'),)]['d'][-1]:
                        a.append('ALC')
                    else:
                        a.append('REP')
                else:
                    if r['q_values'][i][p][((0, 'd'),)]['c'][-1] > r['q_values'][i][p][((0, 'd'),)]['d'][-1]:
                        a.append('SWI')
                    else:
                        a.append('ALD')
            
            if "/".join(a) in count:
                count["/".join(a)] += 1
            else:
                count["/".join(a)] = 1
                
        return count

    # Case: Experiment A11
    elif r['info']['exp_id'] == 'A11':
        count = {}
        for i in range(1000):
            p = 0 # Only concerned with strategy of row player
            s = ((0, ('c', 'c')),)
            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                s = ((0, ('c', 'd')),)
                if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                    s = ((0, ('d', 'c')),)
                    if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'ALC'
                        else:
                            a = 'CCCD'
                    else:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'CCDC'
                        else:
                            a = 'CCDD'
                else:
                    s = ((0, ('d', 'c')),)
                    if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'CDCC'
                        else:
                            a = 'CDCD'
                    else:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'CDDC'
                        else:
                            a = 'CDDD'
            else:
                s = ((0, ('c', 'd')),)
                if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                    s = ((0, ('d', 'c')),)
                    if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'DCCC'
                        else:
                            a = 'DCCD'
                    else:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'DCDC'
                        else:
                            a = 'DCDD'
                else:
                    s = ((0, ('d', 'c')),)
                    if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'DDCC'
                        else:
                            a = 'DDCD'
                    else:
                        s = ((0, ('d', 'd')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            a = 'DDDC'
                        else:
                            a = 'ALD'
            
            if a in count:
                count[a] += 1
            else:
                count[a] = 1
        
        return count      
    
    
    # Case: Experiment B11
    elif r['info']['exp_id'] == 'B11':
        count = {}
        for i in range(1000):
            a = []
            for p in [0, 1]:
                s = ((0, ('c', 'c')),)
                if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                    s = ((0, ('c', 'd')),)
                    if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                        s = ((0, ('d', 'c')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('CCCC')                                    
                            else:
                                a.append('CCCD')
                        else:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('CCDC')
                            else:
                                a.append('CCDD')
                    else:
                        s = ((0, ('d', 'c')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('CDCC')
                            else:
                                a.append('CDCD')
                        else:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('CDDC')
                            else:
                                a.append('CDDD')
                else:
                    s = ((0, ('c', 'd')),)
                    if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                        s = ((0, ('d', 'c')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('DCCC')
                            else:
                                a.append('DCCD')
                        else:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('DCDC')
                            else:
                                a.append('DCDD')
                    else:
                        s = ((0, ('d', 'c')),)
                        if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('DDCC')
                            else:
                                a.append('DDCD')
                        else:
                            s = ((0, ('d', 'd')),)
                            if r['q_values'][i][p][s]['c'][-1] > r['q_values'][i][p][s]['d'][-1]:
                                a.append('DDDC')
                            else:
                                a.append('DDDD')
            
            if "/".join(a) in count:
                count["/".join(a)] += 1
            else:
                count["/".join(a)] = 1
        
        return count      
        
    
    # For all other cases of 'A'
    elif r['info']['exp_id'][0] == 'A':
        count = {}
        for i in range(1000):
            p = 0 # Only concerned with strategy of row player
            a = 'ALC'
            for s in r['q_values'][i][p]:    
                if r['q_values'][i][p][s]['c'][-1] < r['q_values'][i][p][s]['d'][-1]:
                    a = 'NALC'
                    break
                
            if a in count:
                count[a] += 1
            else:
                count[a] = 1
        
        return count      
    
    # For all other cases of 'B'
    elif r['info']['exp_id'][0] == 'B':
        count = {}
        for i in range(1000):
            a = []
            for p in [0, 1]:
                for s in r['q_values'][i][p]:    
                    if r['q_values'][i][p][s]['c'][-1] < r['q_values'][i][p][s]['d'][-1]:
                        a.append('NALC')
                        break
                if len(a) < p+1:
                    a.append('ALC')
            
            if "/".join(a) in count:
                count["/".join(a)] += 1
            else:
                count["/".join(a)] = 1
                
        return count      


def find_sink(count):
    ''' Return sink states for the list of joint strategies in count '''
    map = {}    
    for s in count.keys():
        # Generate matrix for each policy
        mat = {}
        for p in [0, 1]:
            mat[p] = strat_to_mat(s[p*5:p*5 + 4], p)

        # Generate implied TS
        TS = mat[0] * mat[1]

        # Find sink states
        if np.array_equal(np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 5)):
            map[s] = np.linalg.matrix_power(TS, 4)
        elif np.array_equal(np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 6)):
            map[s] = (np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 5))
        elif np.array_equal(np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 7)):
            map[s] = (np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 5), np.linalg.matrix_power(TS, 6))
        else:
            assert np.array_equal(np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 8))
            map[s] = (np.linalg.matrix_power(TS, 4), np.linalg.matrix_power(TS, 5), np.linalg.matrix_power(TS, 6), np.linalg.matrix_power(TS, 7))
    return map


def strat_to_mat(strat, player):
    ''' Return corresponding matrix of strategy, of mem 1 agents '''
    ''' Redundant: use gen_pol instead '''
    p = []
    for offset in range(4):
        if strat[offset] == 'C':
            if player == 0:
                p.append(np.array([1, 1, 0, 0]))
            else:
                p.append(np.array([1, 0, 1, 0]))
        
        elif strat[offset] == 'D':
            if player == 0:
                p.append(np.array([0, 0, 1, 1]))
            else:
                p.append(np.array([0, 1, 0, 1]))
    return np.array(p)

def stability(state, pol0, pol1):
    ''' Return whether state is stable given joint policy '''
    
    # If policies are in code, covert to matrix
    if type(pol0) == str:
        pol0 = gen_pol(0, pol0, 1)
    if type(pol1) == str:
        pol1 = gen_pol(1, pol1, 1)
    
    # Calculate true value about state
    val = q_val(state, pol0, pol1)
    
    # Get state index
    states = ['CC', 'CD', 'DC', 'DD']
    s_idx = states.index(state)
    
    # Check player deviation value
    if np.array_equal(pol0[s_idx], np.array([1, 1, 0, 0])):
        if np.array_equal(pol1[s_idx], np.array([1, 0, 1, 0])):
            # Prescribes CC
            row = 5 + 0.9 * q_val('DC', pol0, pol1)[0]   # Row deviation yields DC
            col = 5 + 0.9 * q_val('CD', pol0, pol1)[1]   # Col deviation yields CD
        else:
            # Prescribes CD
            row = 1 + 0.9 * q_val('DD', pol0, pol1)[0]   # Row deviation yields DD
            col = 3 + 0.9 * q_val('CC', pol0, pol1)[1]   # Col deviation yields CC
    else:
        if np.array_equal(pol1[s_idx], np.array([1, 0, 1, 0])):
            # Prescribes DC
            row = 3 + 0.9 * q_val('CC', pol0, pol1)[0]   # Row deviation yields CC
            col = 1 + 0.9 * q_val('DD', pol0, pol1)[1]   # Col deviation yields DD
        else:
            # Prescribes DD
            row = 0 + 0.9 * q_val('CD', pol0, pol1)[0]   # Row deviation yields CD
            col = 0 + 0.9 * q_val('DC', pol0, pol1)[1]   # Col deviation yields DC
    
    if row > val[0]:
        if col > val[1]:    
            return False, 'Both'
        else:
            return False, 'Row ' + str(row) + ' > ' + str(val[0])
    else:
        if col > val[1]:
            return False, 'Col ' + str(col) + ' > ' + str(val[1])
        else:
            return True, None


def find_trial(r):
    ''' Return indices of trials with pattern (CD, DD) from records r.
    For experiment B11 only.'''
    
    indices = []
    for i in range(len(r['outcomes'])):
        for t in range(10):
            if (r['outcomes'][i][t][1] == ('c', 'd') and 
                r['outcomes'][i][t+1][1] == ('d', 'd') and 
                r['outcomes'][i][t+2][1] == ('c', 'd')):
                print('found!')
                indices.append(i)
                break
    
    return indices
    
    
    
    
    
    

# Examples


#stability('DC', 'CDCC', 'DCDD')
#    
#for s in ['CCCC/CCDD', 'CCDC/CCDD', 'CCDD/CCDD', 'CDCC/CCCD', 'CDCD/CCCC', 'CDDC/CCDDC']:
#    print(s)
#    print(stability('CC', s[0:4], s[5:9]))
#
#for s in ['DDDD/DDDD', 'DDDD/CCDD', 'DDDD/CDCD', 'DDDD/CDDD', 'DDDD/DCCD', 
#          'DDDD/DCDD', 'DDDD/DDCD', 'CCCD/DDDD', 'CDDD/DDDD', 'CDDD/CDDD', 
#          'CDDD/DCDD', 'CDDD/DDCD', 'DCCD/DDDD', 'DCDD/DDDD', 'DCDD/DDCD', 
#          'DDCD/DDDD', 'DDCD/CCCD', 'DDCD/CDCD', 'DDCD/CDDD', 'DDCD/DDCD', 
#          'CCDD/CDCD', 'CCCD/DDDD']:
#    print(s)
#    print(stability('DD', s[0:4], s[5:9]))
#

   
    
    
        