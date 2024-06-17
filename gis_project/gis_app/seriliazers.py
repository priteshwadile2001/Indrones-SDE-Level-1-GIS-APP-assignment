
from rest_framework import serializers
from django.contrib.gis.geos import Point, Polygon
from .models import Location, Boundary
class LocationSerializer(serializers.ModelSerializer):
    coordinates = serializers.ListField(child=serializers.FloatField())
    class Meta:
        model = Location
        fields = "__all__"

    # def create(self, validated_data):
    #     coordinates_data = validated_data.pop('coordinates')
    #     # Create a Point object from the coordinates
    #     point = Point(coordinates_data[0], coordinates_data[1])
    #     validated_data['coordinates'] = point
    #     print(validated_data,"****************")
    #     instance = super().create(validated_data)
    #     return instance

class BoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Boundary
        fields = '__all__'

    # def create(self, validated_data):
    #     area_str = validated_data.pop('area')
    #     # Assuming the area is provided as a WKT string
    #     area = Polygon.from_ewkt(area_str)
    #     validated_data['area'] = area
    #     return super().create(validated_data)
