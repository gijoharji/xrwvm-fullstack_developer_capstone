from django.urls import path  # Import path to define URL patterns
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Import the views from the current app

app_name = 'djangoapp'  # Namespace for the app

urlpatterns = [
    # Path for login
    path(route='login', view=views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registration, name='register'),
    
    # Path for fetching cars
    path(route='get_cars', view=views.get_cars, name='getcars'),
    
    # Path for fetching dealerships
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # Other paths
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
