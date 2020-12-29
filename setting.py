'''
This module contains the Setting class.

Setting is instantiated with Game and Agents.
An instance of Setting models a Markov Game.
'''

import random
from collections import defaultdict
from agents import Agent
from games import Game, SignalPD

class Setting:
    ''' This class provides the Markov Game environment. Initialise with game
    and agents '''
    
    def __init__(self, game, agents):
        self.game = game
        self.agents = agents
        self.max_memory = max([a.memory for a in agents])
        self.initialise_history()
        #self.seed = random.randint(1, 10000)
        #random.seed = self.seed
        
    def initialise_history(self):
        ''' Initialise a random history '''
        # Randomly initialise a stage
        stage = random.choice(tuple(self.game.rewards.keys()))
        
        # Initialise a random history of maximumally required memory length
        history = []
        for t in range(self.max_memory):
            # Generate outcome for each stage game
            joint_act = []
            for a in self.agents:
                joint_act.append(random.choice(tuple(a.actions[stage])))
                
            # Append stage game outcome to history
            outcome = (stage, tuple(joint_act))
            history.append(outcome)
            
            # Transition to next stage game
            stage = self.stage_transition(stage)
            #stage = self.game.transitions[stage]
        
        # Finally, set history and define initial game stage
        self.history = history[:]
        self.stage = stage
        
    def reset(self):
        ''' Reset agents and history '''
        for a in self.agents:
            a.reset()
        self.initialise_history()
        # self.seed = random.seed

    def update_history(self, stage, joint_act):
        ''' Extend history with current stage and joint actions '''
        self.history.append((stage, joint_act))

    def stage_transition(self, stage):
        ''' Transition game to the next stage '''
        return self.game.transitions[stage]

    def return_rewards(self, stage, joint_act):
        ''' Return rewards given stage and joint actions '''
        return self.game.rewards[stage][tuple(joint_act)]

    def play_stage_game(self, stage):
        ''' Run through the stage game once. Then update agents and game '''        
        # Aggregate actions given state
        joint_act = []
        for a in self.agents:
            act = a.choose_action(self.history, stage)
            joint_act.append(act)
        joint_act = tuple(joint_act)
        
        # Determine reward and next state, given current state and actions
        r = self.return_rewards(stage, joint_act)
        stage_next = self.stage_transition(stage)
        history_current = self.history[:]
        self.update_history(stage, joint_act)
        history_next = self.history[:]

        # Players update action values
        for a in self.agents:
            a.update_q(a.history_to_state(history_current),
                       stage,
                       joint_act[a.idx],
                       r[a.idx],
                       a.history_to_state(history_next))
        
        # Players update exploration rate if next stage is the start of a new 
        # game (i.e. stage_next == 0)
        if stage_next == 0:
            for a in self.agents:
                a.update_e()

        # Update game history and stage
        self.stage = stage_next
        
    def play_no_explore_no_learning(self, iterations = 1024):
        ''' Play through the stage game a number of time without exploration 
        and without learning '''
        # Store agents' current exploration rate
        storage = defaultdict(dict)
        storage[0]['epsilon'] = self.agents[0].epsilon
        storage[0]['learn_rate'] = self.agents[0].learn_rate
        storage[1]['epsilon'] = self.agents[1].epsilon
        storage[1]['learn_rate'] = self.agents[1].learn_rate
        
        # Set agents' exploration rate to 0
        self.agents[0].epsilon = 0
        self.agents[0].learn_rate = 0
        self.agents[1].epsilon = 0
        self.agents[1].learn_rate = 0

        # Play stage game a number of times
        for t in range(iterations):
            self.play_stage_game(self.stage)
            
        # Restore explorate and learn rates
        self.agents[0].epsilon = storage[0]['epsilon']
        self.agents[0].learn_rate = storage[0]['learn_rate'] 
        self.agents[1].epsilon = storage[1]['epsilon']
        self.agents[1].learn_rate = storage[1]['learn_rate']
        
    def play(self, iterations = 10000):
        ''' Play stage game a number of times '''
        # Reset training
        self.reset()
        
        # Repeat stage game
        for i in range(iterations):
            self.play_stage_game(self.stage)
        

    def run_experiment(self, trials = 200, training_period = 10000, set_seed = False, full_record = False):
        ''' Run experiment a number of times by doing the following:
            1. Train agents by playing 10000 games            
            2. Test agents by playing a further 1024 games, without update
            3. Record testing outcome
        '''
        # Set seed
        if not set_seed:
            set_seed = random.randint(1, 1000000)
        random.seed(set_seed)
        self.seed = set_seed
        
        # Outcomes is a list of histories in the testing period
