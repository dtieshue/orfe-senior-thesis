import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load the CSV data
file_path = 'eod.csv'
data = pd.read_csv(file_path)

# # convert HO and RB prices to per barrel
# data.loc[data['prs'].str.contains('HO') | data['prs'].str.contains('RB'), ['settle']] *= 42

# Revised Step 1: Identify the year and month of the contracts with the maximum sum of traded volumes for CL, RB, and HO for each day
# Grouping the data by date, year, and month, then summing the total volumes for these groups
grouped_data = data.groupby(['date', 'yr', 'mon']).sum()['totvlm'].reset_index()

# Finding the year and month combination with the maximum summed trading volume for each day
max_vol_dates = grouped_data.loc[grouped_data.groupby('date')['totvlm'].idxmax()]

# Merging the original data with the max_vol_dates to get the settle prices for the contracts with the highest volumes
merged_data = pd.merge(data, max_vol_dates, on=['date', 'yr', 'mon'])

# Step 2: Calculate the crack spread for each day
# Pivot the merged_data to make it easier to calculate the crack spread
pivot_data = merged_data.pivot_table(index='date', columns='prs', values='settle', aggfunc='first')

# Calculate the crack spread: [2 * Gasoline Price + 1 * Heating Oil Price - 3 * Crude oil price]
pivot_data['crack_spread'] = 2 * pivot_data['RB'] * 42 + pivot_data['HO'] * 42 - 3 * pivot_data['CL']

# Plotting the daily crack spread values with x-tick labels every June and December
plt.figure(figsize=(12, 6))
plt.plot(pd.to_datetime(pivot_data.index), pivot_data['crack_spread'], label='3:2:1 Crack Spread', color='blue')

# Formatting the x-axis to display labels every June and December
six_month_locator = mdates.MonthLocator(bymonth=(6, 12))
plt.gca().xaxis.set_major_locator(six_month_locator)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Crack Spread Value')
plt.title('Daily 3:2:1 Crack Spread Over Time')
plt.xticks(rotation=45)
plt.legend()

# Displaying the plot
plt.grid(True)
plt.tight_layout()
plt.show()

print(np.mean(pivot_data['crack_spread']))
print(np.std(pivot_data['crack_spread']))
print(np.max(pivot_data['crack_spread']))
print(np.min(pivot_data['crack_spread']))
