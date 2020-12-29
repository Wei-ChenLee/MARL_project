'''
This module provides the functions for plotting outcomes of experiments
'''

import matplotlib.pyplot as plt
from collections import defaultdict
from games import SignalPD
from experiments import Experiment
from setting import Setting
from matplotlib.ticker import MaxNLocator

def plot_q(records, trial = 0, start = 0, duration = -1024, annotate = 100, save_fig = False):
    '''Takes a record or a experiment and the specified trial number, plot
    Q-values, exploration rate, and action'''
    
    plt.style.use('seaborn-darkgrid')
    colour = {'c':'green', 'd':'red', 'a':'y', 'b':'blue'}

    # Set parameters
    num_states = len(records['q_values'][trial][0])
    
    # Only plot Q-values of training agent, not TFT agent
    if records['info']['exp_id'][-1] == 'a':
        num_players = 1
    else:
        num_players = len(records['q_values'][0])

    # Setup figure
    fig, axs = plt.subplots(num_states + 2, num_players, 
                            figsize=(12, 1.6*(num_states+2)))
    fig.subplots_adjust(hspace = 0.6, wspace= 0.15)
    axs = axs.ravel()
    
    # Plot Q-values
    i = 0
    for state in records['q_values'][trial][0]:
        for action in records['q_values'][trial][0][state]:
            for agent_idx in range(num_players):
                # Plot Q-values for state and action
                ax_idx = i + agent_idx
    
                state_text = ("".join(state[0][1])).upper()
                axs[ax_idx].set_title('Player '+str(agent_idx) + ', State ' + str(state_text))
                #axs[ax_idx].set_title('Player '+str(agent_idx) + ', single state')
                axs[ax_idx].set_ylabel('Q-value')
                axs[ax_idx].plot(
                    range(len(records['action'][trial][agent_idx]))[start:start+duration],
                    records['q_values'][trial][agent_idx][state][action][start:start+duration], 
                    label = action,
                    color = colour[action])
                axs[ax_idx].set_xticks([i for i in range(9991, 10000, 2)])
                #axs[ax_idx].set_xticks([i for i in range(0, 10001, 2000)])
                                
        # Increase axes index
        i += num_players

    # Plot exploration and action
    for agent_idx in range(num_players):
        # Plot actions
        ax_idx = -2*num_players + agent_idx
        
        #axs[ax_idx].set_ylabel('action')
        axs[ax_idx].scatter(
            range(len(records['action'][trial][agent_idx]))[start:start+duration],
            [x == 'd' for x in records['action'][trial][agent_idx][start:start+duration]], 
            marker = 'x')
        axs[ax_idx].set_yticks([0,1])
        labels = [item.get_text() for item in axs[ax_idx].get_yticklabels()]
        labels[0] = 'Cooperate'
        labels[1] = 'Defect'
        axs[ax_idx].set_yticklabels(labels)
        axs[ax_idx].set_xticks([i for i in range(9991, 10001, 2)])
        #axs[ax_idx].set_xticks([i for i in range(0, 10001, 2000)])

        
        # Annotate actions if requested
        if annotate:
            last = 0
            loc = 0.1
            for idx, val in enumerate([x == 'd' for x in records['action'][trial][agent_idx]]):
                if idx > 12000 and val == True and idx - last >= annotate:
                    axs[ax_idx].annotate(idx, (idx, 0.95+loc))
                    last = idx
                    loc = -loc
        
        # Plot exploration
        ax_idx = -num_players + agent_idx
        
        #axs[ax_idx].set_ylabel('explore')
        axs[ax_idx].scatter(
                range(len(records['explore'][trial][agent_idx]))[start:start+duration], 
                records['explore'][trial][agent_idx][start:start+duration],
                marker = 'x')
        axs[ax_idx].set_yticks([0,1])
        labels = [item.get_text() for item in axs[ax_idx].get_yticklabels()]
        labels[0] = 'Exploit'
        labels[1] = 'Explore'
        axs[ax_idx].set_yticklabels(labels)
        axs[ax_idx].set_xticks([i for i in range(9991, 10001, 2)])
        #axs[ax_idx].set_xticks([i for i in range(0, 10001, 2000)])
        
        # Annotate exploration if requested
        if annotate:
            last = 0
            loc = 0.1
            for idx, val in enumerate(records['explore'][trial][agent_idx]):
                if idx > 12000 and val == True and idx - last >= annotate:
                    axs[ax_idx].annotate(idx, (idx, 0.95+loc))
                    last = idx
                    loc = -loc

    handles, labels = axs[0].get_legend_handles_labels()
    labels = [a.upper() for a in labels]
    fig.legend(handles, labels, loc ='lower center', ncol = 2)
    # fig.suptitle('Experiment '+records['info']['exp_id'] +', trial '+str(trial))
    
    if save_fig:
        print("saving figure")
        path = 'img/'
        name = records['info']['exp_id']+' t'+str(trial)+ ' '+str(start)+'-'+str(start+duration)+ ' q_val.png'
        plt.savefig(path + name)
        
    fig.show()

