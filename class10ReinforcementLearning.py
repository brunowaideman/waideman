# -*- coding: utf-8 -*-
import numpy as np
import random
import os

world_states = [[9, 9 , 9 , 9 , 9],
                [9, 0 , 1 , 2 , 9],
                [9, 3 , 4 , 5 , 9],
                [9, 9 , 9 , 9 , 9]]

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def walk(i, j, a):
    global world_states
    d = 0
    if a == 0:
        d = world_states[i][j-1]
    elif a == 1:
        d = world_states[i][j+1]
    elif a == 2:
        d = world_states[i-1][j]
    elif a == 3:
        d = world_states[i+1][j]
    else:
        print('ERROR')
    return d

def main():

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%   Q - LEARNING  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    global world_states

    gamma = 0.5 # discount factor
    alpha = 0.5 # learning rate
    epsilon = 0.9 # exploration probability
    state = [0,1,2,3,4,5] # states
    action = [0,1,2,3] #  ['<','>','/\','\/']  actions
    # initial Q matrix
    Q = np.random.rand(len(state), len(action))
    Q = np.array([Q, np.zeros([1, len(action)])])

    K = 400 # Max iterations
    r = [0, 0, 0, 0, 0, 5]
    h = random.choice([0,1,2,3,4,5])
    state_idx = h   # the initial state to begin from
    world_start_actions = [random.choice([0,1,2,3]) for _ in range(6)]
    c = 0
    world = [ ['#', '#', '#', '#', '#'],
              ['#', '0', '0', '0', '#'],
              ['#', '0', '0', '0', '#'],
              ['#', '#', '#', '#', '#']]
    world_actions = [[9, 9, 9, 9, 9],
                      [9, 0, 0, 0, 9],
                      [9, 0, 0, 0 , 9],
                      [9, 9, 9, 9, 9]]
    for x in range(4):
        for y in range(5):
            if world_actions[x][y] != 9:
                world_actions[x][y] = world_start_actions[c];
                c = c + 1
    for i in range(4):
        for j in range(5):
            if world_states[i][j] == state_idx:
                world[i][j] = "X"
            elif world_states[i][j] == 5:
                world[i][j] = "G"

    print('\n\t#####################################################')
    print('\t################ Q - Learning world #################')
    print('\t#####################################################')
    print('\n\n\tinitial world:')
    for x in world: print(x)
    print('\n\tActions: <  >  /\  \/')
    print('\nPress any key to continue the iteractions...')

    for k in range(K):
        # % state_idx => current state
        # % current_action => current action
        # % next_reward => next reward

        while (state_idx != 5):
            os.system('clear')
            if k >= (2*K/3):
                ra = np.random.rand(1)
                xr=sum(ra>=np.cumsum([0, 1-epsilon, epsilon]))
                if xr == 1:
                    umax = Q[0][state_idx].tolist().index(max(Q[0][state_idx]))
                    current_action = action[umax]
                else:
                    current_action = random.choice(action)
            else:
                umax = Q[0][state_idx].tolist().index(max(Q[0][state_idx]))
                current_action = action[umax]

            action_idx = action[current_action]

            next_state = 0
            for i in range(4):
                for j in range(5):
                    if world[i][j] == 'X':
                        next_state = walk(i,j,current_action)

            if next_state != 9:
                # next_state_idx = find(state == next_state);
                next_state_idx = state.index(next_state)
                next_reward = r[next_state_idx]
            else:
                next_state_idx = state_idx
                next_reward = -5

            for i in range(4):
                for j in range(5):
                    if world[i][j] == 'X':
                        world[i][j] = '0'

            for i in range(4):
                for j in range(5):
                    if world_states[i][j] == next_state_idx:
                        world[i][j] = 'X'
            # Update Q function
            Q[0][state_idx][action_idx] = Q[0][state_idx][action_idx] + alpha * \
                (next_reward + gamma * max(Q[0][next_state_idx]) - Q[0][state_idx][action_idx])

            # Update the current state
            state_idx = next_state_idx
            print('\tCurrent state of world\n')
            for x in world: print('\t' + str(x))
            print('\n\tQ matrix values:\n')
            print(Q)
            pause()
        print('ROBOT WON!!!!!!!!!!!!!!!!!!!!!!')
        pause()
        # os.system('clc')
        print('Episode: ' + str(k) + ' of ' + str(K))
        world[2][3] = 'G'
        pause()

        h = random.choice([0,1,2,3,4])
        state_idx = h

        for i in range(4):
            for j in range(5):
                if world_states[i][j] == state_idx:
                    world[i][j] = 'X'



if __name__ == '__main__':
    main()
