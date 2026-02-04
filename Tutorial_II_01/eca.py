"""
This code simulates elementary CAs
It prints a space-time plot of the CA behaviour
"""

import numpy as np
import matplotlib.pyplot as plt

ncells    = 200                # Number of cells
ntsteps   = 100                # Number of time steps
nextstate = [0,1,1,0,1,0,1,0]  # Define the next states for 000, 001, 010, etc

states = np.zeros((ntsteps, ncells), dtype=int)  # Create matrix to store results
init_states = np.random.randint(2, size=ncells)  # Define the initial states (random choice between 0 and 1 for each cell)
states[0,:] = init_states                        # Store the initial states in the result matrix

# The Time loop
for i in range(1, ntsteps):
    inputtime = i-1

    # Loop over all cells that are not at the boundary and determine their next state
    for j in range(1, ncells-1):
        nei_binary  = 4*states[inputtime,j-1] + 2*states[inputtime,j] + states[inputtime,j+1]
        states[i,j] = nextstate[nei_binary]

    # For index 0, include index (ncells-1) as left neighbour
    nei_binary = 4*states[inputtime,ncells-1] + 2*states[inputtime,0] + states[inputtime,1]
    states[i,0] = nextstate[nei_binary]

    # For index (ncells-1), include index 0 as right neighbour
    nei_binary = 4*states[inputtime,ncells-2] + 2*states[inputtime,ncells-1] + states[inputtime,0]
    states[i,ncells-1] = nextstate[nei_binary]

# Plot the space-time diagram
plt.matshow(states, cmap = 'Greys')
plt.ylabel("Time", fontsize = 24)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.show()