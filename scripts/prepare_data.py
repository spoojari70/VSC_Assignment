import pandas as pd

# Load
coverage = pd.read_csv('data/unicef_indicator_1_cleaned.csv')
mortality = pd.read_csv('data/unicef_indicator_2_cleaned.csv')
metadata = pd.read_csv('data/unicef_metadata_cleaned.csv')

# Rename columns to unify merge keys
coverage = coverage.rename(columns={
    'alpha_3_code': 'country_code',
    'time_period': 'year',
    'obs_value': 'coverage'
})

mortality = mortality.rename(columns={
    'alpha_3_code': 'country_code',
    'time_period': 'year',
    'obs_value': 'mortality'
})

metadata = metadata.rename(columns={
    'alpha_3_code': 'country_code'
})

# Merge
data = pd.merge(coverage, mortality, on=['country_code', 'year'], how='inner')
data = pd.merge(data, metadata, on='country_code', how='left')

# Save merged dataset
data.to_csv('data/unicef_merged.csv', index=False)
print("✅ Data merged and saved successfully!")
