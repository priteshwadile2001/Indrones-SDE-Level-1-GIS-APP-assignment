# Import necessary modules and functions from Django and Django REST Framework
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point,polygon  # Importing Point from Django GIS
from gis_app.models import Location, Boundary  # Importing models Location and Boundary from gis_app
from gis_app.seriliazers import LocationSerializer, BoundarySerializer  # Importing serializers for Location and Boundary
from rest_framework.views import APIView  # Importing APIView from Django REST Framework
from django.http import Http404  # Importing Http404 exception from Django HTTP
from geopy.distance import geodesic  # Importing geodesic function from geopy.distance
from django.contrib.auth.decorators import login_required  # Importing login_required decorator from Django auth
from rest_framework.permissions import IsAuthenticated  # Importing IsAuthenticated permission class from DRF


# Define a function-based view requiring login for accessing profile.html
@login_required
def profile_view(request):
    return render(request, 'profile.html')  # Render profile.html template

# Define a ViewSet for handling Location model operations
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()  # Query all Location objects
    serializer_class = LocationSerializer  # Use LocationSerializer for serialization

# Define a ViewSet for handling Boundary model operations
class BoundaryViewSet(viewsets.ModelViewSet):
    queryset = Boundary.objects.all()  # Query all Boundary objects
    serializer_class = BoundarySerializer  # Use BoundarySerializer for serialization
    

class LocationDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)  # Retrieve Location by primary key
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)  # Serialize Location data
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()  # Delete Location
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data)  # Deserialize and validate data
        if serializer.is_valid():
            serializer.save()  # Save updated Location
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data, partial=True)  # Partially update Location
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Detail API view for Boundary model
class BoundaryDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Ensure authentication is required for this view

    def get_object(self, pk):
        try:
            return Boundary.objects.get(pk=pk)  # Retrieve Boundary by primary key
        except Boundary.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        boundary = self.get_object(pk)
        serializer = BoundarySerializer(boundary)  # Serialize Boundary data
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        boundary = self.get_object(pk)
        serializer = BoundarySerializer(boundary, data=request.data)  # Deserialize and validate data
        if serializer.is_valid():
            serializer.save()  # Save updated Boundary
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    def patch(self, request, pk, format=None):
        boundary = self.get_object(pk)
        serializer = BoundarySerializer(boundary, data=request.data, partial=True)  # Partially update Boundary
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    def delete(self, request, pk, format=None):
        boundary = self.get_object(pk)
        boundary.delete()  # Delete Boundary
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return 204 No Content


# Define an API endpoint for calculating distance between two locations
@api_view(['GET'])
def calculate_distance(request):
    location1_id = request.query_params.get('location1_id')  # Get first location ID from query parameters
    location2_id = request.query_params.get('location2_id')  # Get second location ID from query parameters

    if not location1_id or not location2_id:
        return Response({"detail": "Both location1_id and location2_id are required."}, status=status.HTTP_400_BAD_REQUEST)  # Return 400 if IDs are missing

    location1 = get_object_or_404(Location, pk=location1_id)  # Retrieve first Location
    location2 = get_object_or_404(Location, pk=location2_id)  # Retrieve second Location
    print(location1,location2,'&&&&&&&&&&&&&&&&&')

    if not isinstance(location1.coordinates, Point) or not isinstance(location2.coordinates, Point):
        return Response({"detail": "Invalid coordinates for one or both locations."}, status=status.HTTP_400_BAD_REQUEST)  # Return 400 if coordinates are invalid

    # Assuming coordinates are in degrees and using geopy for accurate distance calculation
    coord1 = (location1.coordinates.y, location1.coordinates.x)  # Extract coordinates of first Location
    print(coord1,"coord")
    coord2 = (location2.coordinates.y, location2.coordinates.x)  # Extract coordinates of second Location
    print(coord2,"****")
    distance = geodesic(coord1, coord2).kilometers  # Calculate distance using geopy
    print(distance,'distance')

    return Response({'distance': distance}, status=status.HTTP_200_OK)  # Return distance in response


# Define a view function named map_view that takes a request object as input
def map_view(request):
    # Retrieve all Boundary objects from the database
    boundaries = Boundary.objects.all()
    
    # Retrieve all Location objects from the database
    locations = Location.objects.all()
    
    # Define a context dictionary containing data to be passed to the template
    context = {
        'boundary_data': boundaries,  # Assign the retrieved boundaries to 'boundary_data'
        'locations': locations,        # Assign the retrieved locations to 'locations'
    }
    
    # Render the 'map.html' template with the provided context data
    return render(request, 'map.html', context)


class CheckBoundaryView(APIView):
    def post(self, request, *args, **kwargs):
        boundary_id = request.data.get('boundary_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if not boundary_id or latitude is None or longitude is None:
            return Response({"error": "Boundary ID, latitude, and longitude are required."}, status=400)

        try:
            boundary = Boundary.objects.get(id=boundary_id)
          
        except Boundary.DoesNotExist:
            return Response({"error": "Boundary does not exist."}, status=404)

        # Create the point from provided coordinates
        point = Point(float(longitude), float(latitude))  # Ensure they are floats
       

        # Check if the point is within the boundary
        if boundary.area.contains(point):
            return Response({"within_boundary": True, "boundary_name": boundary.name})
        else:
            return Response({"within_boundary": False})


    
