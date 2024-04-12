import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Define the data
x_values = np.array([0, 12, 24, 36, 48, 60, 72, 96, 120])  # Time points in hours
normal_values = np.array([0.071, 0.080, 0.112, 0.156, 0.184, 0.194, 0.196, 0.164, 0.155])
differenced_values = np.array([0, 0, 0.002, 0.017, 0.031, 0.030, 0.029, 0.022, 0.019])

# Creating a professional plot
plt.figure(figsize=(10, 6))

# Plotting the data
plt.plot(x_values, normal_values, label='Normal', marker='o', markersize=8, color='navy', linestyle='-', linewidth=2)
plt.plot(x_values, differenced_values, label='Differenced', marker='s', markersize=8, color='crimson', linestyle='--', linewidth=2)

# Adding title and labels with increased font size for professionalism
plt.title('Comparison of Normal and Differenced Values Over Varying Time Horizons', fontsize=16)
plt.xlabel('Outlook (hours)', fontsize=14)
plt.ylabel('R$^2$ Value', fontsize=14)

# Adding a legend and grid
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Setting the x and y axis ticks to be more readable
plt.xticks(ticks=x_values, fontsize=12)
plt.yticks(fontsize=12)

# Adjusting x-axis to display time labels more appropriately
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x)}h'))

# Show the plot
plt.tight_layout()  # Adjusts the plot to ensure everything fits without overlapping
plt.show()

