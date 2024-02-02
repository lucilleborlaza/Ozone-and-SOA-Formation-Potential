# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:52:47 2023
This script is to prepare the OFP calculations.
@author: lb945465
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

# Load VOC_conc
VOC_conc = pd.read_excel(r"C:\mydata\Optimal solution\ICDN\SOAP\Bronx_conc.xls", index_col="Date")
VOC_conc.drop(columns="TVOC", inplace=True)

# Convert the index of both DataFrames to datetime
VOC_conc.index = pd.to_datetime(VOC_conc.index)

# Checkpoint: Display VOC_conc
print(VOC_conc.head())

# Load Residuals
Residuals = pd.read_excel(r"C:\mydata\Optimal solution\ICDN\SOAP\Residuals_unscaled.xlsx", index_col="Date")

# Set "Date_Time" as the index and drop the "TVOC" column if it still exists in the DataFrame
if 'TVOC' in Residuals.columns:
    Residuals.drop(columns="TVOC", inplace=True)

# Convert the index to datetime
Residuals.index = pd.to_datetime(VOC_conc.index)

# Checkpoint: Display Residuals
print(Residuals.head())

# Load Profiles worksheet
profiles_worksheet = pd.read_excel(r"C:\mydata\Optimal solution\ICDN\Base_results.xlsx",
                                  sheet_name="Profiles_norm_specie")

# Drop the first column and set the second column as index
profiles_worksheet.set_index("Species", inplace=True)

# Rename columns to 'Factor 1', 'Factor 2', etc.
profiles_worksheet.columns = ['Factor ' + str(i) for i in range(1, len(profiles_worksheet.columns) + 1)]
profiles_worksheet = profiles_worksheet.drop("TVOC")

# Checkpoint: Display PMF_percentage
print(profiles_worksheet.head())
PMF_percentage=profiles_worksheet

# Load MIR
Prop_Score = pd.read_excel(r"C:\mydata\Optimal solution\ICDN\SOAP\Prop_Score.xlsx", sheet_name="SOAP", index_col="Species")

# Create a dataframe of modelled VOC
aligned_VOC_conc, aligned_Residuals = VOC_conc.align(Residuals)
VOC_modelled = aligned_VOC_conc.sub(aligned_Residuals)

# Checkpoint: Display VOC_modelled
print(VOC_modelled.head())

# Step 1 & 2: Get the VC_ratio value and find its inverse
df_vc = pd.read_excel(r"C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Spyder\ICDN-PMF Article\VC_clean.xlsx",
                   index_col="Date", parse_dates=True)

# Merge the dataframes on the 'Date' column to get the VC_ratio values in the same dataframe
VOC_unnorm = VOC_modelled.merge(df_vc['VC_ratio'], left_index=True, right_index=True, how='left')

# Create a new column for each column in df_contributions, normalized by the VC_ratio value
for col in VOC_unnorm.columns:
    VOC_unnorm[col] = VOC_unnorm[col] / VOC_unnorm['VC_ratio']

# Remove the VC_ratio column as it is no longer needed
VOC_unnorm.drop(columns=['VC_ratio'], inplace=True)

# Assuming the alignment is handled correctly, for example:
OFP = VOC_unnorm.mul(Prop_Score.reindex(VOC_unnorm.columns)['P'], axis=1)

# Checkpoint: Display OFP
print(OFP.head())

# Calculating the OFP per source
OFP_Factors = {}

# Iterate over the columns of PMF_percentage DataFrame
for col in PMF_percentage.columns:
    OFP_Factor = (OFP.mul(PMF_percentage[col]))
    OFP_Factor['OFP_' + col + '_total'] = OFP_Factor.sum(axis=1)
    OFP_Factors[col] = OFP_Factor

# Checkpoint: Display one of the OFP_Factor DataFrames
print(OFP_Factors['Factor 2'])

# Combine the total columns into a single DataFrame
OFP_total = pd.concat({k: df['OFP_' + k + '_total'] for k, df in OFP_Factors.items()}, axis=1)

# Checkpoint: Display OFP_total
print(OFP_total.head())

# Save OFP_total DataFrame to an Excel file
OFP_total.to_excel(r"C:\mydata\Optimal solution\ICDN\SOAP\SOAP_total.xlsx")

