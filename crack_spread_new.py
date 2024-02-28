import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load data
file_path = 'bins17.csv'
data = pd.read_csv(file_path)

# Convert date and time to a datetime format
data['datetime'] = pd.to_datetime(data['date']) + pd.to_timedelta(data['time'], unit='min')

# Convert HO and RB prices to per barrel
data.loc[data['sym'].str.contains('HO') | data['sym'].str.contains('RB'), ['bid', 'ask', 'prc']] *= 42

# Filter data for the desired date range and specific contracts
start_date = datetime(2017, 8, 1)
end_date = datetime(2017, 9, 20)
filtered_data = data[(data['datetime'] >= start_date) & (data['datetime'] <= end_date)]
# filtered_data = filtered_data[filtered_data['sym'].isin(['CLU7', 'RBU7', 'HOU7', 'CLV7', 'RBV7', 'HOV7'])]
filtered_data = filtered_data[filtered_data['sym'].isin([ 'CLV7', 'RBV7', 'HOV7'])]


# Pivot the data for easier calculation
pivoted_data = filtered_data.pivot_table(index='datetime', columns='sym', values='prc')

# Calculate the 3:2:1 crack spreads
# pivoted_data['crack_spread_U7'] = -1 * (3 * pivoted_data['CLU7'] - 2 * pivoted_data['RBU7'] - pivoted_data['HOU7'])
pivoted_data['crack_spread_V7'] = -1* ( 3 * pivoted_data['CLV7'] - 2 * pivoted_data['RBV7'] - pivoted_data['HOV7'])

# Plotting
plt.figure(figsize=(15, 8))
# plt.plot(pivoted_data.index, pivoted_data['crack_spread_U7'], label='CLU7/RBU7/HOU7 Crack Spread')
plt.plot(pivoted_data.index, pivoted_data['crack_spread_V7'], label='CLV7/RBV7/HOV7 Crack Spread')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.xticks(rotation=45)
plt.xlabel('DateTime')
plt.ylabel('3:2:1 Crack Spread')
plt.title(f'3:2:1 Crack Spread for U7 and V7 Contracts ({start_date.strftime("%B %d, %Y")} - {end_date.strftime("%B %d, %Y")})')
plt.legend()
plt.tight_layout()
plt.show()
