from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Polygon
from gis_app.models import Boundary
import csv

class Command(BaseCommand):
    help = 'Import locations data from CSV file'

    def handle(self, *args, **options):
        csv_file = r'C:\Test\projects\New folder\gis_project\cleaned_location.csv'

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Example coordinates for a square around the given point
                    latitude = float(row['latitude'])
                    longitude = float(row['longitude'])

                    # Create a square around the point for demonstration purposes
                    area_coords = [
                        (latitude, longitude),
                        (latitude  + 0.01, longitude),
                        ( latitude+ 0.01,  longitude + 0.01),
                        ( latitude,longitude + 0.01),
                        ( latitude,longitude)  # Closing the polygon
                    ]
                    
                    polygon = Polygon(area_coords, srid=4326)

                    # Create Boundary object with Polygon geometry
                    Boundary.objects.create(name=row['name'], area=polygon)

                    self.stdout.write(self.style.SUCCESS(f'Successfully created Boundary: {row["name"]}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating Boundary: {row["name"]} - {e}'))
