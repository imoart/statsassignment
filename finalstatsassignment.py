import pandas as pd
import matplotlib.pyplot as plt


def read_worldbank_data(filename):
    """
    Read the data in Worldbank format from a CSV file and return two 
    dataframes:
    one with years as columns and one with countries as columns.

    Args:
      - filename (str): The filename of the CSV file containing the data

    Returns:
      - df_filtered (pd.DataFrame): DataFrame with filtered data
      - df_filtered_transposed (pd.DataFrame): DataFrame with filtered data 
        transposed
    """
    # Read the data from the CSV file
    df = pd.read_csv(filename)

    # Fill missing values with 0
    df = df.fillna(0)

    # Drop unnecessary columns
    df = df.drop(df.columns[[3, -1]], axis='columns')

    # Filter the data by indicators
    indicators = [
        'Agricultural land (% of land area)',
        'CO2 emissions (kt)',
        'Forest area (sq. km)',
        'Electric power consumption (kWh per capita)',
        'Population growth (annual %)',
        'Population, total',
        'Mortality rate, under-5 (per 1,000 live births)'
    ]
    df_filtered = df[df['Indicator Name'].isin(indicators)]
    df_filtered = df_filtered.reset_index(drop=True)

    # Merge with the income data
    df2 = pd.read_csv('incomedata.csv')
    df_filtered = pd.merge(df_filtered, df2[['Country Code', 'IncomeGroup']],
                           on='Country Code', how='left')

    # Transpose the dataframe to get years as columns
    df_filtered_transposed = df_filtered.set_index(
        ['Country Name', 'IncomeGroup']).T

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
upper_middle_income_countries = ['Thailand']
poor_countries = ['Sudan']

rich_countries = df_filtered[df_filtered['Country Name'].isin(rich_countries)]
lower_middle_income_countries = df_filtered[df_filtered['Country Name'].isin(
    lower_middle_income_countries)]
upper_middle_income_countries = df_filtered[df_filtered['Country Name'].isin(
    upper_middle_income_countries)]
poor_countries = df_filtered[df_filtered['Country Name'].isin(poor_countries)]