def plot_action(records, assessment_period = 256, start = -20, 
                end = None, cutoff = 10, save_fig = True):
    ''' Plot actions of agents in the final few games of the assessment period
    '''
    plt.style.use('seaborn-darkgrid')
    
    if records['info']['num_stages'] > 1:
        # if game is multi-stage (i.e. Signal PD), take only action phase
        outcomes = {}
        for trial_id in records['outcomes']:
            actions = []
            for stage in records['outcomes'][trial_id]:
                if stage[0] == 1: # Action phase in Signal game
                    actions.append(stage)
            outcomes[trial_id] = actions
    else:
        outcomes = records['outcomes']
    
    # Combine sequences of actions that are similar together
    data = defaultdict(int)
    for trial_id in outcomes:
        found = False
        for offset in range(1, assessment_period + 1):
            offset_trial = tuple(outcomes[trial_id][-assessment_period-offset : -offset])
            if offset_trial in data:
                data[offset_trial] += 1
                found = True
                
                break
        if not found:
            data[tuple(outcomes[trial_id][-assessment_period:])] += 1
            
#    # Combine sequences of actions that are similar together
#    data = defaultdict(int)
#    for o in outcomes:
#        found = False
#        for offset in range(1, assessment_period + 1):
#            offset_o = o[-assessment_period-offset : -offset]
#            if offset_o in data:
#                data[offset_o] += 1
#                found = True
#                break
#        if not found:
#            data[o[-assessment_period:]] += 1
#    
    
    # Plot data
    num_outcomes = len(data.keys())
    
    if num_outcomes == 1:
        # Plot singular outcome
        fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 1.6*num_outcomes))
        fig.subplots_adjust(hspace = 0.5)

        for outcome in data.keys():
            player0 = []
            player1 = []
            for h in outcome:
                if h[1][0] == 'd':
                    player0.append(3)
                else:
                    player0.append(2.04)
                if h[1][1] == 'd':
                    player1.append(1)
                else:
                    player1.append(1.96)
                    
            x_axis = range(1, len(player0)+1)
            axs.plot(x_axis[start:end], player0[start:end], label="p0")
            axs.plot(x_axis[start:end], player1[start:end], label="p1")
            axs.set_title(str(data[outcome]/10)+'%', loc='right')
            axs.set_yticks([1,2,3])
            axs.set_xticks(x_axis[start:end])
            axs.set_yticklabels(['A1 defects', 'Cooperate', 'A0 defects'])
            axs.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=True,       # ticks along the bottom edge are on
                top=True,          # ticks along the top edge are on
                labelbottom=False) # labels along the bottom edge are off
        
    elif num_outcomes > cutoff:
        # Plot most likely outcomes (determined by 'cutoff')
        indices = sorted(data, 
                         key=data.get, 
                         reverse=True)[:cutoff]
        fig, axs = plt.subplots(cutoff, 1, figsize=(12, 1.6*cutoff))
        fig.subplots_adjust(hspace = 0.4)
        
        i = 0
        for outcome in indices:
            player0 = []
            player1 = []
            for h in outcome:
                if h[1][0] == 'd':
                    player0.append(3)
                else:
                    player0.append(2.04)
                if h[1][1] == 'd':
                    player1.append(1)
                else:
                    player1.append(1.96)
            x_axis = range(1, len(player0)+1)
    
            axs[i].plot(x_axis[start:end], player0[start:end], label="p0")
            axs[i].plot(x_axis[start:end], player1[start:end], label="p1")
            axs[i].set_title(str(data[outcome]/10)+'%', loc='right')
            axs[i].set_yticks([1,2,3])
            axs[i].set_xticks(x_axis[start:end])
            axs[i].set_yticklabels(['A1 defects', 'Cooperate', 'A0 defects'])            
            axs[i].tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=True,       # ticks along the bottom edge are on
                top=True,          # ticks along the top edge are on
                labelbottom=False) # labels along the bottom edge are off
            i += 1            
    else:
        # Plot all outcomes
        indices = sorted(data, key=data.get, reverse=True)
        fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 1.6*num_outcomes))
        fig.subplots_adjust(hspace = 0.4)

        i = 0
        for outcome in indices:
            player0 = []
            player1 = []
            for h in outcome:
                if h[1][0] == 'd':
                    player0.append(3)
                else:
                    player0.append(2.04)
                if h[1][1] == 'd':
                    player1.append(1)
                else:
                    player1.append(1.96)
            x_axis = range(1, len(player0)+1)
    
            axs[i].plot(x_axis[start:end], player0[start:end], label="p0")
            axs[i].plot(x_axis[start:end], player1[start:end], label="p0")
            axs[i].set_title(str(data[outcome]/10)+'%', loc='right')
            axs[i].set_yticks([1,2,3])
            axs[i].set_xticks(x_axis[start:end])
            axs[i].set_yticklabels(['A1 defects', 'Cooperate', 'A0 defects'])
            axs[i].tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=True,       # ticks along the bottom edge are on
                top=True,          # ticks along the top edge are on
                labelbottom=False) # labels along the bottom edge are off
            i += 1

    #fig.suptitle('Experiment '+records['info']['exp_id'])

    # Save figure
    if save_fig:
        path = 'img/'
        name = records['info']['exp_id']+' lrn'+str(records['info']['init_learn_rate'])+' trn'+str(records['info']['training_period'])+'.png'
        plt.savefig(path + name)

    # Show figure
    plt.show()    

