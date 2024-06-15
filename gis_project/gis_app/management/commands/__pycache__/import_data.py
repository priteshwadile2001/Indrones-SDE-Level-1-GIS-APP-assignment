# import_data.py

import csv
from django.contrib.gis.geos import Point
from gis_app.models import Location  # Adjust as per your Django app structure
# gis_app/management/commands/import_data.py

from django.core.management.base import BaseCommand
from gis_app.models import Location  # Import your models

def import_data_from_csv():
    with open(r'C:\Test\projects\New folder\gis_project\location_update.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            name = row[0]
            description = row[1]
            latitude = float(row[2])
            longitude = float(row[3])
            
            # Create a Point object for coordinates
            coordinates = Point(longitude, latitude)

            # Create Location instance and save to database
            obj = Location(name=name, description=description, coordinates=coordinates)
            obj.save()

if __name__ == '__main__':
    import_data_from_csv()


class Command(BaseCommand):
    help = 'Imports data from CSV file'

    def handle(self, *args, **options):
        # Your logic to import data from CSV or perform other tasks
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
