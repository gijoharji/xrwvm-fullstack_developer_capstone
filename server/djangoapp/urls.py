# Uncomment the imports before you add the code
from django.urls import path  # Import path to define URL patterns
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Import the views from the current app

app_name = 'djangoapp'  # Namespace for the app

urlpatterns = [
    # Path for login
    path(route='login', view=views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # Uncomment or add additional paths here for registration, reviews, etc.
    path('register/', views.registration, name='register'),
    # path('dealer-reviews/', views.get_dealer_reviews, name='dealer_reviews'),
    # path('add-review/', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
