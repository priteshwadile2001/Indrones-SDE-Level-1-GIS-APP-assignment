import csv

# Your CSV data (replace with your actual data)
csv_data = """name,description,latitude,longitude
Taj Mahal,An ivory-white marble mausoleum in Agra,27.175015,78.042155
Gateway of India,A monument built during the 20th century in Mumbai,18.922000,72.834700
Qutub Minar,A UNESCO World Heritage Site in Delhi,28.524428,77.185455
Hawa Mahal,The Palace of Winds in Jaipur,26.923936,75.826744"""

# Read data and organize into columns
rows = csv_data.strip().split("\n")
header = rows[0].split(",")
data = [dict(zip(header, row.split(","))) for row in rows[1:]]

# Write to a new CSV file
output_file = "update_csv.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

print(f"Data written to {output_file}")
