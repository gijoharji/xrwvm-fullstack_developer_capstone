from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import get_object_or_404
from django.contrib import messages
from datetime import datetime
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Function to populate the database with CarMake and CarModel data
def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(name=data['name'], description=data['description']))

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "E-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "A4", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(name=data['name'], car_make=data['car_make'], type=data['type'], year=data['year'])

# View to get the list of cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()  # Make sure the initiate function is correctly called
    car_models = CarModel.objects.select_related('car_make')  # Ensure CarMake is related
    cars = []
    for car_model in car_models:
        cars.append({
            "CarMake": car_model.car_make.name,
            "CarModel": car_model.name
        })
    return JsonResponse({"CarModels": cars})

# View to get dealerships
def get_dealerships(request, state="All"):
    if state == "All":
        dealers = Dealer.objects.all()  # Fetch all dealers
    else:
        dealers = Dealer.objects.filter(state=state)  # Filter by state
    
    if dealers.exists():
        dealers_list = list(dealers.values())  # Convert queryset to list of dictionaries
        return JsonResponse({"status": 200, "dealers": dealers_list})
    else:
        return JsonResponse({"status": 200, "dealers": None})  # Return None if no dealers are found

# View to get dealer reviews
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "status": "Authentication Failed"}, status=401)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dealer_id = data.get('dealership')  # Ensure the correct field is fetched
            review_text = data.get('review')
            
            # Add validation for required fields
            if not dealer_id or not review_text:
                return JsonResponse({"status": "error", "message": "Dealer ID and review text are required."}, status=400)
            
            # You can add logic to save the review
            # Example: Review.objects.create(dealer_id=dealer_id, text=review_text)
            
            return JsonResponse({"status": "success", "message": "Review added successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def get_dealer_details(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        # Manually create a dictionary from the dealer object
        dealer_data = {
            'id': dealer.id,
            'full_name': dealer.full_name,
            'address': dealer.address,
            'city': dealer.city,
            'state': dealer.state,
            'zip': dealer.zip,
        }
        return JsonResponse({"status": 200, "dealer": dealer_data})
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"})


def logout_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        return JsonResponse({"userName": username})
    else:
        return JsonResponse({"userName": ""})

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    try:
        User.objects.get(username=username)
        return JsonResponse({"userName": username, "error": "Already Registered"})
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
