"""
This code implements a **Q-learning** algorithm where an agent learns an optimal policy for navigating a grid-based environment.
The agent explores the grid, receives rewards, and adjusts its Q-values to improve its strategy. Key features include:

---

### **How the Code Works:**
1. **Q-Table and Visit Count Initialization**:
   - Each valid state-action pair is initialized with a Q-value of 0.
   - The visit count for each state-action pair starts at 1 to avoid division by zero errors in exploration.

2. **Exploration vs. Exploitation (ε-greedy strategy)**:
   - **Exploration**: Select actions with higher probability if they have been visited fewer times (using inverse counts).
   - **Exploitation**: Choose the action with the highest Q-value for a given state when not exploring.
   - The combination allows the agent to balance between learning new behaviors and leveraging known rewards.

3. **Action Noise**:
   - The agent’s intended action may change with some probability due to noise, simulating real-world uncertainties.

4. **Learning and Q-value Updates**:
   - The Q-value is updated using the **Bellman equation**, which considers immediate reward and future expected rewards.

5. **Rewards and Terminal States**:
   - The agent receives rewards based on its position:
     - `1` for reaching the goal.
     - `-1` for falling into a trap.
     - A small negative living reward (`-0.01`) to encourage faster completion.

6. **Decay of Exploration Probability (ε)**:
   - The exploration probability `epsilon` decays after each episode, reducing random exploration over time.

7. **Optimal Policy Extraction**:
   - After training, the optimal policy is extracted from the Q-table and printed as a grid.

---

### **Functions and Their Inputs/Outputs**

1. **`init_Q_and_counts(rows, cols, actions)`**:
   - **Input**:
     - `rows`, `cols`: Dimensions of the grid.
     - `actions`: List of possible actions.
   - **Output**:
     - `Q`: A dictionary storing Q-values initialized to 0 for all state-action pairs.
     - `counts`: A dictionary storing visit counts initialized to 1.

2. **`choose_action(state, Q, counts, epsilon)`**:
   - **Input**:
     - `state`: Current state.
     - `Q`: Q-values table.
     - `counts`: Visit counts.
     - `epsilon`: Probability of exploration.
   - **Output**:
     - Selected action using ε-greedy strategy, favoring unvisited actions during exploration.

3. **`update_Q_and_counts(Q, counts, state, action, reward, next_state, alpha)`**:
   - **Input**:
     - `Q`: Q-values table.
     - `counts`: Visit counts.
     - `state`, `action`: Current state and action taken.
     - `reward`: Reward received.
     - `next_state`: Next state after the action.
     - `alpha`: Learning rate.
   - **Output**: Updated Q-values and visit counts.

4. **`get_reward(new_row, new_col)`**:
   - **Input**:
     - `new_row`, `new_col`: New position.
   - **Output**: Reward associated with the new position.

5. **`run_Q_learning(Q, counts, alpha, epsilon, episodes, noise)`**:
   - **Input**:
     - `Q`: Q-values table.
     - `counts`: Visit counts.
     - `alpha`: Learning rate.
     - `epsilon`: Exploration probability.
     - `episodes`: Number of training episodes.
     - `noise`: Probability of action noise.
   - **Output**: Q-values updated through multiple episodes.

6. **`print_optimal_policy(Q, grid)`**:
   - **Input**:
     - `Q`: Q-values table.
     - `grid`: The environment grid.
   - **Output**: Prints the optimal policy as a grid.

---

### **Environment Parameters and Inputs**

1. **`grid`** (2D List):
   - **Description**:
     - A 2D grid representing the environment where the agent interacts.
     - Each cell can contain:
       - `None`: Empty space where the agent can move freely.
       - `'Wall'`: Obstacle, which the agent cannot pass through.
       - `1`: Goal with a positive reward.
       - `-1`: Trap with a negative reward.
       - `'Start'`: Starting position of the agent.
   - **Example**:
     ```python
     grid = [
         [None, None, None, 1],  # 1 represents the goal
         [None, 'Wall', None, -1],  # -1 represents a trap
         ['Start', None, None, None]  # 'Start' is the agent's starting position
     ]
     ```

2. **`discount`** (Float):
   - **Description**:
     - Discount factor that determines the importance of future rewards.
     - A value closer to 1 means the agent considers future rewards almost as important as immediate rewards.
     - A value closer to 0 makes the agent short-sighted, focusing only on immediate rewards.
   - **Example**: `discount = 1`

3. **`noise`** (Float):
   - **Description**:
     - The probability that an intended action will be replaced by a random action.
     - Higher noise means more randomness, reducing the agent’s ability to precisely control its actions.
   - **Example**: `noise = 0.1`

4. **`livingReward`** (Float):
   - **Description**:
     - A small negative reward given at each step to encourage the agent to find the shortest path to the goal.
     - If this reward is positive, the agent might prefer to take more steps to accumulate rewards.
   - **Example**: `livingReward = -0.01`

5. **`iterations`** (Integer):
   - **Description**:
     - Number of training episodes the agent will run.
     - More episodes allow the agent to explore the environment and improve the policy.
   - **Example**: `iterations = 2000`

6. **`actions`** (Dictionary):
   - **Description**:
     - A dictionary mapping action names to movement directions.
   - **Example**:
     ```python
     actions = {
         'UP': (-1, 0),
         'DOWN': (1, 0),
         'LEFT': (0, -1),
         'RIGHT': (0, 1)
     }
     ```

---

### **Outputs**

2. **Optimal Policy (Printed Output)**:
   - The optimal policy is extracted from the Q-table after training.
   - Each cell displays the best action to take from that state.
   - **Example Output**:
     ```
     |  N ||  N ||  E ||  x |
     |  N ||  # ||  E ||  x |
     |  S ||  E ||  E ||  S |
     ```

   - **Explanation of Symbols**:
     - `N`: Move North.
     - `S`: Move South.
     - `E`: Move East.
     - `#`: Wall or obstacle.
     - `x`: Terminal state (goal or trap).
     - Empty cells (` `) indicate states where no valid Q-value exists.

---

### **Main Execution Block**
This block initializes the environment, runs Q-learning, and prints the optimal policy.

"""


