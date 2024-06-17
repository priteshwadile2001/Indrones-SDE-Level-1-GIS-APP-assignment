# Import necessary modules and functions from Django and Django REST Framework
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.contrib.gis.geos import Point  # Importing Point from Django GIS
from gis_app.models import Location, Boundary  # Importing models Location and Boundary from gis_app
from gis_app.seriliazers import LocationSerializer, BoundarySerializer  # Importing serializers for Location and Boundary
from rest_framework.views import APIView  # Importing APIView from Django REST Framework
from django.http import Http404  # Importing Http404 exception from Django HTTP
from geopy.distance import geodesic  # Importing geodesic function from geopy.distance
from django.contrib.auth.decorators import login_required  # Importing login_required decorator from Django auth
from rest_framework.permissions import IsAuthenticated  # Importing IsAuthenticated permission class from DRF


# Define a class-based view with APIView for a protected endpoint
class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Specify that authentication is required
    
    def get(self, request):
        return Response({"message": "This is a protected view"})  # Return a simple JSON response

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

# API endpoint for detailed operations on Location model

@api_view(['GET', 'DELETE'])
def LocationDetailAPIView(request, pk):
    try:
        location = Location.objects.get(pk=pk)  # Retrieve Location by primary key
    except Location.DoesNotExist:
        return Response({"detail": "Location not found."}, status=status.HTTP_404_NOT_FOUND)  # Return 404 if not found

    if request.method == 'GET':
        serializer = LocationSerializer(location)  # Serialize Location data
        return Response(serializer.data)

    elif request.method == 'DELETE':
        location.delete()  # Delete Location
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Detail API view for Boundary model
class BoundaryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure authentication is required for this view

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


# View for rendering the map.html template
def map_view(request):
    boundaries = Boundary.objects.all()
    locations = Location.objects.all()
    context = {
        'boundary_data': boundaries,
        'locations': locations,
    }
    return render(request, 'map.html', context)

# API view to check if a location is within any boundary
class CheckLocationView(APIView):
    def post(self, request, *args, **kwargs):
        lat = request.data.get('latitude')  # Get latitude from request data
        lng = request.data.get('longitude')  # Get longitude from request data

        if lat is None or lng is None:
            return Response({"error": "Latitude and longitude are required."}, status=400)  # Return 400 if coordinates are missing

        point = Point(float(lng), float(lat))  # Create Point object with given coordinates

        boundaries = Boundary.objects.all()  # Query all Boundary objects
        for boundary in boundaries:
            if boundary.area.contains(point):  # Check if Point is within Boundary
                return Response({"within_boundary": True, "boundary_id": boundary.id, "boundary_name": boundary.name})  # Return success response

        return Response({"within_boundary": False})  # Return response if Point is not within any Boundary

# API view to check if a boundary contains a specific location
class CheckBoundaryView(APIView):
    def post(self, request, *args, **kwargs):
        boundary_id = request.data.get('boundary_id')
        location_id = request.data.get('location_id')

        if not boundary_id or not location_id:
            return Response({"error": "Boundary ID and location ID are required."}, status=400)

        try:
            boundary = Boundary.objects.get(id=boundary_id)
        except Boundary.DoesNotExist:
            return Response({"error": "Boundary does not exist."}, status=404)

        try:
            location = Location.objects.get(id=location_id)
            latitude = location.latitude
            longitude = location.longitude
            
        except Location.DoesNotExist:
            return Response({"error": "Location does not exist."}, status=404)

        # Create the point from location's coordinates
        point = Point(longitude, latitude)  # Correct order: longitude, latitude

        # Check if the point is within the boundary
        if boundary.area.contains(point):
            return Response({"within_boundary": True, "boundary_name": boundary.name})
        else:
            return Response({"within_boundary": False})
