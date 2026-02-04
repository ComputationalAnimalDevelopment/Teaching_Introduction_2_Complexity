"""
A template for a CA-type model, using Game of Life update rules.
Interactive mode of matplotlib is used to visualise the results. 
"""

# Load the required modules
import random

# Installed modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# Parameters for simulation
grid_size = 50
timesteps = 300  # Number of timesteps to simulate

# Set the seed at a constant value for reproducability
# Change to get other random initial pattern
random.seed(23)  
            
# First, lets initialize the grid with a random pattern where 30% of the grid points are set to 1
initial_population = np.random.choice([0, 1], size=(grid_size, grid_size), p=[0.9, 0.1])
grid = initial_population

'''
# As an alternative initialize the grid with a glider gun in the middle
glider_gun = np.zeros((grid_size, grid_size), dtype=int)
# Coordinates for the glider gun pattern
glider_gun_coords = [
    (5, 1), (5, 2), (6, 1), (6, 2),
    (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13), (3, 14), (9, 14),
    (6, 15), (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18),
    (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23),
    (1, 25), (2, 25), (6, 25), (7, 25),
    (3, 35), (4, 35), (3, 36), (4, 36)
]
# Set the glider gun pattern on the grid
for (i, j) in glider_gun_coords:
    glider_gun[i, j] = 1
grid = glider_gun
'''

''''
#As an alternative to the default used update function in which all grid points are updates synchronously
#this method updates the grid asynchronously, meaning that the order in which the grid points are updated is randomized
def simulate_asyncstep(grid):
    # Create an array of all grid points
    grid_points = [(i, j) for i in range(grid_size) for j in range(grid_size)]
    # Randomize the order of grid points
    random.shuffle(grid_points)
    # Loop over the randomized grid points and update the grid
    for i, j in grid_points:
        # Count the number of live neighbors with torus boundary conditions
        live_neighbors = 0
        neighbors = [(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
        for ni, nj in neighbors:
            ni = ni % grid_size
            nj = nj % grid_size
            live_neighbors += grid[ni, nj] > 0
        # Apply the rules of the Game of Life
        if grid[i, j] > 0:  # Cell is alive
            if live_neighbors < 2 or live_neighbors > 3:
                grid[i, j] = 0  # Cell dies
        else:  # Cell is dead
            if live_neighbors == 3:
                grid[i, j] = 1  # Cell becomes alive
    return grid
'''

# Let's write a function that updates the entire grid once, according to the rules.
# We apply a 'synchronous' update, meaning that we first copy the old grid and use
# that grid for reference to determine what happens next. 
def simulate_step(grid):
    new_grid = grid.copy()  # Make a copy of the current grid state

    for i in range(grid_size):  # loop over all rows
        for j in range(grid_size):  # loop over all columns

            # Count the number of live neighbors with torus boundary conditions
            live_neighbors = 0
            neighbors = [(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
            
            for ni, nj in neighbors:
                ni = ni % grid_size
                nj = nj % grid_size
                live_neighbors += grid[ni, nj] > 0

            # Apply the rules of the Game of Life
            if grid[i, j] > 0:  # Cell is alive
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0  # Cell dies
            else:  # Cell is dead
                if live_neighbors == 3:
                    new_grid[i, j] = 1  # Cell becomes alive
    return new_grid


# Plotting code
fig, ax = plt.subplots(figsize=(6, 6)) # returns figure (fig) and axes (ax) so we can set these later
cols = plt.cm.viridis
cols.set_under(color='white')
norm = plt.cm.colors.Normalize(vmin=1, vmax=100)  # Range of color map
im = ax.imshow(grid, cmap=cols,norm=norm)
ax.axis("off")

def plot_grid(grid,t):
    im.set_data(grid)
    ax.set_title(f"Timestep: {t}")
    
# Finally, run the simulation and update the plots
for t in range(1, timesteps + 1):
    plot_grid(grid, t)
    plt.pause(0.01)  # Pause to refresh the plot
    grid = simulate_step(grid)

# And open the last plot. 
plt.show()