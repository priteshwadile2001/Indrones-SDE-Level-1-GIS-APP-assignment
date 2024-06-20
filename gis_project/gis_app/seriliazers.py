
from rest_framework import serializers
from django.contrib.gis.geos import Point, Polygon
from .models import Location, Boundary

# LocationSerializer 
class LocationSerializer(serializers.ModelSerializer):
    coordinates = serializers.ListField(child=serializers.FloatField())
    class Meta:
        model = Location
        fields = "__all__"

    def create(self, validated_data):
        # validated_Data.pop = Extracts the coordinates data from the validated data dictionary.
        coordinates_data = validated_data.pop('coordinates')
        # Create a Point object from the coordinates logitude and latitude
        point = Point(coordinates_data[0], coordinates_data[1])
        # validated_data['coordinates'] = point: Replaces the list of coordinates with the Point object in the validated data dictionary.
        validated_data['coordinates'] = point
        instance = super().create(validated_data)
        return instance
    

    def update(self, instance, validated_data):
        coordinates_data = validated_data.pop('coordinates', None)  # Extract coordinates if provided

        # Update the instance attributes with the validated data
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)

        if coordinates_data:
            # Update the coordinates field if coordinates_data is provided
            instance.coordinates = Point(coordinates_data[0], coordinates_data[1])

        instance.save()  # Save the instance after updates

        return instance

class BoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Boundary
        fields = '__all__'

    def create(self, validated_data):
        area_str = validated_data.pop('area')
        # Assuming the area is provided as a WKT string
        area = Polygon.from_ewkt(area_str)
        validated_data['area'] = area
        return super().create(validated_data)
