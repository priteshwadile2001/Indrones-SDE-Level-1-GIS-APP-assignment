from django.urls import path, include  # Importing path and include functions from Django's URL library
from rest_framework.routers import DefaultRouter  # Importing DefaultRouter from Django REST Framework
from gis_app.views import (  # Importing views from gis_app.views module
    LocationViewSet, BoundaryViewSet, BoundaryDetailAPIView,
    calculate_distance, check_boundary
)
from . import views  # Importing views from the current directory (assuming views.py is in the same directory)
from .views import MyProtectedView, protected_data_view  # Importing specific views from the current directory's views module
from django.contrib.auth import views as auth_views  # Importing views from Django's authentication module

from rest_framework_simplejwt.views import (  # Importing views from Simple JWT for token-based authentication
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()  # Creating a DefaultRouter instance
router.register(r'locations', LocationViewSet)  # Registering LocationViewSet with router
router.register(r'boundaries', BoundaryViewSet)  # Registering BoundaryViewSet with router

urlpatterns = [
    path('', include(router.urls)),  # Including router URLs (automatically includes URLs for 'locations' and 'boundaries')
    path('locations/', views.location_list, name='location-list'),  # URL pattern for listing locations
    path('map/', views.map_view, name='map-view'),  # URL pattern for map view
    path('calculate_distance/', calculate_distance, name='calculate_distance'),  # URL pattern for calculate_distance API endpoint
    path('check_boundary/', check_boundary, name='check_boundary'),  # URL pattern for check_boundary API endpoint
    path('boundary/', BoundaryDetailAPIView.as_view(), name='boundary-detail'),  # URL pattern for BoundaryDetailAPIView
    path('protected/', MyProtectedView.as_view(), name='my_protected_view'),  # URL pattern for MyProtectedView
    path('import_locations_from_csv/', views.import_locations_from_csv, name='import-locations-from-csv'),  # URL pattern for importing locations from CSV
    path('auth/', include('rest_framework.urls')),  # URL patterns for authentication views provided by Django REST Framework
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # URL pattern for login view with custom template
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL pattern for logout view
    # path('fetch-protected-data/', protected_data_view, name='fetch_protected_data'),  # URL pattern for fetching protected data (commented out)
    path('accounts/profile/', views.profile_view, name='profile'),  # URL pattern for profile view
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # URL pattern for obtaining JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # URL pattern for refreshing JWT token
]
