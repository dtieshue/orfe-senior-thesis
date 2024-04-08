import matplotlib.pyplot as plt
import pandas as pd

# Reading the CSV files into pandas DataFrames
track_errors_df = pd.read_csv('1989-present_track_errors.csv')
intensity_errors_df = pd.read_csv('1990-present_intensity_errors.csv')

# Defining a list of distinct colors for the plots
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Adjusting the plot parameters to be suitable for academic papers
plt.rcParams.update({'font.size': 14, 'axes.labelweight': 'bold', 'axes.titlesize': 16, 'axes.titleweight': 'bold'})

# Plotting Track Error over time with professional styling
plt.figure(figsize=(14, 8))
for (column, color) in zip(track_errors_df.columns[1:], colors):
    if 'h' in column:  # Ensure only error columns are plotted
        plt.plot(track_errors_df['Year'], track_errors_df[column], marker='o', linestyle='-', color=color, linewidth=2, label=column)

plt.title('Track Forecast Error Over Time')
plt.xlabel('Year')
plt.ylabel('Forecast Error (nautical miles)')
plt.legend(title="Forecast Horizon", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig('track_forecast_error_academic.png', format='png', dpi=300)
plt.show()

# Plotting Intensity Error over time with professional styling
plt.figure(figsize=(14, 8))
for (column, color) in zip(intensity_errors_df.columns[1:], colors):
    if 'h' in column:  # Ensure only error columns are plotted
        plt.plot(intensity_errors_df['Year'], intensity_errors_df[column], marker='o', linestyle='-', color=color, linewidth=2, label=column)

plt.title('Intensity Forecast Error Over Time')
plt.xlabel('Year')
plt.ylabel('Forecast Error (knots)')
plt.legend(title="Forecast Horizon", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig('intensity_forecast_error_academic.png', format='png', dpi=300)
plt.show()
