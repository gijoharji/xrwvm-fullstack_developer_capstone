from django.views.generic import TemplateView  # Add this line for TemplateView
from django.urls import path  # Import path to define URL patterns
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Import the views from the current app

app_name = 'djangoapp'  # Namespace for the app

urlpatterns = [
    # Path for login
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registration, name='register'),
    
    # Path for fetching cars
    path('get_cars/', views.get_cars, name='getcars'),

    # Path for fetching dealerships
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),

    # Other paths
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('get_reviews/<int:dealer_id>/', views.get_dealer_reviews, name='get_reviews'),
    path('add_review/', views.add_review, name='add_review'),  # New route for adding reviews
    
    # Route for rendering the React page for dealer details and reviews
    path('dealer/<int:id>/', TemplateView.as_view(template_name="index.html")),  
    
    # Route for rendering the React page for posting a review
    path('postreview/<int:id>/', TemplateView.as_view(template_name="index.html")),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