def plot_action_trial(records, trial_id = 0, assessment_period = 256, 
                      start = -20, end = None, cutoff = 10, save_fig = True):
    ''' Plot actions of agents in the final few games of the assessment period
    '''
    plt.style.use('seaborn-darkgrid')
    
    if records['info']['num_stages'] > 1:
        # if game is multi-stage (i.e. Signal PD), take only action phase
        outcomes = {}
        for trial_id in records['outcomes']:
            actions = []
            for stage in records['outcomes'][trial_id]:
                if stage[0] == 1: # Action phase in Signal game
                    actions.append(stage)
            outcomes[trial_id] = actions
    else:
        outcomes = records['outcomes']
    
    # Translate to data format for plotting
    data = defaultdict(int)
    data[tuple(outcomes[trial_id][-assessment_period:])] += 1
                
    # Plot data
    num_outcomes = len(data.keys())
    
    fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 2*num_outcomes))
    fig.subplots_adjust(hspace = 0.5)

    for outcome in data.keys():
        player0 = []
        player1 = []
        for h in outcome:
            if h[1][0] == 'd':
                player0.append(3)
            else:
                player0.append(2)
            if h[1][1] == 'd':
                player1.append(1)
            else:
                player1.append(2)
                
        x_axis = range(1, len(player0)+1)
        axs.plot(x_axis[start:end], player0[start:end], label="p0")
        axs.plot(x_axis[start:end], player1[start:end], label="p1")
        #axs.set_title(str(data[outcome]/2)+'%', loc='right')
        axs.set_yticks([1,2,3])
        axs.set_xticks(x_axis[start:end])
        axs.set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
        axs.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=True,       # ticks along the bottom edge are on
            top=True,          # ticks along the top edge are on
            labelbottom=False) # labels along the bottom edge are off
        
    fig.suptitle('Experiment '+records['info']['exp_id'] +', trial '+str(trial_id))

    # Save figure
    if save_fig:
        path = 'img/'
        name = records['info']['exp_id']+' t'+str(trial_id)+' lrn'+str(records['info']['init_learn_rate'])+' trn'+str(records['info']['training_period'])+'.png'
        plt.savefig(path + name)

    # Show figure
    plt.show()


