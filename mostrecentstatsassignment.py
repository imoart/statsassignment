import pandas as pd
import matplotlib.pyplot as plt


def read_worldbank_data(filename):
    """
    Read the data in Worldbank format from a CSV file and return two dataframes:
    one with years as columns and one with countries as columns.

    Args:
    - filename (str): The filename of the CSV file containing the data

    Returns:
    - df_filtered (pd.DataFrame): DataFrame with filtered data
    - df_filtered_transposed (pd.DataFrame): DataFrame with filtered data transposed
    """
    # Read the data from the CSV file
    df = pd.read_csv(filename)

    # Fill missing values with 0
    df = df.fillna(0)

    # Drop unnecessary columns
    df = df.drop(df.columns[[3, -1]], axis='columns')

    # Filter the data by indicators
    indicators = ['Agricultural land (% of land area)',
                  'CO2 emissions (kt)',
                  'Forest area (sq. km)',
                  'Electric power consumption (kWh per capita)',
                  'Population growth (annual %)',
                  'Population, total',
                  'Mortality rate, under-5 (per 1,000 live births)']
    df_filtered = df[df['Indicator Name'].isin(indicators)]
    df_filtered = df_filtered.reset_index(drop=True)

    # Merge with the income data
    df2 = pd.read_csv('incomedata.csv')
    df_filtered = pd.merge(df_filtered, df2[['Country Code', 'IncomeGroup']],
                           on='Country Code', how='left')

    # Transpose the dataframe to get years as columns
    df_filtered_transposed = df_filtered.set_index(['Country Name', 'IncomeGroup']).T

    return df_filtered, df_filtered_transposed


# Usage example:
df_filtered, df_filtered_transposed = read_worldbank_data('climatedata.csv')
print("Filtered dataframe:")
print(df_filtered.head())
print("\nTransposed dataframe:")
print(df_filtered_transposed.head())

# Using .describe() to explore the data
print(df_filtered.describe())
print(df_filtered_transposed.describe())

# Defining countries by income
rich_countries = ['China']
lower_middle_income_countries = ['Iran, Islamic Rep.']
upper_middle_income_countries = ['Malasiya']
poor_countries = ['Sudan']

rich_countries = df_filtered[df_filtered['Country Name'].isin(rich_countries)]
lower_middle_income_countries = df_filtered[df_filtered['Country Name'].isin(lower_middle_income_countries)]
upper_middle_income_countries = df_filtered[df_filtered['Country Name'].isin(upper_middle_income_countries)]
poor_countries = df_filtered[df_filtered['Country Name'].isin(poor_countries)]

# rich_countries = rich_countries.drop(rich_countries.columns[-1], axis='columns')
# print(rich_countries)

country_groups = {
    'rich': ['China'],
    'lower_middle': ['Iran, Islamic Rep.'],
    'upper_middle': ['Malasiya'],
    'poor': ['Sudan']
}

# Iterate over each group
for group_name, countries in country_groups.items():
    # Filter the DataFrame for countries in the current group
    group_data = df_filtered[df_filtered['Country Name'].isin(countries)]

    # Group the filtered data by 'Country Name'
    grouped_data = group_data.groupby('Country Name')

    # Print the group name
    print(group_name)

    # Iterate over each country in the group
    for country, country_data in grouped_data:
        print(country)
        print(country_data)

#poor_countries.to_csv('pooercountry.csv')
# Define the start and end years
start_year = 1980
end_year = 2022

# Define the list of columns to include in the dataframes
columns_to_include = ['Country Name', 'Country Code', 'IncomeGroup', 'Indicator Name']

# Slice the dataframes for the most recent 20 years and the start 20 years
recent_20_years_columns = [str(year) for year in range(end_year - 20, end_year + 1)]
start_20_years_columns = [str(year) for year in range(start_year, start_year + 21)]

rich_countries_recent_20_years = rich_countries[columns_to_include + recent_20_years_columns]
rich_countries_start_20_years = rich_countries[columns_to_include + start_20_years_columns]

lower_middle_income_recent_20_years = lower_middle_income_countries[columns_to_include + recent_20_years_columns]
lower_middle_income_start_20_years = lower_middle_income_countries[columns_to_include + start_20_years_columns]

upper_middle_income_recent_20_years = upper_middle_income_countries[columns_to_include + recent_20_years_columns]
upper_middle_income_start_20_years = upper_middle_income_countries[columns_to_include + start_20_years_columns]

poor_countries_recent_20_years = poor_countries[columns_to_include + recent_20_years_columns]
poor_countries_start_20_years = poor_countries[columns_to_include + start_20_years_columns]

print('poor country:')
print(poor_countries_recent_20_years)
print(poor_countries_start_20_years)
rich_countries_recent_20_years.to_csv('test.csv')
rich_countries_start_20_years.to_csv('richstart20.csv')
lower_middle_income_recent_20_years.to_csv('lowrec20.csv')
lower_middle_income_start_20_years.to_csv('lowstart20.csv')
upper_middle_income_recent_20_years.to_csv('upprec20.csv')
upper_middle_income_start_20_years.to_csv('uppstart20.csv')
poor_countries_recent_20_years.to_csv('poorrec20.csv')
poor_countries_start_20_years.to_csv('poorstart20.csv')

print(rich_countries_recent_20_years)
print(rich_countries_start_20_years)

# Calculate moving averages for the recent 20 years and start 20 years for rich countries
rich_recent_20_years_ma = rich_countries_recent_20_years.rolling(window=5, axis=1).mean()
rich_start_20_years_ma = rich_countries_start_20_years.rolling(window=5, axis=1).mean()

