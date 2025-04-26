import pandas as pd

# File paths (make sure these match your actual file names and locations)
indicator_file = "C:/Users/Acer/OneDrive/Desktop/tableau_assignment/Quarto Report/unicef_indicator_2.csv"
metadata_file = "C:/Users/Acer/OneDrive/Desktop/tableau_assignment/Quarto Report/unicef_metadata.csv"

# Load data
df_ind = pd.read_csv(indicator_file)
df_meta = pd.read_csv(metadata_file)

# Clean indicator data
columns_to_drop = [
    'unit_multiplier',
    'observation_confidentaility',
    'time_period_activity_related_to_when_the_data_are_collected'
]

df_ind_cleaned = df_ind.drop(columns=[col for col in columns_to_drop if col in df_ind.columns])
df_ind_cleaned = df_ind_cleaned.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Clean metadata
df_meta_cleaned = df_meta.dropna(axis=1, how='all')  # Drop empty columns
df_meta_cleaned = df_meta_cleaned.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Save cleaned data
df_ind_cleaned.to_csv("C:/Users/Acer/OneDrive/Desktop/tableau_assignment/Quarto Report/unicef_indicator_2_cleaned.csv", index=False)
df_meta_cleaned.to_csv("C:/Users/Acer/OneDrive/Desktop/tableau_assignment/Quarto Report/unicef_metadata_cleaned.csv", index=False)

print("✅ Cleaning complete. Cleaned files saved.")
