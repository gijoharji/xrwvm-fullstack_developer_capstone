import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set backend URLs from environment variables or use default values
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# Function to send GET requests to the backend
def get_request(endpoint, **kwargs):
    params = ""
    # Construct URL parameters
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    
    # Combine the backend URL with the endpoint and parameters
    request_url = f"{backend_url}/{endpoint}?{params}"
    print(f"GET from {request_url}")
    
    try:
        # Send GET request and return JSON response
        response = requests.get(request_url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None


# Function to analyze review sentiments using the sentiment analyzer
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}/analyze/{text}"
    print(f"GET from {request_url}")
    
    try:
        response = requests.get(request_url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None

# Function to post a review to the backend
def post_review(data_dict):
    request_url = f"{backend_url}/add-review"
    print(f"POST to {request_url} with data: {data_dict}")
    
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None