#def plot_q(setting):
#    plt.style.use('seaborn-darkgrid')
#    colour = {'c':'green', 'd':'red'}
#
#    num_states = len(setting.agents[0].states)
#    num_players = len(setting.agents)
#
#    fig, axs = plt.subplots(num_states, num_players, 
#                            figsize=(6*num_players, 3.5*num_states))
#    fig.subplots_adjust(hspace = 0.4, wspace= 0.15)
#    axs = axs.ravel()
#
#    i = 0
#    for state in setting.agents[0].states:
#        for action in setting.agents[0].q_values[state]:
#            for agent in setting.agents:
#                #state_action = str(state)+", "+action
#                state_action = state + (action,)
#                axs[i+agent.idx].set_title('Player '+str(agent.idx) + ", State " + str(state))
#                #axs[i+p.idx].set_xlabel('iterations')
#                axs[i+agent.idx].set_ylabel('q value')
#                axs[i+agent.idx].plot(agent.records_q[state_action], label = action, color = colour[action])    
#        i += num_players
#
#    handles, labels = axs[0].get_legend_handles_labels()
#    fig.legend(handles, labels, loc ='lower center', ncol = 2)
#    fig.show()

#def plot_qplus(setting, start = 0, duration = -1024):
#    plt.style.use('seaborn-darkgrid')
#    colour = {'c':'green', 'd':'red'}
#
#    num_states = len(setting.agents[0].states)
#    num_players = len(setting.agents)
#
#    fig, axs = plt.subplots(num_states * 3, num_players, 
#                            figsize=(6*num_players, 3.5*num_states))
#    fig.subplots_adjust(hspace = 0.4, wspace= 0.15)
#    axs = axs.ravel()
#    
##    # Generate action values for plotting
##    action_val = defaultdict(list)
##    for a in setting.agents:
##        action_val[a.idx] = [x == 'd' for x in setting.agents[a.idx].records_other['action']]
##    
##    print(action_val)
#
#    i = 0
#    for state in setting.agents[0].states:
#        for action in setting.agents[0].q_values[state]:
#            for agent in setting.agents:
#                # Plot q_values
#                state_action = state + (action,)
#                axs[i+agent.idx].set_title('Player '+str(agent.idx) + ", State " + str(state))
#                #axs[i+p.idx].set_xlabel('iterations')
#                axs[i+agent.idx].set_ylabel('q value')
#                axs[i+agent.idx].plot(
#                        range(len(agent.records_q[state_action]))[start:start+duration],
#                        agent.records_q[state_action][start:start+duration], 
#                        label = action, 
#                        color = colour[action])    
#                
#                # Plot actions
#                axs[i+2+agent.idx].set_ylabel('defect')
#                axs[i+2+agent.idx].scatter(
#                        range(len(agent.records_other['action']))[start:start+duration],
#                        [x == 'd' for x in agent.records_other['action'][start:start+duration]], 
#                        marker = 'x')
#                axs[i+2+agent.idx].set_yticks([0,1])
#                
#                # Annotate actions
#                last = 0
#                loc = 0.1
#                for idx, val in enumerate([x == 'd' for x in agent.records_other['action']]):
#                    if idx > 6000 and val == True and idx - last >= 100:
#                        axs[i+2+agent.idx].annotate(idx, (idx, 0.95+loc))
#                        last = idx
#                        loc = -loc
#                
#                # Plot exploration
#                axs[i+4+agent.idx].set_ylabel('explore')
#                axs[i+4+agent.idx].scatter(
#                        range(len(agent.records_other['explore']))[start:start+duration], 
#                        agent.records_other['explore'][start:start+duration],
#                        marker = 'x')
#                axs[i+4+agent.idx].set_yticks([0,1])
#                
#                # Annotate exploration
#                last = 0
#                loc = 0.1
#                for idx, val in enumerate(agent.records_other['explore']):
#                    if idx > 6000 and val == True and idx - last >= 100:
#                        axs[i+4+agent.idx].annotate(idx, (idx, 0.95+loc))
#                        last = idx
#                        loc = -loc
#
#        i += num_players * 3
#
#    handles, labels = axs[0].get_legend_handles_labels()
#    fig.legend(handles, labels, loc ='lower center', ncol = 2)
#    fig.show()



