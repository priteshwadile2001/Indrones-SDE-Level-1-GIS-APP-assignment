from django.urls import path, include  # Importing path and include functions from Django's URL library
from rest_framework.routers import DefaultRouter  # Importing DefaultRouter from Django REST Framework
from gis_app.views import (  # Importing views from gis_app.views module
    LocationViewSet, BoundaryViewSet, 
    calculate_distance,CheckBoundaryView,
)
from . import views  # Importing views from the current directory (assuming views.py is in the same directory)
from django.contrib.auth import views as auth_views  # Importing views from Django's authentication module

router = DefaultRouter()  # Creating a DefaultRouter instance
router.register(r'locations', LocationViewSet)  # Registering LocationViewSet with router
router.register(r'boundaries', BoundaryViewSet)  # Registering BoundaryViewSet with router

urlpatterns = [
    path('', include(router.urls)),  # Including router URLs (automatically includes URLs for 'locations' and 'boundaries')
    path('check-boundary/', CheckBoundaryView.as_view(), name='check-boundary'),
    path('map/', views.map_view, name='map-view'),  # URL pattern for map view
    path('calculate_distance/', calculate_distance, name='calculate_distance'),  # URL pattern for calculate_distance API endpoint
    path('auth/', include('rest_framework.urls')),  # URL patterns for authentication views provided by Django REST Framework
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # URL pattern for login view with custom template
    path('accounts/profile/', views.profile_view, name='profile'),  # URL pattern for profile view
   
]
