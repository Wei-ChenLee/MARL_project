'''
This module contains the Agent class and its subclasses.

Game is an input to instantiate the class Agents.
Game and Agents are input to instantiate the class Settings.
'''

from collections import defaultdict
import random
from games import SignalPD

class Agent:
    ''' The base class for all agents. Has finite memory and plays repeated
    games (only one stage-game) '''
    def __init__(self, idx, game, memory, obs_opponents,
                 epsilon = 1, epsilon_decay = 0.999, 
                 learn_rate = 0.3, learn_rate_decay = 1,
                 disc_factor = 0.9):
        
        # Generate attributes
        self.records_other = defaultdict(list)
        self.records_q = dict()
        self.idx = idx
        self.game = game
        self.actions = game.players[idx].actions
        self.epsilon = epsilon
        self.learn_rate = learn_rate
        self.memory = memory * len(game.stages)
        self.obs_opponents = obs_opponents
        self.disc_factor = disc_factor
        self.init_epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.init_learn_rate = learn_rate
        self.learn_rate_decay = learn_rate_decay
        self.q_values = defaultdict(dict)
        #self.states = set(['null']) if memory == 0 else set()
        self.states = set()
                
#            if obs_opponents == 'all actions':
#                actions = [game.players[i].actions[0] for i in game.players]
#                stage_outcomes = list(itertools.product(*actions))
#                self.states = [s for s in itertools.product(stage_outcomes, 
#                                                            repeat = memory)]
#                #! Each state is a tuple of tuples
#            elif obs_opponents == 'own actions':
#                self.states = [s for s in itertools.product(self.actions, 
#                                                            repeat = memory)]
#                #! Each state is a tuple, rather than tuple of tuples
#        
#        # Build q-table as embedded dictionary using states and actions
#        self.q_values = dict()
#        for s in self.states:
#            self.q_values[s] = dict()
#            for a in self.actions:
#                self.q_values[s][a] = random.random()*0.1
            
        # To built states and q_values on the fly
                
    def history_to_state(self, history):
        ''' Given game history, return agent's perceived state '''
        
        # Case: no memory
        if self.memory == 0:
            #return 'null'
            return (0,)
        
        # Case: with memory & observes all opponents' actions
        elif self.obs_opponents == True:
            return tuple(history[-self.memory:])
        
        # Case: with memory, but cannot observe opponents' actions
        else:
            trunk = history[-self.memory:]
            state = []
            
            # Sub-case: can observe signals
            if isinstance(self.game, SignalPD):
                for h in trunk:
                    if h[0] == 1:  # Action phase in Signal PD
                        state.append((h[0], (h[1][self.idx],))) # Obs own action
                    else:  # Signal phase in Signal PD
                        state.append(h)  # Observes all signals
            
            # Sub-case: no signals to observe
            else:
                for h in trunk:
                    state.append((h[0], h[1][self.idx])) # Obs own action
        
            # Return truncated and partially obscured history as agent's state
            return tuple(state)

    def choose_action(self, history, stage):
        ''' Given history and stage game, use epsilon-greedy strategy to 
        choose and return an action. Q_values for the given state are 
        initialised on the fly. '''
        # Determine agent's perceived state given game history, add to states 
        state = self.history_to_state(history)
        self.states.add(state)
        
        # Determine whether to explore or exploit
        if random.random() < self.epsilon:
            # Explore, choose random action
            self.records_other['explore'].append(1)
            act = random.choice(tuple(self.actions[stage]))
            #print('Player', self.idx, 'explores, action =', act, '\n')
            
            # Generate default q_values for all actions in this state
            if self.q_values[state] == {}:
                for a in self.actions[stage]:
                    self.q_values[state].setdefault(a, random.random()*0.1)
     
        else:
            # Exploit, choose optimal action
            self.records_other['explore'].append(0)
            act, best_val = 'null', -1
            
            for a in self.actions[stage]:
                if self.q_values[state].setdefault(a, random.random()*0.1) \
                    >= best_val:
                    act = a
                    best_val = self.q_values[state][a]
            #print('Player', self.idx, 'exploits, action =', act, '\n')

        # Record
        self.records_other['action'].append(act)

        # Return chosen action
        return act

    def update_q(self, state_current, stage, act, reward, state_next):
        ''' Update q_values given reward and future state '''
        
        for s in self.states:
            if isinstance(self.game, SignalPD) and s[-1][0] == stage:
            # In Signal PD, no need to update states that do not directly 
            # precede current stage (e.g. state with last stage as signal -> 
            # signal stage)
                pass
            
            else:
                # Create entry in records
                if s not in self.records_q:
                    self.records_q[s] = defaultdict(list)
                    
                # Update record
                for a in self.actions[stage]:
