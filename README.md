# Indrones-SDE-Level-1-GIS-APP-assignment

# GIS Project

This Django project implements geographic information system (GIS) functionalities using Django with PostgreSQL and PostGIS.

## Setup and Installation

### Prerequisites

- Python 3.x installed
- PostgreSQL installed (with PostGIS extension enabled)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd gis_project

2.## Create and activate virtual environment:
- python3 -m venv env
- source env/bin/activate   # On Windows use `env\Scripts\activate`

3.##  Install dependencies:
- pip install -r requirements.txt

4.## Set up PostgreSQL database:

- Create a database named gis in PostgreSQL.
- Enable the PostGIS extension in your gis database

5.** Update your DATABASES setting in settings.py:**

      ```bash
      DATABASES = {
          'default': {
              'ENGINE': 'django.contrib.gis.db.backends.postgis',
              'NAME': 'DB_name',
              'USER': 'User',
              'PASSWORD': 'Password',
              'HOST': 'localhost',
              'PORT': '5432',  # Use your actual PostgreSQL port
          }
      }

## Data Import Scripts
 To put the CSV data into the PostgreSQL database, use the following Python scripts:
- organized_csv_data.py: This script organizes the data into column format.
- clean_csv.py: This script cleans the messy data.
- database_entry.py: This script imports boundary data into the database.
- import_locations.py: This script imports location data into the database.
  
6.**Apply migrations**:

      ```bash
      python manage.py makemigrations
      python manage.py migrate

7.**Run the development server**:

        ```bash
        python manage.py createsuperuser
        
8.**Run the development server**:

      ```bash
      python manage.py runserver

Access the development server at http://127.0.0.1:8000/.

9.## API Endpoints
   Locations
   - GET /api/locations/: List all locations.
   - POST /api/locations/: Create a new location.
   - DELETE /api/locations/<id>/: Delete a location.

10.## Boundaries

   - GET /api/boundaries/: List all boundaries.
   - POST /api/boundaries/: Create a new boundary.
   - DELETE /api/boundaries/<id>/: Delete a boundary.
     
