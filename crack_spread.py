import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# load data of crude oil, gasoline, and heating oil contracts
file_path = 'bins20.csv'
data = pd.read_csv(file_path)

# convert date and time to a datetime format
data['datetime'] = pd.to_datetime(data['date']) + pd.to_timedelta(data['time'], unit='min')

# # applying the display factor
# data['bid'] *= data['sym'].apply(lambda x: 0.01 if x.startswith('CL') else 0.0001)
# data['ask'] *= data['sym'].apply(lambda x: 0.01 if x.startswith('CL') else 0.0001)
# data['prc'] *= data['sym'].apply(lambda x: 0.01 if x.startswith('CL') else 0.0001)

# convert HO and RB prices to per barrel
data.loc[data['sym'].str.contains('HO') | data['sym'].str.contains('RB'), ['bid', 'ask', 'prc']] *= 42

# filter data for the desired date range
start_date = datetime(2020, 9, 14)
end_date = datetime(2020, 9, 26)
filtered_data = data[(data['datetime'] >= start_date) & (data['datetime'] <= end_date)]

# calculate crack spreads for each time
def calculate_crack_spread(row, cl_prc):
    if 'CL' in row['sym']:
        return None
    return row['prc'] - cl_prc

# add a column for crack spread
filtered_data['crack_spread'] = None

# process each time
for _, row in filtered_data.iterrows():
    if 'CL' in row['sym']:
        cl_price = row['prc']
        datetime = row['datetime']
        filtered_data.loc[filtered_data['datetime'] == datetime, 'crack_spread'] = \
            filtered_data[filtered_data['datetime'] == datetime].apply(lambda r: calculate_crack_spread(r, cl_price), axis=1)

# filter out rows without crack spread and CL rows
crack_spread_data = filtered_data.dropna(subset=['crack_spread']).loc[filtered_data['sym'] != 'CL']

# plotting
plt.figure(figsize=(15, 8))
for sym in crack_spread_data['sym'].unique():
    plt.plot(crack_spread_data[crack_spread_data['sym'] == sym]['datetime'], crack_spread_data[crack_spread_data['sym'] == sym]['crack_spread'], label=sym)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator()) 
plt.xticks(rotation=45)
plt.xlabel('DateTime')
plt.ylabel('Crack Spread')
plt.title(f'Crack Spread Over Time ({start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')})')
plt.legend()
plt.tight_layout()
plt.show()
