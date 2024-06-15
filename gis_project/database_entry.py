import pandas as pd
import psycopg2
from datetime import datetime

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(r'C:\Test\projects\New folder\gis_project\cleaned_location.csv')

# Create a new 'coordinates' column by combining latitude and longitude
df['coordinates'] = df.apply(lambda row: f"POINT( {row['latitude']} {row['longitude']})", axis=1)

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='gis',
    user='root',
    password='Wadile123#',
    host='localhost',  # Change to your database host
    port=5432  # Change to your database port
)

# Create a cursor
cur = conn.cursor()

try:
    # Iterate through the DataFrame and insert data
    for index, row in df.iterrows():
        name = row.get('name')
        latitude = row.get('latitude')
        longitude = row.get('longitude')
        description = row.get('description')
        coordinates = row['coordinates']
        current_timestamp = datetime.now()  # Use the current timestamp for created_at and updated_at

        try:
            cur.execute(
                """
                INSERT INTO gis_app_location (name, description, coordinates, created_at, updated_at)
                VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (name, description, coordinates, current_timestamp, current_timestamp)
            )
            print(f"Inserted data for {name}")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error inserting {name}: {e}")

    # Commit changes
    conn.commit()
    print("Insertion successful!")

except psycopg2.Error as e:
    conn.rollback()
    print(f"Error: {e}")

finally:
    cur.close()
    conn.close()
