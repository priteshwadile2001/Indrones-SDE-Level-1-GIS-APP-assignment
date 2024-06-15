# Import necessary modules and functions from Django and Django REST Framework
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point  # Importing Point from Django GIS
from gis_app.models import Location, Boundary  # Importing models Location and Boundary from gis_app
from gis_app.seriliazers import LocationSerializer, BoundarySerializer  # Importing serializers for Location and Boundary
from rest_framework.views import APIView  # Importing APIView from Django REST Framework
from django.http import Http404  # Importing Http404 exception from Django HTTP
from .utils import process_csv_file  # Importing function process_csv_file from local module
from django.http import JsonResponse  # Importing JsonResponse from Django HTTP
from django.contrib.gis.geos import Point  # Importing Point again from Django GIS
from geopy.distance import geodesic  # Importing geodesic function from geopy.distance
from django.contrib.auth.decorators import login_required  # Importing login_required decorator from Django auth
from rest_framework.permissions import IsAuthenticated  # Importing IsAuthenticated permission class from DRF

# Define a class-based view with APIView for a protected endpoint
class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Specify that authentication is required

    def get(self, request):
        return Response({"message": "This is a protected view"})  # Return a simple JSON response

# Define a function-based view requiring login for accessing protected_data.html
def protected_data_view(request):
    return render(request, 'protected_data.html')  # Render protected_data.html template

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

# Define an API endpoint for calculating distance between two locations
@api_view(['GET'])
def calculate_distance(request):
    location1_id = request.query_params.get('location1_id')  # Get location1_id from query parameters
    location2_id = request.query_params.get('location2_id')  # Get location2_id from query parameters

    if not location1_id or not location2_id:
        return Response({"detail": "Both location1_id and location2_id are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        location1 = get_object_or_404(Location, pk=location1_id)  # Retrieve Location object with location1_id
        location2 = get_object_or_404(Location, pk=location2_id)  # Retrieve Location object with location2_id

        if not isinstance(location1.coordinates, Point) or not isinstance(location2.coordinates, Point):
            return Response({"detail": "Invalid coordinates for one or both locations."}, status=status.HTTP_400_BAD_REQUEST)

        lat1, lon1 = location1.coordinates.y, location1.coordinates.x  # Extract latitude and longitude from Point objects
        lat2, lon2 = location2.coordinates.y, location2.coordinates.x  # Extract latitude and longitude from Point objects

        if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
            return Response({"detail": "Latitude values must be within -90 to 90 degrees."}, status=status.HTTP_400_BAD_REQUEST)

        distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers  # Calculate distance using geopy

        return Response({'distance': distance}, status=status.HTTP_200_OK)  # Return distance in kilometers

    except Location.DoesNotExist:
        return Response({"detail": "One or both locations not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": "An error occurred while calculating distance."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API endpoint to check if a location is within a boundary
@api_view(['GET'])
def check_boundary(request):
    point_id = request.GET.get('point_id')  # Get point_id from query parameters
    boundary_id = request.GET.get('boundary_id')  # Get boundary_id from query parameters
    point = Location.objects.get(id=point_id)  # Retrieve Location object with point_id
    boundary = Boundary.objects.get(id=boundary_id)  # Retrieve Boundary object with boundary_id

    is_within_boundary = False
    boundaries = Boundary.objects.all()  # Query all Boundary objects

    for boundary in boundaries:
        if point.coordinates.within(boundary.area):  # Check if point is within boundary's area
            is_within_boundary = True
            break

    response_data = {
        'is_within_boundary': is_within_boundary,
    }
    return JsonResponse(response_data)  # Return JSON response indicating if point is within boundary

# APIView for detailed operations on Boundary model
class BoundaryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Boundary.objects.get(pk=pk)  # Get Boundary object by primary key
        except Boundary.DoesNotExist:
            raise Http404  # Raise Http404 if Boundary does not exist

    def put(self, request, pk, format=None):
        boundary = self.get_object(pk)  # Retrieve Boundary object
        serializer = BoundarySerializer(boundary, data=request.data)  # Initialize serializer with Boundary data
        if serializer.is_valid():
            serializer.save()  # Save serializer data
            return Response(serializer.data)  # Return serialized data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if serializer is not valid

    def patch(self, request, pk, format=None):
        boundary = self.get_object(pk)  # Retrieve Boundary object
        serializer = BoundarySerializer(boundary, data=request.data, partial=True)  # Initialize serializer with partial data
        if serializer.is_valid():
            serializer.save()  # Save serializer data
            return Response(serializer.data)  # Return serialized data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if serializer is not valid

# Function-based view to list locations and boundaries
def location_list(request):
    locations = Location.objects.all()  # Query all Location objects
    boundaries = Boundary.objects.all()  # Query all Boundary objects
    return render(request, 'index.html', {'locations': locations, 'boundaries': boundaries})  # Render index.html with locations and boundaries

# Function-based view to render map using Leaflet.js
def map_view(request):
    locations = Location.objects.all()  # Query all Location objects
    boundary = Boundary.objects.all()  # Query all Boundary objects
    locations_data = [location.to_dict() for location in locations]  # Convert Location objects to dictionary format
    Boundary_data = [Boundary.to_dict() for Boundary in boundary]  # Convert Boundary objects to dictionary format
    return render(request, 'map.html', {'locations': locations_data, 'Boundary_data': Boundary_data})  # Render map.html with locations and boundaries data

# API endpoint to import locations from CSV
@api_view(['POST'])
def import_locations_from_csv(request):
    file = request.FILES.get('file')  # Get uploaded file from request
    if not file:
        return Response({"detail": "No file uploaded."}, status=400)  # Return error if no file uploaded

    try:
        success_count, error_count = process_csv_file(file)  # Process uploaded CSV file
        return Response({
            "detail": f"Imported {success_count} locations. {error_count} errors occurred."  # Return success message
        }, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)  # Return error message if exception occurs

# APIView for listing boundaries with authentication required
class BoundaryListView(APIView):
    permission_classes = [IsAuthenticated]  # Specify that authentication is required

    def get(self, request):
        boundaries = Boundary.objects.all()  # Query all Boundary objects
        return Response({"boundaries": list(boundaries.values())}, status=status.HTTP_200_OK)  # Return serialized boundaries
