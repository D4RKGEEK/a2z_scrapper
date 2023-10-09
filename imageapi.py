import random
from serpapi import GoogleSearch
import requests
import json

serp_api_keys = [
    "5e7b7e031602e71f653032d95e29851cbfe6358dfb8c6154936b898dc1a4c94d",
    "6f77c33ebc9e4ef90876ead24dd7524c6d46381600d74fa3428a234528b19a1f"
]

search_params = {
    "engine": "google",
    "location": "New Delhi, Delhi, India",
    "google_domain": "google.co.in",
    "gl": "in",
    "hl": "hi",
    "tbm": "isch"
}

def perform_image_search(api_key, query):
    search_params["api_key"] = api_key
    search_params["q"] = query
    try:
        search = GoogleSearch(search_params)
        search_result = search.get_dict()  # This line will trigger the API request
        return search_result
    except Exception as e:
        print(f"Error with API key {api_key}: {e}")
        return None


def search_image(query):
    random.shuffle(serp_api_keys)  # Shuffle the API keys to try them in random order
    search_query = query  # Set your search query here
    excluded_domains = ["modyolo", "i0.wp"]  # List of domains to exclude
    for api_key in serp_api_keys:
        search_result = perform_image_search(api_key, search_query)
        if search_result:
            image_results = search_result.get("images_results", [])
            for first_image in image_results:
                original_image = first_image.get("original")
                thumbnail_image = first_image.get("thumbnail")
                if original_image and not any(domain in original_image for domain in excluded_domains):
                    if is_image_accessible(original_image):
                        return original_image, original_image
                    else:
                        return thumbnail_image, thumbnail_image
            else:
                continue  # Continue to the next API key if no suitable image found


def is_image_accessible(image_url):
    try:
        response = requests.head(image_url)
        return response.status_code == 200
    except requests.RequestException:
        return False

