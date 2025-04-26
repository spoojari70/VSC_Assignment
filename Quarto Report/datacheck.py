import pandas as pd
import numpy as np

# Load mortality data
mortality = pd.read_csv('unicef_indicator_2.csv')

# Clean and filter
mortality_clean = (
    mortality[mortality['sex'] == 'Total']
    .filter(['alpha_3_code', 'time_period', 'obs_value'])
    .rename(columns={
        'alpha_3_code': 'country_code',
        'time_period': 'year',
        'obs_value': 'mortality_rate'
    })
)

# Convert to numeric
mortality_clean['mortality_rate'] = pd.to_numeric(
    mortality_clean['mortality_rate'],
    errors='coerce'
)

print("Cleaned Mortality Data:")
print(mortality_clean.head())


# 1. Load and clean coverage data (from previous success)
coverage = pd.read_csv('cleaned_unicef_indicator_1.csv')
coverage_clean = coverage[['alpha_3_code', 'year', 'vitamin_a_coverage']]
coverage_clean.columns = ['country_code', 'year', 'coverage']

# 2. Load metadata
meta = pd.read_csv('unicef_metadata.csv')
meta_clean = meta[['alpha_3_code', 'population', 'GDP_per_capita']]
meta_clean.columns = ['country_code', 'population', 'gdp_per_capita']

# 3. Merge all datasets
final_df = (
    coverage_clean
    .merge(mortality_clean, on=['country_code', 'year'], how='left')
    .merge(meta_clean, on='country_code', how='left')
)

# 4. Final cleaning
final_df['gdp_per_capita'] = (
    final_df['gdp_per_capita']
    .astype(str)
    .str.replace(',', '')
    .str.replace('$', '')
    .astype(float)
)

# 5. Create analysis columns
final_df['mortality_per_100k'] = final_df['mortality_rate'] * 100
final_df['coverage_status'] = np.where(final_df['coverage'] >= 80, 'Adequate', 'Inadequate')
final_df['gdp_category'] = pd.cut(
    final_df['gdp_per_capita'],
    bins=[0, 1000, 4000, 12000, np.inf],
    labels=['Low', 'Lower-Middle', 'Upper-Middle', 'High']
)

print("\nFinal Dataset Sample:")
print(final_df.head())

# Merge all datasets with error handling
try:
    final_df = (
        coverage_clean
        .merge(mortality_clean, on=['country_code', 'year'], how='left')
        .merge(meta_clean, on='country_code', how='left')
    )
except KeyError as e:
    print(f"Merge failed: {str(e)}")
    print("Available columns in each dataset:")
    print("Coverage:", coverage_clean.columns.tolist())
    print("Mortality:", mortality_clean.columns.tolist())
    print("Metadata:", meta_clean.columns.tolist())
else:
    print("\nSuccessfully merged data:")
    print(final_df.head())