country_groups = {
    'rich': ['China'],
    'lower_middle': ['Iran, Islamic Rep.'],
    'upper_middle': ['Thailand'],
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

# Define the start and end years
start_year = 1980
end_year = 2022

# Define the list of columns to include in the dataframes
columns_to_include = ['Country Name', 'Country Code', 'IncomeGroup',
                      'Indicator Name']

# Slice the dataframes for the most recent 20 years and the start 20 years
recent_20_years_columns = [str(year) for year in range(end_year - 20,
                                                       end_year + 1)]
start_20_years_columns = [str(year) for year in range(start_year,
                                                      start_year + 21)]

rich_countries_recent_20_years = rich_countries[columns_to_include +
                                                recent_20_years_columns]
rich_countries_start_20_years = rich_countries[columns_to_include +
                                               start_20_years_columns]

lower_middle_income_recent_20_years = lower_middle_income_countries[
    columns_to_include + recent_20_years_columns]
lower_middle_income_start_20_years = lower_middle_income_countries[
    columns_to_include + start_20_years_columns]

upper_middle_income_recent_20_years = upper_middle_income_countries[
    columns_to_include + recent_20_years_columns]
upper_middle_income_start_20_years = upper_middle_income_countries[
    columns_to_include + start_20_years_columns]

poor_countries_recent_20_years = poor_countries[columns_to_include +
                                                recent_20_years_columns]
poor_countries_start_20_years = poor_countries[columns_to_include +
                                               start_20_years_columns]

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

# Calculate moving averages for the recent 20 years and start 20 years for rich countries
rich_recent_20_years_ma = rich_countries_recent_20_years.rolling(window=5,
                                                                  axis=1).mean()
rich_start_20_years_ma = rich_countries_start_20_years.rolling(window=5,
                                                                axis=1).mean()

# Calculate moving averages for the recent 20 years and start 20 years for lower middle income countries
lower_middle_income_recent_20_years_ma = lower_middle_income_recent_20_years.rolling(
    window=5, axis=1).mean()
lower_middle_income_start_20_years_ma = lower_middle_income_start_20_years.rolling(
    window=5, axis=1).mean()

# Calculate moving averages for the recent 20 years and start 20 years for upper middle income countries
upper_middle_income_recent_20_years_ma = upper_middle_income_recent_20_years.rolling(
    window=5, axis=1).mean()
upper_middle_income_start_20_years_ma = upper_middle_income_start_20_years.rolling(
    window=5, axis=1).mean()

# Calculate moving averages for the recent 20 years and start 20 years for poor countries
poor_countries_recent_20_years_ma = poor_countries_recent_20_years.rolling(
    window=5, axis=1).mean()
poor_countries_start_20_years_ma = poor_countries_start_20_years.rolling(
    window=5, axis=1).mean()


# Transposing
rich_recent_20_years_ma_trans = rich_recent_20_years_ma.rename_axis('Year').T
upper_middle_income_recent_20_years_ma_trans = upper_middle_income_recent_20_years_ma.rename_axis(
    'Year').T
lower_middle_income_recent_20_years_ma_trans = lower_middle_income_recent_20_years_ma.rename_axis(
    'Year').T
poor_recent_20_years_ma_trans = poor_countries_recent_20_years_ma.rename_axis(
    'Year').T
rich_start_20_years_ma_trans = rich_start_20_years_ma.rename_axis('Year').T
upper_middle_income_start_20_years_ma_trans = upper_middle_income_start_20_years_ma.rename_axis(
    'Year').T
lower_middle_income_start_20_years_ma_trans = lower_middle_income_start_20_years_ma.rename_axis(
    'Year').T
poor_start_20_years_ma_trans = poor_countries_start_20_years_ma.rename_axis(
    'Year').T

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
plt.plot(years, rich_recent_20_years_ma_trans[283], label='China')
plt.plot(years2, upper_middle_income_recent_20_years_ma_trans[1634],
         label='Thailand')
plt.plot(years3, lower_middle_income_recent_20_years_ma_trans[787],
         label='Iran')
plt.plot(years4, poor_recent_20_years_ma_trans[1445], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('CO2 emissions (kt) Recent 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('CO2 emissions rec 20 years')
plt.show()

# Plotting recent 20 years for Electric Power Consumption
plt.figure(figsize=(10, 6))
plt.plot(years, rich_recent_20_years_ma_trans[284], label='China')
plt.plot(years2, upper_middle_income_recent_20_years_ma_trans[1635],
         label='Thailand')
plt.plot(years3, lower_middle_income_recent_20_years_ma_trans[788],
         label='Iran')
plt.plot(years4, poor_recent_20_years_ma_trans[1445], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Electric Power Consumption Recent 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('Electric Power Consumption Recent 20 years')
plt.show()

# Plotting start 20 years for CO2 emissions
plt.figure(figsize=(10, 6))
plt.plot(years5, rich_start_20_years_ma_trans[283], label='China')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans[1634],
         label='Thailand')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans[787],
         label='Iran')
plt.plot(years8, poor_start_20_years_ma_trans[1445], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('CO2 emissions Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('CO2 emissions start 20 years')
plt.show()

# Plotting start 20 years for Electric Power Consumption
plt.figure(figsize=(10, 6))
plt.plot(years5, rich_start_20_years_ma_trans[284], label='China')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans[1635],
         label='Thailand')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans[788],
         label='Iran')
plt.plot(years8, poor_start_20_years_ma_trans[1446], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Electric Power Consumption Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('Electric power consumption Start 20 years')
plt.show()

# Plotting start 20 years for agricultural land
plt.figure(figsize=(10, 6))
plt.plot(years5, rich_start_20_years_ma_trans[286], label='China')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans[1637],
         label='Thailand')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans[790],
         label='Iran')
plt.plot(years8, poor_start_20_years_ma_trans[1446], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Agricultural Land Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('Agriclutural land start 20 years')
plt.show()

# Plotting recent 20 years for agricultural land
plt.figure(figsize=(10, 6))
plt.plot(years5, rich_recent_20_years_ma_trans[286], label='China')
plt.plot(years6, upper_middle_income_recent_20_years_ma_trans[1637],
         label='Thailand')
plt.plot(years7, lower_middle_income_recent_20_years_ma_trans[790],
         label='Iran')
plt.plot(years8, poor_recent_20_years_ma_trans[1446], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Agricultural Land Recent 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('Agricultural land Recent 20 years')
plt.show()

# Plotting Start 20 years Forest Area
plt.figure(figsize=(10, 6))
plt.plot(years5, rich_start_20_years_ma_trans[285], label='China')
plt.plot(years6, upper_middle_income_start_20_years_ma_trans[1636],
         label='Thailand')
plt.plot(years7, lower_middle_income_start_20_years_ma_trans[789],
         label='Iran')
plt.plot(years8, poor_start_20_years_ma_trans[1447], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Forest Area Start 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('Forest Area start 20 years')
plt.show()

# Plotting Recent 20 years Forest Area
plt.figure(figsize=(10, 6))
plt.plot(years5, rich_recent_20_years_ma_trans[285], label='China')
plt.plot(years6, upper_middle_income_recent_20_years_ma_trans[1636],
         label='Thailand')
plt.plot(years7, lower_middle_income_recent_20_years_ma_trans[789],
         label='Iran')
plt.plot(years8, poor_recent_20_years_ma_trans[1447], label='Sudan')

plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Forest Area Recent 20 Years Moving Averages')

plt.legend()
plt.grid(True)
plt.savefig('Forest Area recent 20 years')
plt.show()

print('------------------------CO2 AND FOREST AREA-------------------------')

# Correlation for rich start 20 years Co2 and forest area
corr_start_r = rich_start_20_years_ma_trans[283].corr(
    rich_start_20_years_ma_trans[285])
print(corr_start_r)

# Correlation for rich recent 20 years Co2 and forest area
corr_rec_r = rich_recent_20_years_ma_trans[283].corr(
    rich_recent_20_years_ma_trans[285])
print(corr_rec_r)

# Correlation for upper start 20 years Co2 and forest area
corr_start_u = upper_middle_income_start_20_years_ma_trans[1634].corr(
    upper_middle_income_start_20_years_ma_trans[1636])
print(corr_start_u)

# Correlation for upper recent 20 years Co2 and forest area
corr_rec_u = upper_middle_income_recent_20_years_ma_trans[1634].corr(
    upper_middle_income_recent_20_years_ma_trans[1636])
print(corr_rec_u)

# Correlation for lower start 20 years Co2 and forest area
corr_start_l = lower_middle_income_start_20_years_ma_trans[787].corr(
    lower_middle_income_start_20_years_ma_trans[789])
print(corr_start_l)

# Correlation for lower recent 20 years Co2 and forest area
corr_rec_l = lower_middle_income_recent_20_years_ma_trans[787].corr(
    lower_middle_income_recent_20_years_ma_trans[789])
print(corr_rec_l)

# Correlation for poor start 20 years Co2 and forest area
corr_start_p = poor_start_20_years_ma_trans[1445].corr(
    poor_start_20_years_ma_trans[1447])
print(corr_start_p)

# Correlation for poor recent 20 years Co2 and forest area
corr_rec_p = poor_recent_20_years_ma_trans[1445].corr(
    poor_recent_20_years_ma_trans[1447])
print(corr_rec_p)

print('---------------------CO2 AND MORTALITY RATE-----------------------')

# Correlation for rich start 20 years Co2 and Mortality rate
corr_start_r_m = rich_start_20_years_ma_trans[283].corr(
    rich_start_20_years_ma_trans[282])
print(corr_start_r_m)

# Correlation for rich reecent 20 year Co2 and mortality rate
corr_rec_r_m = rich_recent_20_years_ma_trans[283].corr(
    rich_recent_20_years_ma_trans[282])
print(corr_rec_r_m)

# Correlation for upper start 20 years Co2 and mortality rate
corr_start_u_m = upper_middle_income_start_20_years_ma_trans[1634].corr(
    upper_middle_income_start_20_years_ma_trans[1633])
print(corr_start_u_m)


# Correlation for upper recent 20 years Co2 and mortality rate
corr_rec_u_m = upper_middle_income_recent_20_years_ma_trans[1634].corr(
    upper_middle_income_recent_20_years_ma_trans[1633])
print(corr_rec_u_m)

# Correlation for lower start 20 years Co2 and mortality rate
corr_start_l_m = lower_middle_income_start_20_years_ma_trans[787].corr(
    lower_middle_income_start_20_years_ma_trans[786])
print(corr_start_l_m)

# Correlation for lower recent 20 years Co2 and mortality rate
corr_rec_l_m = lower_middle_income_recent_20_years_ma_trans[787].corr(
    lower_middle_income_recent_20_years_ma_trans[786])
print(corr_rec_l_m)

# Correlation for poor start 20 years Co2 and mortality rate
corr_start_p_m = poor_start_20_years_ma_trans[1445].corr(
    poor_start_20_years_ma_trans[1444])
print(corr_start_p_m)

# Correlation for lower rceent 20 years Co2 and mortality rate
corr_rec_p_m = poor_recent_20_years_ma_trans[1445].corr(
    poor_recent_20_years_ma_trans[1444])
print(corr_rec_p_m)


print('-----------------CO2 AMD ELECTRIC POWER CONSUMPTION-------------------')

# Correlation for rich start 20 years Co2 and electric power
corr_start_r_e = rich_start_20_years_ma_trans[283].corr(
    rich_start_20_years_ma_trans[284])
print(corr_start_r_e)

# Correlation for rich recent 20 years Co2 and electric power
corr_rec_r_e = rich_recent_20_years_ma_trans[283].corr(
    rich_recent_20_years_ma_trans[284])
print(corr_rec_r_e)

# Correlation for upper start 20 years Co2 and electric power
corr_start_u_e = upper_middle_income_start_20_years_ma_trans[1634].corr(
    upper_middle_income_start_20_years_ma_trans[1635])
print(corr_start_u_e)


# Correlation for upper recent 20 years Co2 and electric power
corr_rec_u_e = upper_middle_income_recent_20_years_ma_trans[1634].corr(
    upper_middle_income_recent_20_years_ma_trans[1635])
print(corr_rec_u_e)

# Correlation for lower start 20 years Co2 and electric power
corr_start_l_e = lower_middle_income_start_20_years_ma_trans[787].corr(
    lower_middle_income_start_20_years_ma_trans[788])
print(corr_start_l_e)

# Correlation for lower recent 20 years Co2 and electric power
corr_rec_l_e = lower_middle_income_recent_20_years_ma_trans[787].corr(
    lower_middle_income_recent_20_years_ma_trans[788])
print(corr_rec_l_e)

# Correlation for poor start 20 years Co2 and electric power
corr_start_p_e = poor_start_20_years_ma_trans[1445].corr(
    poor_start_20_years_ma_trans[1446])
print(corr_start_p_e)

# Correlation for poor recemt 20 years Co2 and electric power
corr_rec_p_e = poor_recent_20_years_ma_trans[1445].corr(
    poor_recent_20_years_ma_trans[1446])
print(corr_rec_p_e)


# Plotting start 20 years for  all indicators and income groups
x = ['China', 'Thailand', 'Iran', 'Sudan']
plt.figure(figsize=(10, 6))
plt.scatter(x, [corr_start_r, corr_start_u, corr_start_l,
                corr_start_p], c='red', label='CO2 and Forest Area')
plt.scatter(x, [corr_start_r_m, corr_start_u_m, corr_start_l_m,
                corr_start_p_m], c='blue', label='CO2 and Mortality Rate')
plt.scatter(x, [corr_start_r_e, corr_start_u_e, corr_start_l_e,
                corr_start_p_e], c='green', label='CO2 and Electric Power Consumption')
plt.xlabel('Country')
plt.ylabel('Correlation Coefficient')
plt.title('Start 20 years Correlation')
plt.legend()
plt.grid(True)
plt.savefig('Start 20 years Correlation')
plt.show()

# Plotting recent 20 years for all indicators and income groups
x = ['China', 'Thailand', 'Iran', 'Sudan']
plt.figure(figsize=(10, 6))
plt.scatter(x, [corr_rec_r, corr_rec_u, corr_rec_l,
                corr_rec_p], c='red', label='CO2 and Forest Area')
plt.scatter(x, [corr_rec_r_m, corr_rec_u_m, corr_rec_l_m,
                corr_rec_p_m], c='blue', label='CO2 and Mortality Rate')
plt.scatter(x, [corr_rec_r_e, corr_rec_u_e, corr_rec_l_e,
                corr_rec_p_e], c='green', label='CO2 and Electric Power Consumption')
plt.xlabel('Country')
plt.ylabel('Correlation Coefficient')
plt.title('Recent 20 years Correlation')
plt.legend()
plt.grid(True)
plt.savefig('Recent 20 years Correlation')
plt.show()

