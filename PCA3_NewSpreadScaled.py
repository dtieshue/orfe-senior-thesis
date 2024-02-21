import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load the CSV data
file_path = 'eod.csv'
data = pd.read_csv(file_path)

# Convert HO and RB prices to per barrel
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
pca.fit(scaled_data)
pc2_vector = pca.components_[1]  # Getting the second principal component

# Function to standardize data using the existing scaler
def standardize_data(row):
    return (row - scaler.mean_) / scaler.scale_

# Apply standardization to each day's data and calculate the projection on PC2
pivot_data['standardized_projection'] = price_data.apply(standardize_data, axis=1).dot(pc2_vector)

# Scale back the projection to the original scale
pivot_data['new_crack_spread'] = pivot_data['standardized_projection'] * scaler.scale_[0] + scaler.mean_[0]

# Plotting the new crack spread
plt.figure(figsize=(12, 6))
pivot_data.index = pd.to_datetime(pivot_data.index)  # Ensure the index is in datetime format for plotting
plt.plot(pivot_data.index, pivot_data['new_crack_spread'], label='New Crack Spread based on PC2', color='purple')

# Formatting the x-axis
six_month_locator = mdates.MonthLocator(bymonth=(6, 12))
plt.gca().xaxis.set_major_locator(six_month_locator)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('New Crack Spread Value')
plt.title('Daily New Crack Spread Over Time based on Second Principal Component')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
