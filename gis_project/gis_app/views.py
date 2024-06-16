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
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Define a class-based view with APIView for a protected endpoint
class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Specify that authentication is required

    def get(self, request):
        return Response({"message": "This is a protected view"})  # Return a simple JSON response

# Define a function-based view requiring login for accessing protected_data.html
def protected_data_view(request):
    return render(request, 'protected_data.html')  # Render protected_data.html template

# Define a function-based view requiring login for accessing profile.html
# @login_required
# def profile_view(request):
#     return render(request, 'profile.html')  # Render profile.html template

# Define a ViewSet for handling Location model operations
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()  # Query all Location objects
    serializer_class = LocationSerializer  # Use LocationSerializer for serialization

# Define a ViewSet for handling Boundary model operations
class BoundaryViewSet(viewsets.ModelViewSet):
    queryset = Boundary.objects.all()  # Query all Boundary objects
    serializer_class = BoundarySerializer  # Use BoundarySerializer for serialization

# API endpoint for detailed operations on Location model
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
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
    coord2 = (location2.coordinates.y, location2.coordinates.x)  # Extract coordinates of second Location
    distance = geodesic(coord1, coord2).kilometers  # Calculate distance using geopy

    return Response({'distance': distance}, status=status.HTTP_200_OK)  # Return distance in response

# Custom authentication token view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})  # Validate request data
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)  # Get or create authentication token
        return Response({'token': token.key})  # Return token in response

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

# Function-based view to render map using Leaflet.js
# def map_view(request):
#     locations = Location.objects.all()  # Query all Location objects
#     boundary = Boundary.objects.all()  # Query all Boundary objects
#     locations_data = [location.to_dict() for location in locations]  # Convert Location objects to dictionary format
#     boundary_data = [boundary.to_dict() for boundary in boundary]  # Convert Boundary objects to dictionary format
#     return render(request, 'map.html', {'locations': locations_data, 'boundary_data': boundary_data})  # Render map.html with locations and boundaries data

def map_view(request):
    boundaries = Boundary.objects.all()
    locations = Location.objects.all()
    context = {
        'Boundary_data': boundaries,
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
