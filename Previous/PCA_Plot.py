import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load the CSV data
file_path = 'eod.csv'
data = pd.read_csv(file_path)

# # convert HO and RB prices to per barrel
data.loc[data['prs'].str.contains('HO') | data['prs'].str.contains('RB'), ['settle']] *= 42

# Grouping the data by date, year, and month, then summing the total volumes for these groups
grouped_data = data.groupby(['date', 'yr', 'mon']).sum()['totvlm'].reset_index()

# Finding the year and month combination with the maximum summed trading volume for each day
max_vol_dates = grouped_data.loc[grouped_data.groupby('date')['totvlm'].idxmax()]

# Merging the original data with the max_vol_dates to get the settle prices for the contracts with the highest volumes
merged_data = pd.merge(data, max_vol_dates, on=['date', 'yr', 'mon'])

# Pivot the merged_data to focus on the 'settle' prices
pivot_data = merged_data.pivot_table(index='date', columns='prs', values='settle', aggfunc='first')
price_data = pivot_data[['HO', 'RB', 'CL']].dropna()

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(price_data)

# Apply PCA
pca = PCA(n_components=3)
principal_components = pca.fit_transform(scaled_data)

# Creating the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotting the original data points
ax.scatter(price_data['CL'], price_data['RB'], price_data['HO'], c='blue', marker='o', alpha=0.5, s=10)

# Preparing to plot the principal components
mean_vals = scaler.mean_
components = pca.components_
length = 200  # Determines length of the PCA vectors


# Custom function to plot principal components
def plot_principal_component(component, color, label):
    end_point = mean_vals + component * length
    ax.plot([mean_vals[2], end_point[2]], [mean_vals[1], end_point[1]], [mean_vals[0], end_point[0]], 
            color=color, linewidth=3, label=label)

# Plotting principal components with legends
plot_principal_component(components[0], 'red', '1st Principal Component')
plot_principal_component(components[1], 'green', '2nd Principal Component')
plot_principal_component(components[2], 'yellow', '3rd Principal Component')

# print(components[0])
# print(components[1])
# print(components[2])

# print(scaler.mean_)
# print(scaler.var_)
# print(scaler.scale_)


# Setting labels, title, and adjusting the viewing angle
ax.set_xlabel('Crude Oil Futures (CL)')
ax.set_ylabel('Gasoline Futures (RB)')
ax.set_zlabel('Heating Oil Futures (HO)')
ax.set_title('3D Plot of Oil Futures with PCA Components')
ax.view_init(elev=10., azim=45)

# Adding the legend
ax.legend()

# Display the plot
plt.show()