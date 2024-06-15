from rest_framework.views import exception_handler  # Importing exception_handler from Django REST Framework views
from rest_framework.exceptions import AuthenticationFailed  # Importing AuthenticationFailed exception from DRF
from rest_framework.response import Response  # Importing Response class from DRF
import csv  # Importing CSV module for CSV file operations
from io import TextIOWrapper  # Importing TextIOWrapper from io module for file decoding
from django.contrib.gis.geos import Point  # Importing Point from Django GIS
from .models import Location  # Importing Location model from current directory's models module

# Custom exception handler for handling specific exceptions
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # Default exception handler from DRF
    
    if isinstance(exc, AuthenticationFailed) and 'Session expired' in str(exc):
        # Handling AuthenticationFailed exception with specific message
        response_data = {
            'error': 'Session expired',
            'message': 'Your session has expired. Please refresh the page to continue.'
        }
        return Response(response_data, status=401)  # Returning customized response with status code 401
    
    return response  # Returning default response if no custom handling is required

# Function to process uploaded CSV file
def process_csv_file(file):
    success_count = 0  # Counter for successful imports
    error_count = 0  # Counter for errors encountered
    
    # Decode the uploaded file if it's bytes
    if isinstance(file, bytes):
        file = TextIOWrapper(file, encoding='utf-8')  # Decode bytes into TextIOWrapper
    
    try:
        csv_reader = csv.reader(file)  # Initialize CSV reader
        next(csv_reader)  # Skip header row
        
        for row in csv_reader:
            if len(row) != 4:  # Checking if each row has expected number of columns
                error_count += 1
                continue  # Skip processing this row
            
            # Extracting data from CSV row
            name = row[0].strip()  # Name of the location
            description = row[1].strip()  # Description of the location
            latitude = float(row[2].strip())  # Latitude of the location
            longitude = float(row[3].strip())  # Longitude of the location
            
            # Creating a Point object from latitude and longitude
            coordinates = Point(longitude, latitude)
            
            # Creating or updating Location object in the database
            location, created = Location.objects.update_or_create(
                name=name,
                defaults={
                    'description': description,
                    'coordinates': coordinates
                }
            )
            
            if created:
                success_count += 1  # Incrementing success count for new imports
            
            # Handle the case where you might want to update existing records
            # You can add code here to handle updates if needed
        
        return success_count, error_count  # Returning counts of successful imports and errors
    
    except Exception as e:
        raise e  # Re-raising any exceptions encountered during processing