"""
### **Experiment Results Summary**

After running the code **20 times**, the following distinct outcomes were observed. 
The results demonstrate different policies learned by the agent, reflecting both successful pathfinding and the impact of noise on strategy selection.

---

### **Observed Results**

1. **Frequency: 1 Time**
   | E || E || E || x |
   | S || # || W || x |
   | E || E || N || S |

2. **Frequency: 15 Times**
   | E || E || E || x |
   | N || # || W || x |
   | N || W || W || S |

3. **Frequency: 2 Times**
   | E || E || E || x |
   | N || # || W || x |
   | N || S || N || S |

4. **Frequency: 1 Time**
   | E || E || E || x |
   | S || # || W || x |
   | E || E || N || S |

5. **Frequency: 1 Time**
   | E || E || E || x |
   | N || # || W || x |
   | N || W || N || S |

---

### **Analysis of Results**
1. **Consistency Across Runs**:
   - **First Row Pattern**: 
     - In almost all results, the agent consistently moves **East (E)** along the first row. 
     - This indicates that the learned policy prioritizes a straightforward and efficient path toward the goal (x).

2. **Variations in Second and Third Rows**:
   - **Second and third rows** show more variation in the selected actions, especially in the **North (N)**, **South (S)**, and **West (W)** directions.
   - These variations reflect the **exploration-exploitation trade-off** where the agent balances exploring alternative paths with using known optimal strategies.

3. **Impact of Noise**:
   - Some variations in actions, such as switching between **N** and **S** in certain runs, are likely due to the **action noise** introduced during training.
   - Noise causes occasional deviations from the optimal policy, leading to less consistent behavior in certain states.

4. **Exploration Behavior**:
   - In certain outcomes (e.g., results 3 and 5), the agent explores alternative actions such as moving **West (W)** or oscillating between **N** and **S**.
   - This behavior highlights the influence of the **ε-greedy strategy**, which encourages the agent to explore unvisited paths even after identifying a seemingly optimal route.

5. **Common Path to Goal**:
   - Despite these variations, every policy successfully guides the agent to the goal (x).
   - This indicates that the agent has learned **multiple feasible strategies**, even though some may be slightly less efficient.
"""



import random

