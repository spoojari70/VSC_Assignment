# Data Cleaning Pipeline
import pandas as pd
import numpy as np

# Load datasets with error handling
coverage = pd.read_csv('unicef_indicator_1.csv', encoding='latin1')
mortality = pd.read_csv('unicef_indicator_2.csv', encoding='latin1')
metadata = pd.read_csv('unicef_metadata.csv', encoding='latin1')

# =============================================================================
# 1. Coverage Data Cleaning (Vitamin A)
# =============================================================================

# Filter relevant columns
coverage_clean = coverage[['alpha_3_code', 'time_period', 'obs_value']].copy()
coverage_clean.columns = ['country_code', 'year', 'coverage']

# Convert year to numeric
coverage_clean['year'] = pd.to_numeric(coverage_clean['year'], errors='coerce')

# Handle missing values
coverage_clean['coverage'] = coverage_clean['coverage'].replace({'NAN': np.nan, 'NA': np.nan})
coverage_clean['coverage'] = coverage_clean['coverage'].astype(float)

# Remove years without coverage data
coverage_clean = coverage_clean.dropna(subset=['coverage'])

# =============================================================================
# 2. Mortality Data Cleaning (Ages 15-19)
# =============================================================================
mortality_clean = mortality[mortality['sex'] == 'Total'].copy()
mortality_clean = mortality_clean[['alpha_3_code', 'time_period', 'obs_value']]
mortality_clean.columns = ['country_code', 'year', 'mortality_rate']

# Convert to numeric
mortality_clean['year'] = pd.to_numeric(mortality_clean['year'], errors='coerce')
mortality_clean['mortality_rate'] = pd.to_numeric(mortality_clean['mortality_rate'], errors='coerce')

# =============================================================================
# 3. Metadata Cleaning
# =============================================================================
meta_clean = metadata[['alpha_3_code', 'Population', 'GDP Per Capita (USD)']].copy()
meta_clean.columns = ['country_code', 'population', 'gdp_per_capita']

# Convert GDP to float and handle missing values
meta_clean['gdp_per_capita'] = (
    meta_clean['gdp_per_capita']
    .replace({',': '', '\$': ''}, regex=True)
    .astype(float)
)

# =============================================================================
# 4. Merge Datasets
# =============================================================================
# Inner merge coverage and mortality
merged = pd.merge(
    coverage_clean,
    mortality_clean,
    on=['country_code', 'year'],
    how='inner'
)

# Left merge with metadata
final_df = pd.merge(
    merged,
    meta_clean,
    on='country_code',
    how='left'
)

# Final cleaning
final_df = final_df.dropna(subset=['mortality_rate'])
final_df['year'] = final_df['year'].astype(int)
final_df['coverage'] = final_df['coverage'].clip(0, 100)  # Ensure 0-100% range

# Add decade column for temporal analysis
final_df['decade'] = (final_df['year'] // 10) * 10

# =============================================================================
# 5. Feature Engineering
# =============================================================================
# Mortality rate per 100,000 population
final_df['mortality_per_100k'] = final_df['mortality_rate'] * 100

# GDP categories
final_df['gdp_category'] = pd.cut(
    final_df['gdp_per_capita'],
    bins=[0, 1000, 4000, 12000, np.inf],
    labels=['Low', 'Lower-Middle', 'Upper-Middle', 'High']
)

# Coverage adequacy
final_df['coverage_status'] = np.where(
    final_df['coverage'] >= 80, 
    'Adequate (≥80%)', 
    'Inadequate (<80%)'
)

# Save cleaned data
final_df.to_csv('unicef_cleaned_data.csv', index=False)
