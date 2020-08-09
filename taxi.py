import gym 
import numpy as np
import matplotlib.pyplot as plt
env = gym.make("Taxi-v3").env

'''
# methods:
1. env.reset: resets the environments and returns a random initial state
2. env.step(action): returns
    - observation
    - reward
    - done (boolean) - either reach the goal or end the episode
    - info - additional info such as performance and latency for debugging purposes
3. env.render: renders one frame of the environment (useful for visualization).
'''

''' the TAxi problem 
- the job is to pick up the passenger at one location
and drop him off at another
- there are 4 locations (labeled by different letters (R, G, Y, B))
    - blue letter: the current passenger pick-up locations
    - purple letter: current destination
- +20 points for a successful drop off
- -1 point for every time-step it takes
- -10 points penalty for illegal pick-up and drop-off actions

Action:
0 - south
1 - north
2 - east
3 - west
4 - pickup
5 - dropoff
'''
env.nA
env.action_space   # total number of possible actions
env.nS
env.observation_space # all possible states
env.P
env.reward_range

state = env.encode(3, 1, 2, 0) # (taxi row, taxi column, passenger index, destination index)
print("State:", state)
env.s = state
env.render()
env.P[328] # {action: [(probability, nextstate, reward, done)]}


###############################################################
# just for illustration
env.s = 328
epochs = 0
penalties = 0
reward = 0
frames = []
done = False

while not done:
    action = env.action_space.sample()
    state,reward,done,info = env.step(action)

    if reward == -10:
        penalties += 1

    # put each rendered frame into dict for animation
    frames.append(
        {
            'frame': env.render('ansi'),
            'state': state,
            'action': action,
            'reward': reward
        }
    )

    epochs += 1

print("Timesteps taken: {}".format(epochs))
print("Penalties incurred: {}".format(penalties))

from IPython.display import clear_output
from time import sleep

for i, frame in enumerate(frames):
    clear_output(wait = True)
    print(frame['frame'])
    print(f"Timestep: {i+1}")
    print(f"State: {frame['state']}")
    print(f"Action: {frame['action']}")
    print(f"Reward: {frame['reward']}")
    sleep(.05)


###############################################################

''' Q-learning
Update rule:
Q(s, a) <- (1- alpha) Q(s, a) + alpha (reward + gamma * max (Q(s', A)))
- alpha = [0,1]
- gamma = [0, 1]

Q-table approach:
1. initialize the Q-table by all zeros
2. exploring actions for each state
3. travel to next state as a result of the selected action
4. for all possible actions from the s', select the one with the highest Q-value
5. update q-table values 
6. termination? reach the goal? end of episode?

tradeoff between exploration and exploitation
- introduce epsilon - to facilitate the learning process during training
- intuitively, we can explore the action rather than exploit the best learned Q-value action
'''

# initialize the Q table
qTable = np.zeros([env.nS, env.nA])

# hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

episodes = 10000

# for plotting metrics
all_epochs = []
all_penalties = []

for i in range(0, episodes):
    state = env.reset()

    epochs, penalties = 0,0
    done = False
    
    while not done:
        if np.random.uniform(0,1) < epsilon or epochs < 100 :
            print(f"[{epochs} ]: exploration")
            action = env.action_space.sample()
        else:
            print(f"[{epochs} ]: exploitation")
            action = np.argmax(qTable[state])

        nextS, r, done, info = env.step(action)

        q = (1-alpha) * qTable[state, action] + alpha * (r + gamma * np.max(qTable[nextS, :]))
        qTable[state, action] = q

        if r == -10:
            penalties += 1

        state = nextS
        epochs += 1

    if i %100 ==0:
        print(f"Episode: {i+1}")
        #plt.imshow(qTable)
        #plt.show()

# evalute the agent's performance using q-table learned via q-learning
episodes = 10
penalties = np.zeros([episodes])
rewards = np.zeros([episodes])
timeSteps = np.zeros([episodes])

for i in range (episodes):
    print(f"Episode:{i}")
    state = env.reset()
    iteration = 0

    done = False
    while not done:
        clear_output(wait = True)
        sleep(.5)
        env.render()

        action = np.argmax(qTable[state])
        nextS, r, done, info = env.step(action)

        if r == -10:
            penalties[i] += 1

        state = nextS

        rewards[i] += r
        iteration += 1
    timeSteps[i] = iteration
    sleep(1)