#def plot_history(setting, start = -20, end = None):
#    plt.style.use('seaborn-darkgrid')
#
#    player0 = []
#    player1 = []
#    for h in setting.history:
#        if h[1][0] == 'd':
#            player0.append(3)
#        else:
#            player0.append(2)
#        if h[1][1] == 'd':
#            player1.append(1)
#        else:
#            player1.append(2)
#
#    x_axis = range(1, len(player0)+1)
#    
#    fig, ax = plt.subplots(figsize=(12, 2))
#    ax.plot(x_axis[start:end], player0[start:end], label="p0")
#    ax.plot(x_axis[start:end], player1[start:end], label="p1")
#    # ax.legend()
#    ax.set_yticks([1,2,3])
#    ax.set_xticks(x_axis[start:end])
#    ax.set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#    
#    plt.show()
    #handles, labels = axs[0].get_legend_handles_labels()
    #fig.legend(handles, labels, loc ='lower center', ncol = 2)

#def plot_outcomes(setting, cutoff = 12, start = -20, end = None):
#    
#    # Handle SignalPD in a separate function
#    if isinstance(setting.game, games.SignalPD):
#        return plot_outcomes_SignalPD(setting, cutoff = 12, start = -20, end = None)
#        
#    plt.style.use('seaborn-darkgrid')
#    num_outcomes = len(setting.outcomes)
#    
#    if num_outcomes == 1:
#        # Plot singular outcome
#        fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 2*num_outcomes))
#        fig.subplots_adjust(hspace = 0.4)
#
#        for outcome in setting.outcomes.keys():
#            player0 = []
#            player1 = []
#            for h in outcome:
#                if h[1][0] == 'd':
#                    player0.append(3)
#                else:
#                    player0.append(2)
#                if h[1][1] == 'd':
#                    player1.append(1)
#                else:
#                    player1.append(2)
#            x_axis = range(1, len(player0)+1)
#    
#            axs.plot(x_axis[start:end], player0[start:end], label="p0")
#            axs.plot(x_axis[start:end], player1[start:end], label="p0")
#            axs.set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs.set_yticks([1,2,3])
#            axs.set_xticks(x_axis[start:end])
#            axs.set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#            axs.tick_params(
#                axis='x',          # changes apply to the x-axis
#                which='both',      # both major and minor ticks are affected
#                bottom=True,       # ticks along the bottom edge are on
#                top=True,          # ticks along the top edge are on
#                labelbottom=False) # labels along the bottom edge are off
#        
#    elif num_outcomes > cutoff:
#        # Plot top 15 most likely outcomes
#        indices = sorted(setting.outcomes, 
#                         key=setting.outcomes.get, 
#                         reverse=True)[:cutoff]
#        fig, axs = plt.subplots(cutoff, 1, figsize=(12, 2*cutoff))
#        fig.subplots_adjust(hspace = 0.4)
#        
#        i = 0
#        for outcome in indices:
#            player0 = []
#            player1 = []
#            for h in outcome:
#                if h[1][0] == 'd':
#                    player0.append(3)
#                else:
#                    player0.append(2)
#                if h[1][1] == 'd':
#                    player1.append(1)
#                else:
#                    player1.append(2)
#            x_axis = range(1, len(player0)+1)
#    
#            axs[i].plot(x_axis[start:end], player0[start:end], label="p0")
#            axs[i].plot(x_axis[start:end], player1[start:end], label="p0")
#            axs[i].set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs[i].set_yticks([1,2,3])
#            axs[i].set_xticks(x_axis[start:end])
#            axs[i].set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])            
#            axs[i].tick_params(
#                axis='x',          # changes apply to the x-axis
#                which='both',      # both major and minor ticks are affected
#                bottom=True,       # ticks along the bottom edge are on
#                top=True,          # ticks along the top edge are on
#                labelbottom=False) # labels along the bottom edge are off
#            i += 1            
#    else:
#        # Plot all outcomes
#        fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 2*num_outcomes))
#        fig.subplots_adjust(hspace = 0.4)
#
#        i = 0
#        for outcome in setting.outcomes.keys():
#            player0 = []
#            player1 = []
#            for h in outcome:
#                if h[1][0] == 'd':
#                    player0.append(3)
#                else:
#                    player0.append(2)
#                if h[1][1] == 'd':
#                    player1.append(1)
#                else:
#                    player1.append(2)
#            x_axis = range(1, len(player0)+1)
#    
#            axs[i].plot(x_axis[start:end], player0[start:end], label="p0")
#            axs[i].plot(x_axis[start:end], player1[start:end], label="p0")
#            axs[i].set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs[i].set_yticks([1,2,3])
#            axs[i].set_xticks(x_axis[start:end])
#            axs[i].set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#            axs[i].tick_params(
#                axis='x',          # changes apply to the x-axis
#                which='both',      # both major and minor ticks are affected
#                bottom=True,       # ticks along the bottom edge are on
#                top=True,          # ticks along the top edge are on
#                labelbottom=False) # labels along the bottom edge are off
#            i += 1
#
#    fig.suptitle('Experiment '+setting.exp_id)
#    plt.show()
#    
#    
#def plot_outcomes_SignalPD(setting, cutoff = 12, start = -20, end = None):
#        
#    plt.style.use('seaborn-darkgrid')
#    num_outcomes = len(setting.outcomes)
#    
#    if num_outcomes*2 <= cutoff:
#        # Plot singular outcome
#        fig, axs = plt.subplots(num_outcomes*2, 1, figsize=(12, 4*num_outcomes))
#        fig.subplots_adjust(hspace = 0.4)
#
#        i = 0
#        for outcome in setting.outcomes.keys():
#            
#            # If outcome ends in signal phase, trim start and end
#            if outcome[-1][0] == 0: 
#                outcome = outcome[1:-1]
#            
#            # Prepare signals and actions to be plotted
#            player0 = []
#            player1 = []
#            signal0 = []
#            signal1 = []
#
#            for h in outcome:
#                if h[0] == 0: # Signal phase
#                    if h[1][0] == 'a':
#                        signal0.append(3)
#                    else:
#                        signal0.append(2)
#                    if h[1][1] == 'a':
#                        signal1.append(1)
#                    else:
#                        signal1.append(0)
#                        
#                else: # Action phase
#                    if h[1][0] == 'd':
#                        player0.append(3)
#                    else:
#                        player0.append(2)
#                    if h[1][1] == 'd':
#                        player1.append(1)
#                    else:
#                        player1.append(2)
#            
#            x_axis = range(1, len(player0)+1)
#            
#            axs[i].plot(x_axis[start:end], signal0[start:end], label="p0")
#            axs[i].plot(x_axis[start:end], signal1[start:end], label="p0")
#            #axs[i].set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs[i].set_yticks([0,1,2,3])
#            axs[i].set_xticks(x_axis[start:end])
#            axs[i].set_yticklabels(['Agent 1 signals "b"', 'Agent 1 signals "a"', 'Agent 0 signals "b"', 'Agent 0 signals "a"'])
#            axs[i].tick_params(
#                    axis='x',          # changes apply to the x-axis
#                    which='both',      # both major and minor ticks are affected
#                    bottom=True,       # ticks along the bottom edge are on
#                    top=True,          # ticks along the top edge are on
#                    labelbottom=False) # labels along the bottom edge are off
#            
#            axs[i+1].plot(x_axis[start:end], player0[start:end], label="p0")
#            axs[i+1].plot(x_axis[start:end], player1[start:end], label="p0")
#            axs[i+1].set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs[i+1].set_yticks([1,2,3])
#            axs[i+1].set_xticks(x_axis[start:end])
#            axs[i+1].set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#            axs[i+1].tick_params(
#                    axis='x',          # changes apply to the x-axis
#                    which='both',      # both major and minor ticks are affected
#                    bottom=True,       # ticks along the bottom edge are on
#                    top=True,          # ticks along the top edge are on
#                    labelbottom=False) # labels along the bottom edge are off
#            i+=2
#        
#    else:
#        # Plot top most likely outcomes
#        indices = sorted(setting.outcomes, 
#                         key=setting.outcomes.get, 
#                         reverse=True)[:int(cutoff/2)]
#        fig, axs = plt.subplots(cutoff, 1, figsize=(12, 2*cutoff))
#        fig.subplots_adjust(hspace = 0.4)
#        
#        i = 0
#        for outcome in indices:
#            
#            # If outcome ends in signal phase, trim start and end
#            if outcome[-1][0] == 0: 
#                outcome = outcome[1:-1]
#            
#            # Prepare signals and actions to be plotted
#            player0 = []
#            player1 = []
#            signal0 = []
#            signal1 = []
#
#            for h in outcome:
#                if h[0] == 0: # Signal phase
#                    if h[1][0] == 'a':
#                        signal0.append(3)
#                    else:
#                        signal0.append(2)
#                    if h[1][1] == 'a':
#                        signal1.append(1)
#                    else:
#                        signal1.append(0)
#                        
#                else: # Action phase
#                    if h[1][0] == 'd':
#                        player0.append(3)
#                    else:
#                        player0.append(2)
#                    if h[1][1] == 'd':
#                        player1.append(1)
#                    else:
#                        player1.append(2)
#            
#            x_axis = range(1, len(player0)+1)
#            
#            axs[i].plot(x_axis[start:end], signal0[start:end], label="p0")
#            axs[i].plot(x_axis[start:end], signal1[start:end], label="p0")
#            #axs[i].set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs[i].set_yticks([0,1,2,3])
#            axs[i].set_xticks(x_axis[start:end])
#            axs[i].set_yticklabels(['Agent 1 signals "b"', 'Agent 1 signals "a"', 'Agent 0 signals "b"', 'Agent 0 signals "a"'])
#            axs[i].tick_params(
#                    axis='x',          # changes apply to the x-axis
#                    which='both',      # both major and minor ticks are affected
#                    bottom=True,       # ticks along the bottom edge are on
#                    top=True,          # ticks along the top edge are on
#                    labelbottom=False) # labels along the bottom edge are off
#            
#            axs[i+1].plot(x_axis[start:end], player0[start:end], label="p0")
#            axs[i+1].plot(x_axis[start:end], player1[start:end], label="p0")
#            axs[i+1].set_title(str(setting.outcomes[outcome]/2)+'%', loc='right')
#            axs[i+1].set_yticks([1,2,3])
#            axs[i+1].set_xticks(x_axis[start:end])
#            axs[i+1].set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#            axs[i+1].tick_params(
#                    axis='x',          # changes apply to the x-axis
#                    which='both',      # both major and minor ticks are affected
#                    bottom=True,       # ticks along the bottom edge are on
#                    top=True,          # ticks along the top edge are on
#                    labelbottom=False) # labels along the bottom edge are off
#            i+=2
            