# Define the colors for specific column names
color_mapping = {
    "Fuel evaporation": "#1f77b4",   # blue
    "Combustion": "#ff7f0e",   # orange
    "Natural gas": "#2ca02c",   # green
    "Diesel traffic": "#d62728",   # red
    "Industrial solvents": "#9467bd",   # purple
    "Gasoline traffic": "#8c564b",   # brown
    "Biogenic": "#e377c2", # pink
    #"Urban mix": "#7f7f7f", # gray
    }

# Load the existing DataFrame
file_path = r"C:\mydata\Optimal solution\ICDN\SOAP\SOAP_total.xlsx"
OFP_total = pd.read_excel(file_path, index_col="Date")

# Calculate the mean and standard error for each column
means = OFP_total.mean()
standard_errors = OFP_total.sem()

# Calculate the 95% confidence interval
confidence_level = 0.95
degrees_freedom = OFP_total.shape[0] - 1
confidence_intervals = standard_errors * stats.t.ppf((1 + confidence_level) / 2, degrees_freedom)

# Create a new DataFrame containing means and confidence intervals
data = pd.DataFrame({
    'Mean': means,
    'Confidence Interval': confidence_intervals
}).sort_values(by='Mean')

# Assign colors based on color_mapping
colors = [color_mapping.get(col, "#333333") for col in data.index]  # default to grey if category not in mapping

# Set up the matplotlib figure
plt.figure(figsize=(8, 5), dpi=300)

# Draw a bar plot with error bars representing 95% confidence intervals
ax = sns.barplot(x=data.index, y=data['Mean'], yerr=data['Confidence Interval'], palette=colors)

# Set labels and title
plt.ylabel('SOA Formation Potential (ppbv)')
plt.title('SOA Formation Potential by Factor in Bronx')

# Annotate bars with the mean value
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.3f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 10), 
                textcoords = 'offset points')

# Rotate x labels for better readability
plt.xticks(rotation=45, fontsize=12)

# Save the figure with a transparent background
plt.savefig("SOA_barplot.png", bbox_inches='tight', transparent=True, dpi=300)

# Show the plot
plt.show()

# After loading OFP_total_Queens DataFrame
OFP_total['Month'] = OFP_total.index.month

# Create a dictionary to map months to seasons
seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
           6: 'Summer', 7: 'Summer', 8: 'Summer',
           9: 'Fall', 10: 'Fall', 11: 'Fall', 12: 'Winter'}

# Map the 'Month' column to a new 'Season' column using the dictionary
OFP_total['Season'] = OFP_total['Month'].map(seasons)

# Drop the 'Month' column as it is no longer needed
OFP_total.drop('Month', axis=1, inplace=True)

# Group the DataFrame by 'Season' and calculate the sum of each group
seasonal_data = OFP_total.groupby('Season').mean()

# Assign colors based on color_mapping
stacked_colors = [color_mapping.get(col, "#333333") for col in seasonal_data.columns] 

# Set up the matplotlib figure
plt.figure(figsize=(5, 5), dpi=200)

# Draw a stacked bar plot
ax = seasonal_data.plot(kind='bar', stacked=True, color=stacked_colors, figsize=(5,5))

# Set labels and title
plt.xlabel('')
plt.ylabel('SOA Formation Potential (ppbv)')
plt.title('Seasonal SOA Formation Potential by Factor in Bronx', fontsize=10)

# Rotate x labels for better readability
plt.xticks(rotation=45, fontsize=10)

# Move the legend to the right side
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Save the figure with a transparent background
plt.savefig("SOAP_stacked_barplot.png", bbox_inches='tight', transparent=True, dpi=300)

# Show the plot
plt.show()

# Normalize the seasonal data
normalized_data = seasonal_data.div(seasonal_data.sum(axis=1), axis=0)

# Set up the matplotlib figure
plt.figure(figsize=(5, 5), dpi=200)

# Draw a normalized stacked bar plot
ax = normalized_data.plot(kind='bar', stacked=True, color=stacked_colors, figsize=(5,5))

# Set labels and title
plt.xlabel('')
plt.ylabel('Normalized SOA Formation Potential')
plt.title('Normalized Seasonal SOA Formation Potential by Factor in Bronx', fontsize=10)

# Rotate x labels for better readability
plt.xticks(rotation=45, fontsize=10)

# Move the legend to the right side
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Save the figure with a transparent background
plt.savefig("SOAP_normalized_barplot.png", bbox_inches='tight', transparent=True, dpi=300)

# Show the plot
plt.show()

