from django.contrib import admin  # Importing Django's admin module
from django.urls import path, include  # Importing path and include functions from Django's URL library
from gis_app import views  # Importing views from gis_app module
from gis_app.views import protected_data_view  # Importing protected_data_view from gis_app.views
from django.contrib.auth import views as auth_views  # Importing views from Django's authentication module

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for Django admin site

    # Commented out: URL pattern for map view from gis_app.views
    # path('map/', views.map_view, name='map-view'),

    path('api/', include("gis_app.urls")),  # Including API endpoints from gis_app.urls using router

    path('fetch-protected-data/', protected_data_view, name='fetch_protected_data'),  # URL pattern for fetching protected data

    path('auth/', include('rest_framework.urls')),  # URL patterns for authentication views provided by Django REST Framework

    path('accounts/profile/', views.profile_view, name='profile'),  # URL pattern for profile view

    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # URL pattern for login view with custom template
]
