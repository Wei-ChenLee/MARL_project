'''
This module sets out the class Experiment, a subclass of Setting, which
specifies the experimental game and agents. Designed for ease of running 
preset experiments.

'''

from setting import Setting
from agents import Agent, TFT
from games import PD, SignalPD

class Experiment(Setting):
        
    def build_exp_1a(self):
        ''' Build experiment: Agent with no memory, plays against TFT '''
        game = PD()
        agent_0 = Agent(0 , game, 0, obs_opponents = False)
        agent_1 = TFT(1 , game)
        return game, agent_0, agent_1
        
    def build_exp_1b(self):
        ''' Build experiment: Agent with no memory, plays against self '''
        game = PD()
        agent_0 = Agent(0 , game, 0, obs_opponents = False)
        agent_1 = Agent(1 , game, 0, obs_opponents = False)
        return game, agent_0, agent_1
        
    def build_exp_2a(self):
        ''' Build experiment: Agent with 1 memory, no obs, plays against TFT '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = False)
        agent_1 = TFT(1 , game)
        return game, agent_0, agent_1
        
    def build_exp_2b(self):
        ''' Build experiment: Agent with 1 memory, no obs, plays against self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = False)
        agent_1 = Agent(1 , game, 1, obs_opponents = False)
        return game, agent_0, agent_1

    def build_exp_3a(self):
        ''' Build experiment: Agent with 1 memory, obs opponent, plays against 
        TFT '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True)
        agent_1 = TFT(1 , game)
        return game, agent_0, agent_1
        
    def build_exp_3b(self):
        ''' Build experiment: Agent with 1 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True)
        agent_1 = Agent(1 , game, 1, obs_opponents = True)
        return game, agent_0, agent_1
    
    def build_exp_B11b(self):
        ''' Build experiment: Agent with 1 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True, epsilon_decay = 0.9995)
        agent_1 = Agent(1 , game, 1, obs_opponents = True, epsilon_decay = 0.9995)
        return game, agent_0, agent_1

    def build_exp_B11c(self):
        ''' Build experiment: Agent with 1 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True, learn_rate = 0.7)
        agent_1 = Agent(1 , game, 1, obs_opponents = True, learn_rate = 0.7)
        return game, agent_0, agent_1

    def build_exp_B11d(self):
        ''' Build experiment: Agent with 1 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True, learn_rate = 0.7, epsilon_decay = 0.9995)
        agent_1 = Agent(1 , game, 1, obs_opponents = True, learn_rate = 0.7, epsilon_decay = 0.9995)
        return game, agent_0, agent_1

    def build_exp_4a(self):
        ''' Build experiment: Agent with 2 memory, no obs opponent, plays against 
        TFT '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = False)
        agent_1 = TFT(1 , game)
        return game, agent_0, agent_1
        
    def build_exp_4b(self):
        ''' Build experiment: Agent with 2 memory, no obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = False)
        agent_1 = Agent(1 , game, 2, obs_opponents = False)
        return game, agent_0, agent_1

    def build_exp_5a(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against 
        TFT '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = True)
        agent_1 = TFT(1 , game)
        return game, agent_0, agent_1
        
    def build_exp_5b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = True)
        agent_1 = Agent(1 , game, 2, obs_opponents = True)
        return game, agent_0, agent_1
    
    def build_exp_B12b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = True, epsilon_decay = 0.9995)
        agent_1 = Agent(1 , game, 2, obs_opponents = True, epsilon_decay = 0.9995)
        return game, agent_0, agent_1
    
    def build_exp_B12c(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = True, learn_rate = 0.7)
        agent_1 = Agent(1 , game, 2, obs_opponents = True, learn_rate = 0.7)
        return game, agent_0, agent_1

    def build_exp_B12d(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 2, obs_opponents = True, learn_rate = 0.7, epsilon_decay = 0.9995)
        agent_1 = Agent(1 , game, 2, obs_opponents = True, learn_rate = 0.7, epsilon_decay = 0.9995)
        return game, agent_0, agent_1
    
    def build_exp_6a(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = False)
        agent_1 = TFT(1, game)
        return game, agent_0, agent_1
    
    def build_exp_6b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = False)
        agent_1 = Agent(1 , game, 3, obs_opponents = False)
        return game, agent_0, agent_1

    def build_exp_7a(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True)
        agent_1 = TFT(1, game)
        return game, agent_0, agent_1
    
    def build_exp_A13b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True)
        agent_1 = TFT(1, game)
        return game, agent_0, agent_1

    def build_exp_A13c(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True, epsilon_decay = 0.9995)
        agent_1 = TFT(1, game)
        return game, agent_0, agent_1
    
    def build_exp_7b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True)
        agent_1 = Agent(1 , game, 3, obs_opponents = True)
        return game, agent_0, agent_1
    
    def build_exp_B13b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True, epsilon_decay = 0.9995)
        agent_1 = Agent(1 , game, 3, obs_opponents = True, epsilon_decay = 0.9995)
        return game, agent_0, agent_1

    def build_exp_B13c(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True, learn_rate = 0.7)
        agent_1 = Agent(1 , game, 3, obs_opponents = True, learn_rate = 0.7)
        return game, agent_0, agent_1
    
    def build_exp_B13d(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 3, obs_opponents = True, learn_rate = 0.7, epsilon_decay = 0.9995)
        agent_1 = Agent(1 , game, 3, obs_opponents = True, learn_rate = 0.7, epsilon_decay = 0.9995)
        return game, agent_0, agent_1

    def build_exp_8a(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 4, obs_opponents = False)
        agent_1 = TFT(1, game)
        return game, agent_0, agent_1
    
    def build_exp_8b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 4, obs_opponents = False)
        agent_1 = Agent(1 , game, 4, obs_opponents = False)
        return game, agent_0, agent_1

    def build_exp_9a(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 4, obs_opponents = True)
        agent_1 = TFT(1, game)
        return game, agent_0, agent_1
    
    def build_exp_9b(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 4, obs_opponents = True)
        agent_1 = Agent(1 , game, 4, obs_opponents = True)
        return game, agent_0, agent_1
    
    def build_exp_C1101(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True)
        agent_1 = Agent(1 , game, 1, obs_opponents = False)
        return game, agent_0, agent_1
    
    def build_exp_C1102(self):
        ''' Build experiment: Agent with 2 memory, obs opponent, plays against
        self '''
        game = PD()
        agent_0 = Agent(0 , game, 1, obs_opponents = True)
        agent_1 = Agent(1 , game, 2, obs_opponents = False)
        return game, agent_0, agent_1

#    def build_exp_6a(self):
#        ''' Build experiment: Agent with 1 memory, obs opponent, plays against 
#        TFT '''
#        game = SignalPD()
#        agent_0 = Agent(0 , game, 1, obs_opponents = True)
#        agent_1 = TFT(1 , game)
#        return game, agent_0, agent_1
#        
#    def build_exp_6b(self):
#        ''' Build experiment: Agent with 1 memory, obs opponent, plays against
#        self '''
#        game = SignalPD()
#        agent_0 = Agent(0 , game, 1, obs_opponents = True, 
#                        epsilon_decay = 0.999**0.5)
#        agent_1 = Agent(1 , game, 1, obs_opponents = True,
#                        epsilon_decay = 0.999**0.5)
#        return game, agent_0, agent_1
#
#    def build_exp_7a(self):
#        ''' Build experiment: Agent with 3 memory, obs opponent, plays against 
#        TFT '''
#        game = SignalPD()
#        agent_0 = Agent(0 , game, 3, obs_opponents = True)
#        agent_1 = TFT(1 , game)
#        return game, agent_0, agent_1
#        
#    def build_exp_7b(self):
#        ''' Build experiment: Agent with 3 memory, obs opponent, plays against
#        self '''
#        game = SignalPD()
#        agent_0 = Agent(0 , game, 3, obs_opponents = True, 
#                        epsilon_decay = 0.999**0.5)
#        agent_1 = Agent(1 , game, 3, obs_opponents = True,
#                        epsilon_decay = 0.999**0.5)
#        return game, agent_0, agent_1


        
    def __init__(self, exp_id):
        switcher = {
            '1a': self.build_exp_1a,
            '1b': self.build_exp_1b,
            '2a': self.build_exp_2a,
            '2b': self.build_exp_2b,
            '3a': self.build_exp_3a,
            '3b': self.build_exp_3b,
            '4a': self.build_exp_4a,
            '4b': self.build_exp_4b,
            '5a': self.build_exp_5a,
            '5b': self.build_exp_5b,
            '6a': self.build_exp_6a,
            '6b': self.build_exp_6b,
            '7a': self.build_exp_7a,
            '7b': self.build_exp_7b,
            '8a': self.build_exp_8a,
            '8b': self.build_exp_8b,
            '9a': self.build_exp_9a,
            '9b': self.build_exp_9b,
            'A00': self.build_exp_1a,
            'A01': self.build_exp_2a,
            'A02': self.build_exp_4a,
            'A03': self.build_exp_6a,
            'A04': self.build_exp_8a,
            'A11': self.build_exp_3a,
            'A12': self.build_exp_5a,
            'A13': self.build_exp_7a,
            'A13b': self.build_exp_A13b,
            'A13c': self.build_exp_A13c,
            'A14': self.build_exp_9a,
            'B00': self.build_exp_1b,
            'B01': self.build_exp_2b,
            'B02': self.build_exp_4b,
            'B03': self.build_exp_6b,
            'B04': self.build_exp_8b,
            'B11': self.build_exp_3b,
            'B11b': self.build_exp_B11b,
            'B11c': self.build_exp_B11c,
            'B11d': self.build_exp_B11d,
            'B12': self.build_exp_5b,
            'B12b': self.build_exp_B12b,
            'B12c': self.build_exp_B12c,            
            'B12d': self.build_exp_B12d,
            'B13': self.build_exp_7b,
            'B13b': self.build_exp_B13b,
            'B13c': self.build_exp_B13c,
            'B13d': self.build_exp_B13d,
            'B14': self.build_exp_9b,
            'C1101': self.build_exp_C1101,
            'C1102': self.build_exp_C1102

        }
        
        build_experiment = switcher.get(exp_id)
                                        #print('WL: Not a valid model code'))
        
        game, agent_0, agent_1 = build_experiment()
        super().__init__(game, [agent_0, agent_1])
        self.exp_id = exp_id