#def strip_signals(setting):
#    ''' Remove signal phases from outcomes and return list of outcome with only
#    action phases '''
#    # Scrape action outcomes
#    if len(setting.game.stages) > 1:
#        # if game is multi-stage (i.e. Signal PD), take only action phase
#        outcomes = []
#        for o in setting.outcomes:
#            actions = []
#            for stage in o:
#                if stage[0] == 1: # Action phase in Signal game
#                    actions.append(stage)
#            outcomes.append(tuple(actions))
#    else:
#        outcomes = setting.outcomes
#    return outcomes
#    
#def combine_similar_outcomes(outcomes, assessment_period = 256):
#    # Generate dictionary of similar action outcomes
#    data = defaultdict(int)
#    
#    for o in outcomes:
#        found = False
#        for offset in range(1, assessment_period + 1):
#            offset_o = o[-assessment_period-offset : -offset]
#            if offset_o in data:
#                data[offset_o] += 1
#                found = True
#                break
#        
#        if not found:
#            data[o[-assessment_period:]] += 1
#        
#    # Return processed action data
#    return data
            

#def plot_actions(setting, assessment_period = 256, 
#                 start = -20, end = None, cutoff = 10):
#    ''' Plot actions of agents in the final few games oaf the assessment period
#    '''
#    plt.style.use('seaborn-darkgrid')
#
#    # Pre-process data to get actions only (no signals)
#    if len(setting.game.stages) > 1:
#        # if game is multi-stage (i.e. Signal PD), take only action phase
#        outcomes = []
#        for o in setting.outcomes:
#            actions = []
#            for stage in o:
#                if stage[0] == 1: # Action phase in Signal game
#                    actions.append(stage)
#            outcomes.append(tuple(actions))
#    else:
#        outcomes = setting.outcomes
#        
#    # Combine sequences of actions that are similar together
#    data = defaultdict(int)
#    for o in outcomes:
#        found = False
#        for offset in range(1, assessment_period + 1):
#            offset_o = o[-assessment_period-offset : -offset]
#            if offset_o in data:
#                data[offset_o] += 1
#                found = True
#                break
#        if not found:
#            data[o[-assessment_period:]] += 1
#    
#    # Plot data
#    num_outcomes = len(data.keys())
#    
#    if num_outcomes == 1:
#        # Plot singular outcome
#        fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 2*num_outcomes))
#        fig.subplots_adjust(hspace = 0.5)
#
#        for outcome in data.keys():
#            player0 = []
#            player1 = []
#            for h in outcome:
#                if h[1][0] == 'd':
#                    player0.append(3)
#                else:
#                    player0.append(2)
#                if h[1][1] == 'd':
#                    player1.append(1)
#                else:
#                    player1.append(2)
#                    
#            x_axis = range(1, len(player0)+1)
#            axs.plot(x_axis[start:end], player0[start:end], label="p0")
#            axs.plot(x_axis[start:end], player1[start:end], label="p1")
#            axs.set_title(str(data[outcome]/2)+'%', loc='right')
#            axs.set_yticks([1,2,3])
#            axs.set_xticks(x_axis[start:end])
#            axs.set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#            axs.tick_params(
#                axis='x',          # changes apply to the x-axis
#                which='both',      # both major and minor ticks are affected
#                bottom=True,       # ticks along the bottom edge are on
#                top=True,          # ticks along the top edge are on
#                labelbottom=False) # labels along the bottom edge are off
#        
#    elif num_outcomes > cutoff:
#        # Plot most likely outcomes (determined by 'cutoff')
#        indices = sorted(data, 
#                         key=data.get, 
#                         reverse=True)[:cutoff]
#        fig, axs = plt.subplots(cutoff, 1, figsize=(12, 2*cutoff))
#        fig.subplots_adjust(hspace = 0.4)
#        
#        i = 0
#        for outcome in indices:
#            player0 = []
#            player1 = []
#            for h in outcome:
#                if h[1][0] == 'd':
#                    player0.append(3)
#                else:
#                    player0.append(2)
#                if h[1][1] == 'd':
#                    player1.append(1)
#                else:
#                    player1.append(2)
#            x_axis = range(1, len(player0)+1)
#    
#            axs[i].plot(x_axis[start:end], player0[start:end], label="p0")
#            axs[i].plot(x_axis[start:end], player1[start:end], label="p1")
#            axs[i].set_title(str(data[outcome]/2)+'%', loc='right')
#            axs[i].set_yticks([1,2,3])
#            axs[i].set_xticks(x_axis[start:end])
#            axs[i].set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])            
#            axs[i].tick_params(
#                axis='x',          # changes apply to the x-axis
#                which='both',      # both major and minor ticks are affected
#                bottom=True,       # ticks along the bottom edge are on
#                top=True,          # ticks along the top edge are on
#                labelbottom=False) # labels along the bottom edge are off
#            i += 1            
#    else:
#        # Plot all outcomes
#        fig, axs = plt.subplots(num_outcomes, 1, figsize=(12, 2*num_outcomes))
#        fig.subplots_adjust(hspace = 0.4)
#
#        i = 0
#        for outcome in data.keys():
#            player0 = []
#            player1 = []
#            for h in outcome:
#                if h[1][0] == 'd':
#                    player0.append(3)
#                else:
#                    player0.append(2)
#                if h[1][1] == 'd':
#                    player1.append(1)
#                else:
#                    player1.append(2)
#            x_axis = range(1, len(player0)+1)
#    
#            axs[i].plot(x_axis[start:end], player0[start:end], label="p0")
#            axs[i].plot(x_axis[start:end], player1[start:end], label="p0")
#            axs[i].set_title(str(data[outcome]/2)+'%', loc='right')
#            axs[i].set_yticks([1,2,3])
#            axs[i].set_xticks(x_axis[start:end])
#            axs[i].set_yticklabels(['Agent 1 defects', 'Cooperate', 'Agent 0 defects'])
#            axs[i].tick_params(
#                axis='x',          # changes apply to the x-axis
#                which='both',      # both major and minor ticks are affected
#                bottom=True,       # ticks along the bottom edge are on
#                top=True,          # ticks along the top edge are on
#                labelbottom=False) # labels along the bottom edge are off
#            i += 1
#
#    fig.suptitle('Experiment '+setting.exp_id)
#    plt.show()
    
