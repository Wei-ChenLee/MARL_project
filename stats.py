'''
This module contains functions which calculate the summary statistics of 
experimental outcomes
'''

from collections import defaultdict

def calc_avg_rewards(records):
    ''' Calculate avg reward for agent in the testing phase '''
    # Nested dictionary with levels: trial, agent, avg. reward
    avg_rewards = {}
    num_stages = records['info']['num_stages']
    num_games = len(records['outcomes'][0]) / num_stages
    
    for trial_id in records['outcomes']: # for each one of 200 trials
        avg_rewards[trial_id] = defaultdict(int)
        for stage in records['outcomes'][trial_id]: # for each stage in trial
            rewards = records['info']['rewards'][stage[0]][stage[1]]
            for agent_id in range(records['info']['num_players']): # for each agent 
                avg_rewards[trial_id][agent_id] += rewards[agent_id]
        #print('trial', trial_id, 'a0 reward', avg_rewards[trial_id][0], 'a1 reward', avg_rewards[trial_id][1])
        for agent_id in range(records['info']['num_players']): # for each agent, calculate average
            avg_rewards[trial_id][agent_id] = avg_rewards[trial_id][agent_id] / num_games

    return avg_rewards

def aggr_avg_rewards(avg_rewards):
    
    total_avg = defaultdict(int)
    num_trials = len(avg_rewards)
    num_agents = len(avg_rewards[0])
    
    # Aggregate rewards for each agent across all trials
    for trial_id in avg_rewards:
        for agent_id in range(num_agents):
            total_avg[agent_id] += avg_rewards[trial_id][agent_id]
    
    # Calculate avg reward per trial for each agent
    for agent_id in range(num_agents):
        total_avg[agent_id] = total_avg[agent_id] / num_trials
        
    return total_avg
    
def calc_outcome_prob(records):
    ''' Calculate average outcome of action stage in the testing phase '''
    # Nested dictionary with levels: trial, outcome, count
    game_outcomes = {}
    num_stages = records['info']['num_stages']
    num_games = len(records['outcomes'][0]) / num_stages
    
    for trial_id in records['outcomes']: # for each one of 200 trials
        game_outcomes[trial_id] = {('c', 'c'):0, ('c', 'd'):0, ('d', 'c'):0, ('d', 'd'):0}
        
        # Count occurance of each stage outcome
        for stage in records['outcomes'][trial_id]: # for each stage in trial
            if stage[1] in game_outcomes[trial_id]:
                game_outcomes[trial_id][stage[1]] += 1
        
        # Calculate probability of each stage outcome
        for outcome in game_outcomes[trial_id]:
            game_outcomes[trial_id][outcome] = game_outcomes[trial_id][outcome] / num_games
        
    return game_outcomes

def aggr_outcome_prob(game_outcomes):
    
    aggr_prob = defaultdict(int)
    num_trials = len(game_outcomes)
    
    for trial_id in game_outcomes:
        for outcome in game_outcomes[trial_id]:
            aggr_prob[outcome] += game_outcomes[trial_id][outcome]
            
    for outcome in game_outcomes[0]:
        aggr_prob[outcome] = aggr_prob[outcome] / num_trials
    
    return aggr_prob
    
    
### OLD

#def calc_avg_rewards(setting):
#    ''' Calculate avg reward for agent in the testing phase '''
#    # Nested dictionary with levels: trial, agent, avg. reward
#    avg_rewards = {}
#    num_stages = len(setting.game.stages)
#    num_games = len(setting.outcomes[0]) / num_stages
#    
#    trial_id = 0
#    for trial in setting.outcomes: # for each one of 200 trials
#        avg_rewards[trial_id] = defaultdict(int)
#        for stage in trial: # for each stage in trial
#            rewards = setting.game.rewards[stage[0]][stage[1]]
#            for agent in setting.agents: # for each agent 
#                avg_rewards[trial_id][agent.idx] += rewards[agent.idx]
#        #print('trial', trial_id, 'a0 reward', avg_rewards[trial_id][0], 'a1 reward', avg_rewards[trial_id][1])
#        for agent in setting.agents: # for each agent, calculate average
#            avg_rewards[trial_id][agent.idx] = avg_rewards[trial_id][agent.idx] / num_games
#
#        trial_id += 1
#
#    return avg_rewards
#
#def aggr_avg_rewards(avg_rewards):
#    
#    total_avg = defaultdict(int)
#    num_trials = len(avg_rewards)
#    num_agents = len(avg_rewards[0])
#    
#    # Aggregate rewards for each agent across all trials
#    for trial_id in avg_rewards:
#        for agent_id in range(num_agents):
#            total_avg[agent_id] += avg_rewards[trial_id][agent_id]
#    
#    # Calculate avg reward per trial for each agent
#    for agent_id in range(num_agents):
#        total_avg[agent_id] = total_avg[agent_id] / num_trials
#        
#    return total_avg
#    
#def calc_outcome_prob(setting):
#    ''' Calculate average outcome of action stage in the testing phase '''
#    # Nested dictionary with levels: trial, outcome, count
#    game_outcomes = {}
#    num_games = len(list(setting.outcomes)[0])
#    
#    trial_id = 0
#    for trial in setting.outcomes: # for each one of 200 trials
#        game_outcomes[trial_id] = {('c', 'c'):0, ('c', 'd'):0, ('d', 'c'):0, ('d', 'd'):0}
#        
#        # Count occurance of each stage outcome
#        for stage in trial: # for each stage in trial
#            if stage[1] in game_outcomes[trial_id]:
#                game_outcomes[trial_id][stage[1]] += 1
#        
#        # Calculate probability of each stage outcome
#        for outcome in game_outcomes[trial_id]:
#            game_outcomes[trial_id][outcome] = game_outcomes[trial_id][outcome] / num_games
#        
#        trial_id += 1
#    return game_outcomes
#
#def aggr_outcome_prob(game_outcomes):
#    
#    aggr_prob = defaultdict(int)
#    num_trials = len(game_outcomes)
#    
#    for trial_id in game_outcomes:
#        for outcome in game_outcomes[trial_id]:
#            aggr_prob[outcome] += game_outcomes[trial_id][outcome]
#            
#    for outcome in game_outcomes[0]:
#        aggr_prob[outcome] = aggr_prob[outcome] / num_trials
#    
#    return aggr_prob
#    
#    
        