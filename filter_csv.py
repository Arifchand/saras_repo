import pandas as pd

# Load the CSV file
df = pd.read_csv('instrument_data_filtered.csv')

# Filter the DataFrame
filtered_df = df[df['symbol'].str.endswith('-EQ')]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_file.csv', index=False)
