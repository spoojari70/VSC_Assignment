import pandas as pd
import numpy as np

# 1. Load data with verification
try:
    coverage = pd.read_csv('cleaned_unicef_indicator_1.csv')
    print("Actual columns:", coverage.columns.tolist())
except FileNotFoundError:
    print("ERROR: File not found. Check filename/path!")
    exit()

# 2. Verify vitamin_a_coverage exists
if 'vitamin_a_coverage' not in coverage.columns:
    print("ERROR: 'vitamin_a_coverage' column missing!")
    print("Actual columns:", coverage.columns.tolist())
    exit()

# 3. Diagnostic print
print("\nFirst 5 vitamin_a_coverage values:")
print(coverage['vitamin_a_coverage'].head().tolist())

# 4. Data Cleaning (if values look valid)
coverage_clean = coverage[['alpha_3_code', 'year', 'vitamin_a_coverage']].copy()
coverage_clean.columns = ['country_code', 'year', 'coverage']

# Convert to numeric
coverage_clean['coverage'] = (
    coverage_clean['coverage']
    .astype(str)
    .str.replace('%', '')
    .str.replace(',', '')
    .replace('NA', np.nan)
    .replace('N/A', np.nan)
    .astype(float)
)

# Final check
print("\nCleaned coverage values:")
print(coverage_clean[['country_code', 'year', 'coverage']].head())



# Load mortality data
mortality = pd.read_csv('unicef_indicator_2.csv')
mortality_clean = mortality[mortality['sex'] == 'Total'][['alpha_3_code', 'year', 'obs_value']]
mortality_clean.columns = ['country_code', 'year', 'mortality_rate']

# Load metadata
meta = pd.read_csv('unicef_metadata.csv')[['alpha_3_code', 'population', 'GDP_per_capita']]
meta.columns = ['country_code', 'population', 'gdp_per_capita']

# Merge all datasets
final_df = (
    coverage_clean
    .merge(mortality_clean, on=['country_code', 'year'], how='left')
    .merge(meta, on='country_code', how='left')
)
