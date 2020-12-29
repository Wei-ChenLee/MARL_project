# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 21:25:07 2020

@author: Will
"""

import numpy as np
import itertools
import pickle


# Create dictionary of mapping states to vectors
vectors = {'CC':np.array([1, 0, 0, 0]),
           'CD':np.array([0, 1, 0, 0]),
           'DC':np.array([0, 0, 1, 0]),
           'DD':np.array([0, 0, 0, 1])}

for i, j in zip(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = 2), range(16)):
    vectors[i[0]+', '+i[1]] = np.zeros(16)
    vectors[i[0]+', '+i[1]][j] = 1

# Create dictionary of mapping vectors to states
code = {(1, 0, 0, 0):'CC',
        (0, 1, 0, 0):'CD',
        (0, 0, 1, 0):'DC',
        (0, 0, 0, 1):'DD'}    
for i, j in zip(range(16), itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = 2)):
    vec = np.zeros(16)
    vec[i] = 1
    code[tuple(vec)] = j[0]+', '+j[1]
    

# Create feasible transition in the case of dim 2
feasible_trans = np.array([[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                           [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                           [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                           [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                           [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                           [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                           [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                           [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                           [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                           [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                           [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                           [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                           [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                           [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                           [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]])


def s_space(mem):
    ''' Return the state space of a given memory size '''
    space = [np.zeros([4**mem]) for x in range(4**mem)]
    for x in range(4**mem):
        space[x][x] = 1
    return space

def c2v(code):
    ''' Return an array representing the state '''
    return vectors[code]

def v2c(vector):
    ''' Return the state code corresponding to the state vector '''
    return code[tuple(vector)]

def pol_matrix(pol, player_pos, dim):
    ''' Converts a policy (dictionary) into a policy matrix. Requires player
    position (0: row, 1: column) and dimension (0, 1 or 2)'''
    mat = np.zeros((len(pol), len(pol)))

    if dim <= 1:
        if player_pos == 0:
            for idx, outcome in enumerate(['CC', 'CD', 'DC', 'DD']):
                if pol[outcome] == 'C':
                    mat[idx][0] = 1
                    mat[idx][1] = 1
                elif pol[outcome] == 'D':
                    mat[idx][2] = 1
                    mat[idx][3] = 1
        elif player_pos == 1:
            for idx, outcome in enumerate(['CC', 'CD', 'DC', 'DD']):
                if pol[outcome] == 'C':
                    mat[idx][0] = 1
                    mat[idx][2] = 1
                elif pol[outcome] == 'D':
                    mat[idx][1] = 1
                    mat[idx][3] = 1
    
    elif dim == 2:
        if player_pos == 0:
            for idx, outcome in enumerate(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = 2)):
                if pol[outcome] == 'C':
                    for i in range(0, 8):
                        mat[idx][i] = 1
                elif pol[outcome] == 'D':
                    for i in range(8, 16):
                        mat[idx][i] = 1

        elif player_pos == 1:
            for idx, outcome in enumerate(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = 2)):
                if pol[outcome] == 'C':
                    for i in list(range(0, 4))+list(range(8, 12)):
                        mat[idx][i] = 1
                elif pol[outcome] == 'D':
                    for i in list(range(4, 8))+list(range(12, 16)):
                        mat[idx][i] = 1
                        
        # Remove infeasible transitions
        mat = mat * feasible_trans
    
#    # Check policy transitions to exactly two possible states
#    for row in mat:
#        assert np.sum(row) == 2
    
    return mat
        
def gen_pol(player_pos, pol_code, dim):
    '''Given a policy code and player position, returns policy matrix '''
    if pol_code == 'TFT':
        if dim == 1:
            if player_pos == 1:
                pol = {'CC':'C',
                       'CD':'C',
                       'DC':'D',
                       'DD':'D'}
            elif player_pos == 0:
                pol = {'CC':'C',
                       'CD':'D',
                       'DC':'C',
                       'DD':'D'}
        elif dim == 2:
            pol = {}
            for state in itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim):
                if player_pos == 1:
                    pol[state] = state[0][0]
                elif player_pos == 0:
                    pol[state] = state[0][1]

    elif pol_code == 'REP':
        if player_pos == 1:
            pol = {'CC':'C',
                   'CD':'D',
                   'DC':'C',
                   'DD':'D'}
        elif player_pos == 0:
            pol = {'CC':'C',
                   'CD':'C',
                   'DC':'D',
                   'DD':'D'}

    elif pol_code == 'SWI':
        if player_pos == 1:
            pol = {'CC':'D',
                   'CD':'C',
                   'DC':'D',
                   'DD':'C'}
        elif player_pos == 0:
            pol = {'CC':'D',
                   'CD':'D',
                   'DC':'C',
                   'DD':'C'}            

    elif pol_code == 'ALC':
        states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim))
        pol = {}
        for s in states:
            if dim <= 1:
                pol[s[0]] = 'C'
            else:
                pol[s] = 'C'

    elif pol_code == 'ALD':
        states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim))
        pol = {}
        for s in states:
            if dim <= 1:
                pol[s[0]] = 'D'
            else:
                pol[s] = 'D'
    
    else:
        if dim == 1 and len(pol_code) == 4:
            pol = {}
            for i, s in enumerate(['CC', 'CD', 'DC', 'DD']):
                pol[s] = pol_code[i]
    
    return pol_matrix(pol, player_pos, dim)

def reward(outcome):
    ''' Returns reward tuple given stage game outcome '''
    if len(outcome) == 16:
        out = np.array([np.sum(outcome[0:4])] + 
                       [np.sum(outcome[4:8])] + 
                       [np.sum(outcome[8:12])] + 
                       [np.sum(outcome[12:])])
    else:
        out = outcome
    rewards = np.array([[3, 3],
                        [0, 5],
                        [5, 0],
                        [1, 1]])
    return np.matmul(out, rewards)

def transition(state, pol0, pol1):
    ''' Returns transitioned state, given current state and policies '''
    trans_matrix = pol0 * pol1
    return np.matmul(state, trans_matrix)

def q_val(state, pol0, pol1, counter = 0, disc = 0.9):
    if type(state) == str:
        state = c2v(state)
    if type(pol0) == str:
        pol0 = gen_pol(0, pol0, 1)
    if type(pol1) == str:
        pol1 = gen_pol(1, pol1, 1)
    ''' Returns Q-value of state under a given pair of policies '''
    return tuple(np.round(q_calc(state, pol0, pol1, counter, disc), 2))

def q_calc(state, pol0, pol1, counter = 0, disc = 0.9):
    ''' Calculates Q-value (not rounded). Called by the function q_val. '''
    if counter == 60:
        return 0
    next_state = transition(state, pol0, pol1)
    next_next_state = transition(next_state, pol0, pol1)
    if np.array_equal(next_next_state, next_state):
        return reward(next_state)/(1-disc)
    elif np.array_equal(transition(next_next_state, pol0, pol1), next_state):
        return (reward(next_state) + disc * reward(next_next_state))/(1-disc**2)
    else:
        return reward(next_state) + disc * q_calc(next_state, pol0, pol1, counter + 1)

def is_BR(state, p0, p0_space, p1):
    ''' Returns True if p0 is a BR to p1 in state '''
    val = q_val(state, p0, p1)
    # Check possible deviations
    for p in p0_space:
        if q_val(state, p, p1)[0] > val[0] + 0.000000001:
            return False, 0, p
    # If no better move is found, confirm p0 is a BR in the current state
    return True, None, None

def is_NE(state, p0, p1, p0_space, p1_space):
    ''' Returns True if state and policy pair is a NE, false otherwise '''
    # If state is in code, convert to vector 
    if type(state) == str:
        state = c2v(state)
    if type(p0) == str:
        p0 = gen_pol(0, p0, 1)
    if type(p1) == str:
        p1 = gen_pol(1, p1, 1)

    val = q_val(state, p0, p1)
    # Check possible deviation for row player
    for p in p0_space:
        if q_val(state, p, p1)[0] > val[0] + 0.000000001:
            return False, 0, p
    
    # Check possible deviation for column player
    for p in p1_space:
        if q_val(state, p0, p)[1] > val[1]  + 0.000000001:
            return False, 1, p

    # If no better move is found, confirm state and policies constitute a NE
    return True, None, None


def is_NE_oneshot(state, p0, p1):
    ''' Returns True if state and policy pair is a NE, false otherwise '''
    # If state is in code, convert to vector 
    if type(state) == str:
        state = c2v(state)
    if type(p0) == str:
        p0 = gen_pol(0, p0, 1)
    if type(p1) == str:
        p1 = gen_pol(1, p1, 1)

    val = q_val(state, p0, p1)
    # Check one-shot deviation for row player
    i = list(state).index(1) # find state index
    p0_alt = np.copy(p0)
    k = np.ones(len(p0)) - p0[i]
    p0_alt[i] = k
    if len(p0) == 4**2:
        p0_alt = p0_alt * feasible_trans
        
    next_state = transition(state, p0_alt, p1)
    r = reward(next_state)
        
    if r[0] + 0.9 * q_val(next_state, p0, p1)[0] > val[0] + 0.000000001: # Consider only deviation about the current state (and not any subsequent states)
        return False, 0, p0_alt
#        if q_val(state, p0_alt, p1)[0] > val[0] + 0.000000001:
#            return False, 0, p0_alt
            
    # Check possible deviation for column player
    i = list(state).index(1) # find state index
    p1_alt = np.copy(p1)
    k = np.ones(len(p1)) - p1[i]
    p1_alt[i] = k
    if len(p1) == 4**2:
        p1_alt = p1_alt * feasible_trans
        
    next_state = transition(state, p0, p1_alt)
    r = reward(next_state)
        
    if r[1] + 0.9 * q_val(next_state, p0, p1)[1] > val[1] + 0.000000001: # Consider only deviation about the current state (and not any subsequent states)
        return False, 1, p1_alt
    # If no better move is found, confirm state and policies constitute a NE
    return True, None, None

def p_space(pos, mem, obs, dim):
    ''' Generates and returns a policy space, expressed in policy matrices '''
    actions = ['C', 'D']
    
    # If agent has no memory, adopt same policy space size as dim
    if mem == 0:
        if dim == 0:
            # If dim is also zero, use state space of dim 1
            states = ['CC', 'CD', 'DC', 'DD']
            space = [tuple(zip(states, x*len(states))) for x in actions]
        else:
            states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim))
            space = [tuple(zip(states, x*len(states))) for x in actions]

    # If agent can observe opponent actions, use full state space
    elif obs:
        if mem == dim:
            states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim))
            space = [tuple(zip(states, x)) for x in itertools.product(actions, repeat = len(states))]
            
        else:
            states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim))
            obs_states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = mem))
            obs_space = [tuple(zip(obs_states, x)) for x in itertools.product(actions, repeat = len(obs_states))]
            
            space = []
            for i in range(len(obs_space)):
                pol = []
                for s in states:
                    for o in obs_space[i]:
                        if s[0] == o[0][0]:
                            act = o[1]
                            pol.append(tuple([s, act]))
                space.append(tuple(pol))    
     
    # Else, restrict policy space to policies that only condition on own actions
    elif not obs: 
        if pos == 0:
            if mem == 1 and dim == 1:
                states = list(itertools.product(['CC', 'DC', 'CD', 'DD'], repeat = dim)) # size 4

            elif mem == 1 and dim == 2:
                rev_tuples = list(itertools.product(['CC', 'DC', 'CD', 'DD'], repeat = dim)) # size 16
                states = []
                for t in rev_tuples:
                    states.append(t[::-1])
                                
            elif mem == 2:
                states = (list(itertools.product(['CC', 'DC'], ['CC', 'DC'], repeat = dim-1)) +
                          list(itertools.product(['CC', 'DC'], ['CD', 'DD'], repeat = dim-1)) +
                          list(itertools.product(['CD', 'DD'], ['CC', 'DC'], repeat = dim-1)) +
                          list(itertools.product(['CD', 'DD'], ['CD', 'DD'], repeat = dim-1))) # size 16

            num_states = len(states)                
            subj_states = list(itertools.product(actions, repeat = mem)) # size 4
            num_subj_states = len(subj_states)            
            space = [tuple(zip(states, x * (num_states//num_subj_states))) for x in itertools.product(actions, repeat = num_subj_states)]
        
        elif pos == 1:
            if mem == 1 and dim == 1:
                states = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = mem))
                
                
            elif mem == 1 and dim == 2:
                rev_tuples = list(itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = dim))
                states = []
                for t in rev_tuples:
                    states.append(t[::-1])                
                                    
            elif mem == 2:
                states = (list(itertools.product(['CC', 'CD'], ['CC', 'CD'], repeat = mem-1)) +
                          list(itertools.product(['CC', 'CD'], ['DC', 'DD'], repeat = mem-1)) +
                          list(itertools.product(['DC', 'DD'], ['CC', 'CD'], repeat = mem-1)) +
                          list(itertools.product(['DC', 'DD'], ['DC', 'DD'], repeat = mem-1)))

            num_states = len(states)                
            subj_states = list(itertools.product(actions, repeat = mem)) # size 4
            num_subj_states = len(subj_states)            
            space = [tuple(zip(states, x * (num_states//num_subj_states))) for x in itertools.product(actions, repeat = num_subj_states)]
    
    pol_space = []
    for pol in space:
        p = {}
        for state_action_pair in pol:            
            if dim == 1:
                p[state_action_pair[0][0]] = state_action_pair[1]
            else:
                p[state_action_pair[0]] = state_action_pair[1]
        pol_space.append(p)

    pol_space_matrices = []
    for pol in pol_space:
        pol_space_matrices.append(pol_matrix(pol, pos, dim))
    
    return pol_space_matrices

def find_BR(dim, p_space, p1):
    ''' Return best reponses to p1 from p_space '''
    BR = {}
    for p in p_space:
        for s in s_space(dim):
            BR[s] = []
            if is_BR(s, p, p_space, p1)[0]:
                BR[tuple(s)].append(p)
    return BR

def tup(pol):
    ''' Returns policy or TS as a tuple for use as a dictionary key '''
    return tuple(map(tuple, pol))


def find_NE(p0_mem, p0_obs, p1_mem, p1_obs):
    ''' Returns NE of all policy pairs, for all states '''
    if p0_mem == 0 and p1_mem == 0:
        dim = 1
    else:
        dim = max(p0_mem, p1_mem)

    p_space0 = p_space(0, p0_mem, p0_obs, dim)
    p_space1 = p_space(1, p1_mem, p1_obs, dim)
    NE = {}
    
    # Loop through all policies and states to find NE
    pol = 0
    for p0 in p_space0:
        for p1 in p_space1:
            for s in s_space(dim):
                if is_NE(s, p0, p1, p_space0, p_space1)[0]:
                    if (tup(p0), tup(p1)) in NE:
                        NE[(tup(p0), tup(p1))].append(s)
                    else:
                        NE[(tup(p0), tup(p1))] = [s]
            print('Joint pol', pol)
            pol += 1
    return NE

def find_NE_oneshot(p0_mem, p0_obs, p1_mem, p1_obs):
    ''' Returns NE of all policy pairs, for all states '''
    if p0_mem == 0 and p1_mem == 0:
        dim = 1
    else:
        dim = max(p0_mem, p1_mem)

    p_space0 = p_space(0, p0_mem, p0_obs, dim)
    p_space1 = p_space(1, p1_mem, p1_obs, dim)
    NE = {}
    
    # Loop through all policies and states to find NE
    pol = 0
    for p0 in p_space0:
        for p1 in p_space1:
            for s in s_space(dim):
                if is_NE_oneshot(s, p0, p1)[0]:
                    if (tup(p0), tup(p1)) in NE:
                        NE[(tup(p0), tup(p1))].append(s)
                    else:
                        NE[(tup(p0), tup(p1))] = [s]
            print('Joint pol', pol)
            pol += 1
    return NE

def find_SPE(p0_mem, p0_obs, p1_mem, p1_obs):
    ''' Returns SPE of all policy pairs by checking for one-shot deviation.
    For each policy pair, check if one-shot deviation is profitable for either 
    player at each state. If no deviation is profitable, then joint policy is
    subgame perfect. '''
    if p0_mem == 0 and p1_mem == 0:
        dim = 1
    else:
        dim = max(p0_mem, p1_mem)

    p_space0 = p_space(0, p0_mem, p0_obs, dim)
    p_space1 = p_space(1, p1_mem, p1_obs, dim)
    SPE = []
    
    # For each policy pair
    for p0 in p_space0:
        for p1 in p_space1:
            # For each joint policy, consider check each state
            for s in s_space(dim):
                # Check if one-shot deviation is profitable
                if not is_SGP(s, (p0, p1))[0]:
                    break
            else:
                SPE.append([p0, p1])
    return SPE
    

def is_SGP(state, pol):
    ''' Check if one-shot deviation is profitable for either player, about the
    state given. Returns True or False. '''
    
    
    # Find state values of joint policy
    val = q_val(state, pol[0], pol[1])
    
    # Check one-shot deviation for both players:
    for player in [0, 1]:        
        i = list(state).index(1) # find state index
        p_alt = np.copy(pol[player])
        k = np.ones(len(pol[player])) - pol[player][i]
        p_alt[i] = k
        if len(pol[player]) == 4**2:
            p_alt = p_alt * feasible_trans
        
        if player == 0:
            next_state = transition(state, p_alt, pol[1])
        elif player == 1:
            next_state = transition(state, pol[0], p_alt)
        r = reward(next_state)
        
        # If profitable deviation exists, return false
        if r[player] + 0.9 * q_val(next_state, pol[0], pol[1])[player] > val[player] + 0.000000001:
            return False, player, p_alt
        
    # If no profitable deviation, return true
    return True, 0, 0


def is_cycle(pol, s, s_set, NE):
    # Check if s is already in s_set. If so, return s_set
    if v2c(s) in s_set:
        return s_set
    
    # Else, append s and check transition
    else:
        s_set.append(v2c(s))
        s = transition(s, np.array(pol[0]), np.array(pol[1]))
        
        if any((s == x).all() for x in NE[pol]):
        #if s in NE[pol]:
            return is_cycle(pol, s, s_set, NE)
        else:
            return None

def find_cycle(NE):
    cycle = {}
    for pol in NE:
        for s in NE[pol]:
            # If s is already in a cycle, then go to next state
            checked = False
            if pol in cycle:
                for sets in cycle[pol]:
                    #if s in sets:
                    if v2c(s) in sets:
                        checked = True
            if checked:
                break
            
            # Check if s is in a cycle. Returns a list of states in the cycle 
            # if so, or None if not.
            s_set = is_cycle(pol, s, [], NE)
            
            # If not in a cycle, break
            if not s_set:
                break
            
            # Else, add cycle to dictionary
            else:
                if pol in cycle:
                    cycle[pol].append(s_set)
                else:
                    cycle[pol] = [s_set]
    return cycle

def cycle(NE, idx = 'all'):
    cyc = find_cycle(NE)
    if idx == 'all':
        for j in cyc:
            print(j)
            print(cyc[j], "\n")
    else:
        for i, j in enumerate(cyc):
            if i == idx:
                print(j)
                print(cyc[j], "\n")

def SPE(NE):
    spe = []
    for ne in NE:
        num_states = len(NE[ne][0])
        if len(NE[ne]) == num_states:
            spe.append(ne)
    return spe
    
def dump(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(k)
                dump(v)
            else:
                print('%s : %s' % (k, v))
    elif isinstance(obj, list):
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v)
            else:
                print(v)
    else:
        print(obj)


#def save(d, name):
#    with open('nash/'+ name + '.pkl', 'wb') as f:
#        pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
#
#def load(name):
#    with open('obj/' + name + '.pkl', 'rb') as f:
#        return pickle.load(f)

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

def check_p_space(space, pos, mem, obs, dim):
    # Check dimension:
    subj_states = (2 * (2**obs))** dim
    num_actions = 2
    print('p_space should have size', num_actions ** subj_states, ', and have size', len(space))
    assert len(space) == num_actions ** subj_states
    
    # Check uniqueness
    assert len(set(totuple(space))) == len(space), 'Policies in space are not unique'
    
    # Check only controls own action
    
    # Check only controls observables

def gen_s(dim, pos):
    s = np.zeros(4**dim)
    s[pos] = 1
    return s

def term_TS(pol, repeat = None):
    if repeat == None:
        repeat = len(pol[0][0])
    if type(pol) == tuple:
        pol = np.array(pol)

    init = np.linalg.matrix_power(pol[0]*pol[1], repeat)
    t_states = [init]
    mat = np.matmul(init, pol[0]*pol[1])
    while not np.array_equal(mat, init):
        t_states.append(mat)
        mat = np.matmul(mat, pol[0]*pol[1])
    return t_states

def term_states(NE):
    for pol in NE:
        print()
        print(dump(np.array(pol)))
        for nash in NE[pol]:
            term_s = []
            for t_mat in term_TS(pol):
                term_s.append(np.matmul(nash, t_mat))
            print(v2c(nash), "-->", [v2c(x) for x in term_s])

def trunc_dict(NE, fro, to):
    return {x:y for x,y in list(NE.items())[fro:to]}

# Build experiments:
#
#t = {}
#agent = [(0, False), (1, False), (1, True), (2, False)]
#agents = list(itertools.product(agent, repeat = 2))
#
#for i, a in enumerate(agents):
#    t[i] =  {'p0_mem':a[0][0],
#             'p0_obs':a[0][1],
#             'p1_mem':a[1][0],
#             'p1_obs':a[1][1]}

#t[16] = {'p0_mem': 2, 'p0_obs': True, 'p1_mem': 0, 'p1_obs': False}
#n[16] = find_NE(**t[20])

#%%

# Run experiments

#ne = {}
#for i in t:
#    print(t[i])
#    ne[i] = find_NE_oneshot(**t[i])
    
#spe = {}
#for i in range(20):
#    print(f[i])
#    spe[i] = find_SPE(**f[i])

# spe[24] = find_SPE(**f[24])

#%%
#q_val(c2v('CD'), p0, p1)

## Test NE for Mem 2, Obs T and Mem 2, Obs 2
#p0_space = p_space(0, 2, True, 2)
#p1_space = p_space(1, 2, True, 2)
#
#is_NE(c2v('CC, CC'), gen_pol(0, 'ALD', 2), gen_pol(1, 'ALD', 2), p_space(0, 2, True, 2), p_space(1, 2, True, 2))

#is_NE_oneshot('CC', p[0], p[1])    


#%% Print SPEs

#f = {}
#agent = [(0, False), (1, False), (1, True), (2, False), (2, True)]
#agents = list(itertools.product(agent, repeat = 2))
#
#for i, a in enumerate(agents):
#    f[i] =  {'p0_mem':a[0][0],
#             'p0_obs':a[0][1],
#             'p1_mem':a[1][0],
#             'p1_obs':a[1][1]}
#
#ne = {}
#for i in range(4, ):
#    print(f[i])
#    ne[i] = find_NE_oneshot(**f[i])

#ne[9] = find_NE_oneshot(**f[9])

#for i in range(16):
#    print('Old SPEs:', len(SPE(n[i])))
#    print('New SPEs:', len(SPE(ne[i])))
    
#for s in itertools.product(['CC', 'CD', 'DC', 'DD'], repeat = 2):
#    print(is_NE(s, p0, p1, p_space(0, 2, True, 2), p_space(1, 0, False, 2)))


#p_space1 = p_space(1, 2, True, 2)
#
#s = set()
#for p in p_space1:
#    s.add(tup(p))
#
#print(len(s))
