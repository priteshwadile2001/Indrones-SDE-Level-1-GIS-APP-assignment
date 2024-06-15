import pandas as pd
from datetime import datetime

# Step 1: Read the CSV file
input_file = r'C:\Test\projects\New folder\gis_project\location_update.csv'
# df = pd.read_csv(input_file,encoding='utf-8')


# Attempt to read the CSV file with 'utf-8' encoding first, if it fails try 'latin1'
try:
    df = pd.read_csv(input_file, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(input_file, encoding='latin1')

# Step 2: Remove duplicate entries
df = df.drop_duplicates()

# Step 3: Handle missing values
# Here, I'll fill missing values with a placeholder. You can adjust this as needed.
df = df.fillna('N/A')

# Step 4: Add 'updated_at' column with the current timestamp
# df['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Step 5: Save the cleaned and transformed data into a new CSV file
output_file = 'cleaned_location.csv'
df.to_csv(output_file, index=False)

print(f"Data cleaned and saved to {output_file}")