# Calculate moving averages for the recent 20 years and start 20 years for lower middle income countries
lower_middle_income_recent_20_years_ma = lower_middle_income_recent_20_years.rolling(window=5, axis=1).mean()
lower_middle_income_start_20_years_ma = lower_middle_income_start_20_years.rolling(window=5, axis=1).mean()

# Calculate moving averages for the recent 20 years and start 20 years for upper middle income countries
upper_middle_income_recent_20_years_ma = upper_middle_income_recent_20_years.rolling(window=5, axis=1).mean()
upper_middle_income_start_20_years_ma = upper_middle_income_start_20_years.rolling(window=5, axis=1).mean()

# Calculate moving averages for the recent 20 years and start 20 years for poor countries
poor_countries_recent_20_years_ma = poor_countries_recent_20_years.rolling(window=5, axis=1).mean()
poor_countries_start_20_years_ma = poor_countries_start_20_years.rolling(window=5, axis=1).mean()

# Transposing 
rich_recent_20_years_ma_trans = rich_recent_20_years_ma.rename_axis('Year').T
upper_middle_income_recent_20_years_ma_trans = upper_middle_income_recent_20_years_ma.rename_axis('Year').T
lower_middle_income_recent_20_years_ma_trans = lower_middle_income_recent_20_years_ma.rename_axis('Year').T
poor_recent_20_years_ma_trans = poor_countries_recent_20_years_ma.rename_axis('Year').T
rich_start_20_years_ma_trans = rich_start_20_years_ma.rename_axis('Year').T
upper_middle_income_start_20_years_ma_trans = upper_middle_income_start_20_years_ma.rename_axis('Year').T
lower_middle_income_start_20_years_ma_trans = lower_middle_income_start_20_years_ma.rename_axis('Year').T
poor_start_20_years_ma_trans = poor_countries_start_20_years_ma.rename_axis('Year').T

# Defining variables
years = rich_recent_20_years_ma_trans.index
years2 = upper_middle_income_recent_20_years_ma_trans.index
years3 = lower_middle_income_recent_20_years_ma_trans.index
years4 = poor_recent_20_years_ma_trans.index
years5 = rich_start_20_years_ma_trans.index
years6 = upper_middle_income_start_20_years_ma_trans.index
years7 = lower_middle_income_start_20_years_ma_trans.index
years8 = poor_start_20_years_ma_trans.index

# Plotting recent 20 years for CO2 emissions
plt.figure(figsize=(10, 6))
plt.plot(years, rich_recent_20_years_ma_trans[45], label='CO2 emissions AUS')
plt.plot(years2, upper_middle_income_recent_20_years_ma_trans[794], label='CO2 emissions IRQ')
plt.plot(years3, lower_middle_income_recent_20_years_ma_trans[143], label='CO2 emissions BGD')
plt.plot(years4, poor_recent_20_years_ma_trans[1837], label='CO2 emissions YEM')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('CO2 emissions (kt) Recent 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.show()

# Plotting recent 20 years for Mortality rate 
plt.figure(figsize=(10,6))
plt.plot(years, rich_recent_20_years_ma_trans[44], label='Mortality rate AUS')
plt.plot(years2, upper_middle_income_recent_20_years_ma_trans[793], label='Mortality rate IRQ')
plt.plot(years3, lower_middle_income_recent_20_years_ma_trans[142], label='Mortality rate BGD')
plt.plot(years4, poor_recent_20_years_ma_trans[1836], label='Mortality rate YEM')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Moratlity rate Recent 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.show()

# Plotting start 20 years for CO2 emissions
plt.figure(figsize=(10,6))
plt.plot(years5, rich_start_20_years_ma_trans[45], label='CO2 emissions AUS')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans[794], label='CO2 emissions IRQ')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans[143], label='CO2 emissions BGD')
plt.plot(years8, poor_start_20_years_ma_trans[1837], label='CO2 emissions YEM')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('CO2 emissions Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.show()

# Plotting start 20 years for Mortality rate 
plt.figure(figsize=(10,6))
plt.plot(years5, rich_start_20_years_ma_trans [44], label='Mortality rate AUS')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans [793], label='Mortality rate IRQ')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans [142], label='Mortality rate BGD')
plt.plot(years8, poor_start_20_years_ma_trans[1836], label='Mortality rate YEM')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Moratlity rate Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.show()


# Plotting start 20 years for agricultural land 
plt.figure(figsize=(10,6))
plt.plot(years5, rich_start_20_years_ma_trans [44], label='Mortality rate AUS')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans [793], label='Mortality rate IRQ')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans [142], label='Mortality rate BGD')
plt.plot(years8, poor_start_20_years_ma_trans[1836], label='Mortality rate YEM')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Moratlity rate Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.show()




'''
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
# Filter the rich_countries DataFrame for 'CO2 emissions (metric tons per capita)'
co2_df = rich_countries[rich_countries['Indicator Name'] == 
                        'CO2 emissions (metric tons per capita)']

# Filter the rich_countries DataFrame for 'Forest area (sq. km)'
forest_df = rich_countries[rich_countries['Indicator Name'] == 
                           'Forest area (sq. km)']

print('The co2 df is: ')
print(co2_df)
print('The forest df is: ')
print(forest_df)
print('--------------------------------------')

# Check if both CO2 emissions and forest area data are available
if not co2_df.empty and not forest_df.empty:
    # Calculate correlation between CO2 emissions and forest area
    correlation = co2_df.corrwith(forest_df, axis=1)
    print(f'Correlation between CO2 emissions and forest area for Australia: {correlation}')
else:
    print('The co2 df is: ')
    print(co2_df)
    print('The forest df is: ')
    print(forest_df)
    print('Insufficient data available for correlation calculation for Australia')'''


