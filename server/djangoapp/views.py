# Uncomment the required imports before adding the code
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Get the username and password from the request body
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')

        # Try to authenticate the user with the provided credentials
        user = authenticate(username=username, password=password)
        
        # If user is authenticated successfully
        if user is not None:
            # Log the user in
            login(request, user)
            # Return a JSON response with success status
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            # If authentication fails, return a failure message
            return JsonResponse({"userName": username, "status": "Authentication Failed"}, status=401)
    
    # If request method is not POST, return a bad request response
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Additional views can be implemented below...
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_user(request):
    # Check if the user is authenticated before logging out
    if request.user.is_authenticated:
        username = request.user.username  # Get the username of the currently logged-in user
        logout(request)  # Log out the user
        data = {"userName": username}
    else:
        data = {"userName": ""}
    
    # Return a JSON response with the username
    return JsonResponse(data)
#     ...

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # Initialize context and response data
    context = {}

    # Load the data from the request body
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    # Check if username or email already exists
    username_exist = False
    email_exist = False

    try:
        # Check if a user with the same username already exists
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        # Log that this is a new user if the username does not exist
        logger.debug(f"{username} is a new user")

    # If the username does not already exist, proceed with registration
    if not username_exist:
        # Create the new user
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)

        # Log in the new user
        login(request, user)

        # Return a JSON response indicating successful registration and login
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        # If the username already exists, return an error message
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)
# @csrf_exempt
# def registration(request):
#     ...
