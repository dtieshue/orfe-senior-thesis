print("hello world")
print("hello 2")


import matplotlib.pyplot as plt
import numpy as np

x = np.arange(100)
y = 2 * np.arange(100)

# Load the image using plt.imread and provide the correct file path
map = plt.imread('/Users/dylantieshue/Documents/GitHub/orfe-senior-thesis/map1.png')

# Create a single subplot
fig, ax = plt.subplots(1)

# Plot the data on the subplot
ax.plot(x, y)

# Display the image using imshow on the same subplot
ax.imshow(map, extent=[-165, 190, -75, 150])

plt.show()

