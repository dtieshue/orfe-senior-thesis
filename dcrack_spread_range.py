import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# # Nicholas
# start_date = '2019-09-01'  # Change to your desired start date
# end_date = '2019-09-30'    # Change to your desired end date

# Beta
start_date = '2020-09-18'  # Change to your desired start date
end_date = '2021-09-18'    # Change to your desired end date

# # Harvey
# start_date = '2017-08-01'  # Change to your desired start date
# end_date = '2017-09-30'    # Change to your desired end date

# Load the CSV data
file_path = 'eod.csv'
data = pd.read_csv(file_path)

# Grouping the data by date, year, and month, then summing the total volumes for these groups
grouped_data = data.groupby(['date', 'yr', 'mon']).sum()['totvlm'].reset_index()

# Finding the year and month combination with the maximum summed trading volume for each day
max_vol_dates = grouped_data.loc[grouped_data.groupby('date')['totvlm'].idxmax()]

# Merging the original data with the max_vol_dates to get the settle prices for the contracts with the highest volumes
merged_data = pd.merge(data, max_vol_dates, on=['date', 'yr', 'mon'])

# Pivot the merged_data to make it easier to calculate the crack spread
pivot_data = merged_data.pivot_table(index='date', columns='prs', values='settle', aggfunc='first')

# Calculate the crack spread: [2 * Gasoline Price + 1 * Heating Oil Price - 3 * Crude oil price]
pivot_data['crack_spread'] = 2 * pivot_data['RB'] * 42 + pivot_data['HO'] * 42 - 3 * pivot_data['CL']

# Convert the index to datetime if it's not already
pivot_data.index = pd.to_datetime(pivot_data.index)

# Filter the data to include only the dates within the specified range
filtered_data = pivot_data[(pivot_data.index >= start_date) & (pivot_data.index <= end_date)]

# Plotting the crack spread for the specified date range
plt.figure(figsize=(12, 6))
plt.plot(filtered_data.index, filtered_data['crack_spread'], label='3:2:1 Crack Spread', color='blue')

# Formatting the x-axis to display labels every June and December (or adjust as needed)
six_month_locator = mdates.MonthLocator(bymonth=(6, 12))
plt.gca().xaxis.set_major_locator(six_month_locator)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Crack Spread Value')
plt.title('3:2:1 Crack Spread from ' + start_date + ' to ' + end_date)
plt.xticks(rotation=45)
plt.legend()

# Displaying the plot
plt.grid(True)
plt.tight_layout()
plt.show()