#        self.outcomes = []
#        self.seeds = []
        
        # q_values is a nest dictionary with levels: trial_id, agent, state, 
        # action
#        self.q_values = defaultdict(dict)
        
        # records is a nested dictionary with info, seeds, q_values, explore,
        # and defects        
        self.initialise_records(training_period)
        
        # For games with multiple stages, extend training periods to allows for
        # the same number of PD stage games to be played
        num_stages = len(self.game.stages)
        training_stages = training_period * num_stages
        testing_stages = 1024 * num_stages
        
        # Run experiment
        for trial_id in range(trials):
            if not trial_id%100:
                print('i = ', trial_id)
            
            # Training
            self.play(training_stages)
                        
            # Testing
            self.play_no_explore_no_learning(testing_stages)

            # Record trained q_values
#            self.record_q_values(trial_id)
            
            # Record outcome and seed
#            test_outcome = tuple(self.history[-testing_stages:])
#            self.outcomes.append(test_outcome)
            #self.seeds.append(self.seed)
            
            # Record outcomes
            self.record_outcomes(trial_id, testing_stages, full_record)
            
            # Reset seed
            self.seed = random.randint(1, 1000000)
            random.seed(self.seed)

    def initialise_records(self, num_training_games):
        self.records = {}
        self.records['info'] = {}
        self.records['info']['game'] = type(self.game)
        self.records['info']['num_stages'] = len(self.game.stages)
        self.records['info']['num_players'] = self.game.num_players
        self.records['info']['exp_id'] = self.exp_id
        self.records['info']['rewards'] = self.game.rewards
        self.records['info']['init_epsilon'] = self.agents[0].init_epsilon
        self.records['info']['epsilon_decay'] = self.agents[0].epsilon_decay
        self.records['info']['init_learn_rate'] = self.agents[0].init_learn_rate
        self.records['info']['learn_rate_decay'] = self.agents[0].learn_rate_decay
        self.records['info']['training_period'] = num_training_games
        self.records['seeds'] = []
        self.records['q_values'] = {}
        self.records['explore'] = {}
        self.records['action'] = {}
        self.records['outcomes'] = {}
        
    def record_outcomes(self, trial_id, testing_stages, full_record):
        # Initialise dictionaries
        self.records['q_values'][trial_id] = {}
        self.records['explore'][trial_id] = {}
        self.records['action'][trial_id] = {}

        #Record seed, Q-values, explorations, and actions
        self.records['seeds'].append(self.seed)
        self.records['outcomes'][trial_id] = self.history[-testing_stages:]
              
        for agent in self.agents:
            
            if full_record:
                
                # Record full records, including both training and testing periods
                self.records['q_values'][trial_id][agent.idx] = agent.records_q
                self.records['explore'][trial_id][agent.idx] = agent.records_other['explore']
                self.records['action'][trial_id][agent.idx] = agent.records_other['action']
            
            else:
                    
                # Shorten records to testing period only
                self.records['explore'][trial_id][agent.idx] = agent.records_other['explore'][-1024:]
                self.records['action'][trial_id][agent.idx] = agent.records_other['action'][-1024:]
    
                self.records['q_values'][trial_id][agent.idx] = {}
                for state in agent.records_q:
                    self.records['q_values'][trial_id][agent.idx][state] = {}
                    for action in agent.records_q[state]:
                        self.records['q_values'][trial_id][agent.idx][state][action] = agent.records_q[state][action][-1024:]

#    def record_q_values(self, trial_id):
#        ''' Record current q_values of all agents in the games to self.q_values
#        '''
#        for agent in self.agents:
#            self.q_values[trial_id][agent.idx] = agent.q_values
#            
    
#e.run_experiment(1, 10000, set_seed = 796780)