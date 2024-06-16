from django.contrib.gis.db import models  # Importing GIS-related models from Django

# Model for storing location data
class Location(models.Model):
    name = models.CharField(max_length=100)  # Name of the location
    description = models.TextField()  # Description of the location
    coordinates = models.PointField()  # PointField for storing coordinates (longitude, latitude)
    created_at = models.DateTimeField(auto_now_add=True)  # DateTimeField for creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # DateTimeField for last update timestamp

    def __str__(self):
        return self.name  # String representation of the Location instance



# Model for storing boundary data
class Boundary(models.Model):
    name = models.CharField(max_length=100)  # Name of the boundary
    area = models.PolygonField()  # PolygonField for storing the boundary area
    created_at = models.DateTimeField(auto_now_add=True)  # DateTimeField for creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # DateTimeField for last update timestamp

    def __str__(self):
        return self.name  # String representation of the Boundary instance
    
  
