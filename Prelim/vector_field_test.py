import matplotlib.pyplot as plt
import numpy as np

# Dummy center point for the plot (latitude, longitude)
center_point = (25, -80)  # Approximate coordinates for Miami, Florida

# Generate a grid of points around the center
grid_size = 1
x = np.arange(center_point[1] - 5, center_point[1] + 5, grid_size)
y = np.arange(center_point[0] - 5, center_point[0] + 5, grid_size)
X, Y = np.meshgrid(x, y)

# Create a tangential wind velocity field around the center point
# Using a simple rotational pattern
wind_speed = 20  # Max wind speed in arbitrary units
R = np.sqrt((X - center_point[1])**2 + (Y - center_point[0])**2)
U = -wind_speed * (Y - center_point[0]) / R
V = wind_speed * (X - center_point[1]) / R

# Replace NaN values (at the center) with 0
U[np.isnan(U)] = 0
V[np.isnan(V)] = 0

# Create the plot
plt.figure(figsize=(8, 8))
plt.quiver(X, Y, U, V, pivot='middle')

# Plot the center point
plt.plot(center_point[1], center_point[0], 'ro', markersize=10)

# Adding titles and labels
plt.title('Tangential Wind Velocity Field Around a Point')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

plt.show()