# Initialize Q-table and visit counts
def init_Q_and_counts(rows, cols, actions):
    Q = {}
    counts = {}
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] is None or grid[row][col] == 'Start':
                Q[(row, col)] = {a: 0 for a in actions}
                counts[(row, col)] = {a: 1 for a in actions}  # Initialize counts to avoid division by zero
    return Q, counts

# Choose an action using ε-greedy strategy with enhanced exploration
def choose_action(state, Q, counts, epsilon):
    total_visits = sum(counts[state].values())
    action_probs = {a: (1 / counts[state][a]) for a in actions}  # Higher chance for unvisited actions
    actions_list, weights = zip(*action_probs.items())
    if random.random() < epsilon:
        return random.choices(actions_list, weights=weights)[0]  # Randomly explore
    else:
        return max(Q[state], key=Q[state].get)  # Exploit known information

# Update Q-values and visit counts
def update_Q_and_counts(Q, counts, state, action, reward, next_state, alpha):
    future_rewards = max(Q[next_state].values()) if next_state in Q else 0
    Q[state][action] += alpha * (reward + discount * future_rewards - Q[state][action])
    counts[state][action] += 1  # Increment visit count

# Get the reward for the new position
def get_reward(new_row, new_col):
    if grid[new_row][new_col] == 1:
        return 1
    elif grid[new_row][new_col] == -1:
        return -1
    else:
        return livingReward

# Run Q-learning algorithm across multiple episodes
def run_Q_learning(Q, counts, alpha, epsilon, episodes, noise):
    true_direction_with_noise = {
        'UP': ['UP', 'RIGHT', 'LEFT'],
        'DOWN': ['DOWN', 'RIGHT', 'LEFT'],
        'RIGHT': ['RIGHT', 'UP', 'DOWN'],
        'LEFT': ['LEFT', 'UP', 'DOWN']
    }

    for episode in range(episodes):
        row, col = 2, 0  # Start position
        while True:
            state = (row, col)
            intended_action = choose_action(state, Q, counts, epsilon)

            # Determine actual action with noise
            possible_actions = true_direction_with_noise[intended_action]
            action_probabilities = [1 - 2 * noise, noise, noise]
            chosen_action = random.choices(possible_actions, action_probabilities)[0]

            # Get movement direction
            dr, dc = actions[chosen_action]
            new_row, new_col = row + dr, col + dc

            # Boundary and obstacle checks
            if new_row < 0 or new_row >= len(grid) or new_col < 0 or new_col >= len(grid[0]) or grid[new_row][new_col] == 'Wall':
                new_row, new_col = row, col

            # Update Q-table and counts
            reward = get_reward(new_row, new_col)
            next_state = (new_row, new_col)
            update_Q_and_counts(Q, counts, state, intended_action, reward, next_state, alpha)

            if grid[new_row][new_col] in [1, -1]:  # Terminal state
                break

            row, col = new_row, new_col  # Update current position

        epsilon *= 0.99  # Decay epsilon

# Print the optimal policy based on the Q-table
def print_optimal_policy(Q, grid):
    direction_symbols = {'UP': 'N', 'DOWN': 'S', 'LEFT': 'W', 'RIGHT': 'E'}
    policy_grid = []

    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            cell = grid[i][j]
            if cell == 'Wall':
                row.append('#')
            elif isinstance(cell, (int, float)):
                row.append('x')
            elif cell is None or cell == 'Start':
                if (i, j) in Q:
                    best_action = max(Q[(i, j)], key=Q[(i, j)].get)
                    row.append(direction_symbols[best_action])
                else:
                    row.append(' ')
            else:
                row.append(' ')
        policy_grid.append(row)

    output_str = ""
    for row in policy_grid:
        output_str += "| " + " || ".join(row) + " |\n"

    print(output_str)

if __name__ == "__main__":
    discount = 1
    noise = 0.1
    livingReward = -0.01
    iterations = 2000
    grid = [
        [None, None, None, 1],
        [None, 'Wall', None, -1],
        ['Start', None, None, None]
    ]
    actions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

    # Initialize Q-table and visit counts
    Q, counts = init_Q_and_counts(len(grid), len(grid[0]), actions)

    # Run Q-learning
    run_Q_learning(Q, counts, alpha=0.5, epsilon=0.2, episodes=iterations, noise=noise)

    # Print the optimal policy based on learned Q-values
    print_optimal_policy(Q, grid)