#                    print('agent', self.idx)
#                    print('state', s)
#                    print('stage', stage)
#                    print('action', a)
#                    print('current_record', self.records_q[str(s)+", "+a])
#                    print('append', self.q_values[s][a], "\n")
#                    self.records_q[s + (a,)].append(self.q_values[s][a])
                    self.records_q[s][a].append(self.q_values[s][a])

        # Update q-value
        if not self.q_values[state_next]:
            # Dictionary is empty. Assign a random value
            next_state_value = random.random()*0.1
        else:
            next_state_value = max(self.q_values[state_next].values())
        
        self.q_values[state_current][act] = \
            (1-self.learn_rate) * self.q_values[state_current][act] + \
            self.learn_rate * (reward + self.disc_factor * next_state_value)    
        # print(self.q_values)

    def update_e(self):
        ''' Decay exploration and/or learning rate '''
        # Record current epsilon and learn_rate
        self.records_other['epsilon'].append(self.epsilon)
        self.records_other['learn_rate'].append(self.learn_rate)

        # Update epsilon and learn_rate
        self.epsilon *= self.epsilon_decay
        self.learn_rate *= self.learn_rate_decay

    def print_q(self):
        ''' Print q values '''
        for s in list(self.q_values):
            for a in list(self.q_values[s]):
                print ("(state "+str(s)+", actions "+a+"): "+str(self.q_values[s][a]))

    def reset(self):
        ''' Reset aganet for another round of training '''
        for s in list(self.q_values):
            for a in list(self.q_values[s]):
                self.q_values[s][a] = random.random()*0.1
        self.epsilon = self.init_epsilon
        self.learn_rate = self.init_learn_rate
        self.records_other = defaultdict(list)
        self.records_q = defaultdict(list)

### Define TFT agent ###

class TFT(Agent):
    def __init__(self, idx, game, epsilon = 1, epsilon_decay = 0.999, 
                 learn_rate = 0.3, learn_rate_decay = 1,
                 disc_factor = 0.9):
        super().__init__(idx, game, 2, True,
                 epsilon, epsilon_decay, learn_rate, learn_rate_decay,
                 disc_factor)
        
    def choose_action(self, history, stage):
        ''' Given history and stage game, use epsilon-greedy strategy to 
        choose and return an action. Q_values for the given state are 
        initialised on the fly. '''
        # Determine agent's perceived state given game history, add to states 
        state = self.history_to_state(history)
        self.states.add(state)
        
        # Play strategy tit-for-tat, i.e. play whatever opponent played last round
        if isinstance(self.game, SignalPD):
            if stage == 0:
                # In signalling phase, randomly choose signal
                act = random.choice(tuple(self.actions[stage]))
            else:
                # In action phase, follow previous action (2 rounds ago) of opponent 
                act = state[-2][1][1-self.idx] 
        
        else:
            # Repeat last round (-1) action (1) by the opponent (1-self.idx)
            act = state[-1][1][1-self.idx] 
        
        # Generate default q_values for all actions in this state
        if self.q_values[state] == {}:
            for a in self.actions[stage]:
                self.q_values[state].setdefault(a, random.random()*0.1)
     
        # Record
        self.records_other['action'].append(act)

        # Return chosen action
        return act
