
import csv
from django.core.management.base import BaseCommand
from gis_app.models import Location
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Import locations from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    name = row['name']
                    description = row['description']
                    latitude = float(row['latitude'])
                    longitude = float(row['longitude'])
                    coordinates = Point(latitude,longitude)

                    location, created = Location.objects.get_or_create(
                        name=name,
                        defaults={'description': description, 'coordinates': coordinates},
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added location: {name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Location already exists: {name}'))
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f'Skipping row due to error: {e} - {row}'))
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Skipping row due to missing column: {e} - {row}'))
