import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3_seaborn as sns
import glob

csv_files = glob.glob("states*.csv")
# Read and concatenate them into one DataFrame
df_list = [pd.read_csv(file) for file in csv_files]
us_census = pd.concat(df_list)

print(us_census.columns)
print(us_census.dtypes)
print(us_census.head())

# Remove dollar signs and commas
us_census['Income'] = us_census['Income'].replace('[\$,]', '', regex=True).astype(float)

gender_split = us_census['GenderPop'].str.split('_', expand=True)
us_census['Men'] = gender_split[0].str.replace('M', '')
us_census['Women'] = gender_split[1].str.replace('F', '')

# Convert to numeric
us_census['Men'] = pd.to_numeric(us_census['Men'])
us_census['Women'] = pd.to_numeric(us_census['Women'])

plt.scatter(us_census['Women'], us_census['Income'])
plt.xlabel('Number of Women')
plt.ylabel('Average Income')
plt.title('Women vs. Income')
plt.show()

us_census['Women'] = us_census['Women'].fillna(us_census['TotalPop'] - us_census['Men'])
us_census = us_census.drop_duplicates()

plt.scatter(us_census['Women'], us_census['Income'])
plt.xlabel('Number of Women')
plt.ylabel('Average Income')
plt.title('Women vs. Income (Cleaned)')
plt.show()

# Remove % and convert to float
race_cols = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
for col in race_cols:
    us_census[col] = us_census[col].str.replace('%', '')
    us_census[col] = pd.to_numeric(us_census[col])
    us_census[col] = us_census[col].fillna(us_census[col].mean())  # fill NaNs with mean\

for col in race_cols:
    plt.hist(us_census[col], bins=10, edgecolor='black')
    plt.title(f'Distribution of {col} Population %')
    plt.xlabel(f'{col} (%)')
    plt.ylabel('Number of States')
    plt.show()

# Add a new column: women proportion
us_census['Women_Proportion'] = us_census['Women'] / us_census['TotalPop']

# Scatterplot: Women Proportion vs Income
plt.scatter(us_census['Women_Proportion'], us_census['Income'])
plt.xlabel('Proportion of Women')
plt.ylabel('Average Income')
plt.title('Proportion of Women vs Income')
plt.show()


