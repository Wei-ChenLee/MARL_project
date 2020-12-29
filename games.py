'''
This module contains the Game class and its subclasses.

Players are generated for a given Game.
Game is an input to instantiate the class Agents.
Game and Agents are input to instantiate the class Settings.
'''

from collections import defaultdict
     
class Player:
    def __init__(self, id):
        self.id = id
        self.actions = {}
        
    def __repr__(self):
        return 'Player actions: '+repr(self.actions)

class Game:
    def __init__(self, num_players, rewards, transitions):
        self.rewards = rewards
        self.transitions = transitions
        self.num_players = num_players
        
        # Define stages
        self.stages = [s for s in rewards.keys()]
        
        # Generate players
        self.players = {}
        for i in range(num_players):
            self.players[i] = Player(i)
            
        # Generate action space for players for each round of stage game
        for i in range(num_players):
            for s in rewards:
                self.players[i].actions[s] = set()
                for o in rewards[s]:
                    self.players[i].actions[s].add(o[i])
                    
    def __repr__(self):
        s = ''
        for i, p in self.players.items():
            s += str(i) + " " + repr(p) + '\n'
        s += 'Rewards: ' + repr(self.rewards)
        return s

### Games ###
        
class PD(Game):
    def __init__(self):
        num_players = 2
        
        rewards = defaultdict(dict)
        rewards[0][('c', 'c')] = (3, 3)
        rewards[0][('d', 'd')] = (1, 1)
        rewards[0][('c', 'd')] = (0, 5)
        rewards[0][('d', 'c')] = (5, 0)
        
        transitions = {}
        transitions[0] = 0
        
        super().__init__(num_players, rewards, transitions)

class AsymmetricPD(Game):
    def __init__(self):
        num_players = 2
        
        rewards = defaultdict(dict)
        rewards[0][('c', 'c')] = (4, 3)
        rewards[0][('d', 'd')] = (1, 2)
        rewards[0][('c', 'd')] = (0, 5)
        rewards[0][('d', 'c')] = (5, 0)        
        
        transitions = {}
        transitions[0] = 0
        
        super().__init__(num_players, rewards, transitions)

class Stackelberg(Game):
    def __init__(self):        
        num_players = 2
        
        rewards = defaultdict(dict)
        rewards[0][('c', 'c')] = (4, 3)
        rewards[0][('d', 'd')] = (2, 1)
        rewards[0][('c', 'd')] = (1, 0)
        rewards[0][('d', 'c')] = (5, 0)
        
        transitions = defaultdict(int)
        transitions[0] = 0
        
        super().__init__(num_players, rewards, transitions)

class SignalPD(Game):
    def __init__(self):        
        num_players = 2
        
        rewards = defaultdict(dict)
        for s in [('a', 'a'), ('a', 'b'), ('b', 'a'), ('b', 'b')]:
            rewards[0][s] = (0, 0)
        rewards[1][('c', 'c')] = (3, 3)
        rewards[1][('d', 'd')] = (1, 1)
        rewards[1][('c', 'd')] = (0, 5)
        rewards[1][('d', 'c')] = (5, 0)        
        
        transitions = {}
        transitions[0] = 1
        transitions[1] = 0
        
        super().__init__(num_players, rewards, transitions)

class PDxPureCoord(Game):
    def __init__(self):        
        num_players = 2
        
        rewards = defaultdict(dict)
        rewards[0][('c1', 'c1')]    = (3, 3)
        rewards[0][('c1', 'c2')]    = (0, 0)
        rewards[0][('c1', 'd')]     = (0, 5)
        rewards[0][('c2', 'c1')]    = (0, 0)
        rewards[0][('c2', 'c2')]    = (3, 3)
        rewards[0][('c2', 'd')]     = (0, 5)
        rewards[0][('d', 'c1')]     = (5, 0)
        rewards[0][('d', 'c2')]     = (5, 0)
        rewards[0][('d', 'd')]      = (1, 1)

        transitions = defaultdict(int)
        transitions[0] = 0
        
        super().__init__(num_players, rewards, transitions)

class PDxStagHunt(Game):
    def __init__(self):        
        num_players = 2
        
        rewards = defaultdict(dict)
        rewards[0][('c1', 'c1')]    = (3, 3)
        rewards[0][('c1', 'c2')]    = (0, 2)
        rewards[0][('c1', 'd')]     = (0, 5)
        rewards[0][('c2', 'c1')]    = (2, 0)
        rewards[0][('c2', 'c2')]    = (1, 1)
        rewards[0][('c2', 'd')]     = (0, 5)
        rewards[0][('d', 'c1')]     = (5, 0)
        rewards[0][('d', 'c2')]     = (5, 0)
        rewards[0][('d', 'd')]      = (1, 1)

        transitions = defaultdict(int)
        transitions[0] = 0
        
        super().__init__(num_players, rewards, transitions)


class PDxBattleOfSexes(Game):
    def __init__(self):        
        num_players = 2
        
        rewards = defaultdict(dict)
        rewards[0][('c1', 'c1')]    = (4, 2)
        rewards[0][('c1', 'c2')]    = (0, 0)
        rewards[0][('c1', 'd')]     = (0, 5)
        rewards[0][('c2', 'c1')]    = (0, 0)
        rewards[0][('c2', 'c2')]    = (2, 4)
        rewards[0][('c2', 'd')]     = (0, 5)
        rewards[0][('d', 'c1')]     = (5, 0)
        rewards[0][('d', 'c2')]     = (5, 0)
        rewards[0][('d', 'd')]      = (1, 1)

        transitions = defaultdict(int)
        transitions[0] = 0
        
        super().__init__(num_players, rewards, transitions)

