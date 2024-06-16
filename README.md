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
"
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
"
