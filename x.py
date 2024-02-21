import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

# Calculate the crack spread
pivot_data['crack_spread'] = 2 * pivot_data['RB'] * 42 + pivot_data['HO'] * 42 - 3 * pivot_data['CL']

# Convert index to datetime
pivot_data.index = pd.to_datetime(pivot_data.index)

# Creating dummy variables for each month
month_dummies = pd.get_dummies(pivot_data.index.month, prefix='month')
pivot_data = pd.concat([pivot_data, month_dummies], axis=1)

# Define X (independent variables) and y (dependent variable)
X = pivot_data.drop(columns=['crack_spread', 'month_12'])  # Avoiding multicollinearity by dropping one month
y = pivot_data['crack_spread']

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Fit the linear regression model
model = sm.OLS(y, X).fit()

# Print the summary of the regression
print(model.summary())

# Plot the crack spread and fitted values
pivot_data['fitted'] = model.fittedvalues
plt.figure(figsize=(12, 6))
plt.plot(pivot_data.index, pivot_data['crack_spread'], label='Actual Crack Spread', color='blue')
plt.plot(pivot_data.index, pivot_data['fitted'], label='Fitted Values', color='red')

# Formatting the x-axis to display labels
six_month_locator = mdates.MonthLocator(bymonth=(6, 12))
plt.gca().xaxis.set_major_locator(six_month_locator)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xlabel('Date')
plt.ylabel('Crack Spread Value')
plt.title('Crack Spread and Seasonal Regression Line')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
