from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .utilities import WeatherCaller
import json

class defaultView(TemplateView):
    template_name = 'weather/default.html'

# Create your views here.
@csrf_exempt
def WebtherView(request, latitude=None, longitude=None):
    weather_templates = {
        'thunderstorm': 'weather/thunderstorm.html',
        'drizzle': 'weather/drizzle.html',
        'rain': 'weather/rain.html',
        'snow': 'weather/snow.html',
        'atmosphere': 'weather/atmosphere.html',
        'clear': 'weather/clear.html',
        'clouds': 'weather/clouds.html',
        'sunny': 'weather/sun.html',  # unused template so far
    }
    template_name = ""

    # If latitude and longitude are not provided in the URL parameters,
    # try to get them from the request body (POST request)
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        print(latitude, longitude)

        # Process the latitude and longitude as needed
        # For example, you can save them to a database or perform other actions
        #geoLoc = process_geolocation(latitude, longitude)

    weather_util = WeatherCaller()
    base_url = weather_util.get_url()
    raw_data = weather_util.get_weather_data_raw(base_url)
    context = weather_util.data_raw_to_webther_format(raw_data)
    print(context)

    # conditional template switch logic
    if context['current_weather_status'] == "Thunderstorm":
        template_name = weather_templates['thunderstorm']
    elif context['current_weather_status'] == "Drizzle":
        template_name = weather_templates['drizzle']
    elif context['current_weather_status'] == "Rain":
        template_name = weather_templates['rain']
    elif context['current_weather_status'] == "Snow":
        template_name = weather_templates['snow']
    elif context['current_weather_status'] == "Atmosphere":
        template_name = weather_templates['atmosphere']
    elif context['current_weather_status'] == "Clear":
        template_name = weather_templates['clear']
    elif context['current_weather_status'] == "Clouds":
        template_name = weather_templates['clouds']
    elif context['current_weather_status'] == "Sun":
        template_name = weather_templates['sunny']

    return render(request, template_name, context)

#def WebtherView(TemplateView): #TODOO: implement api call and showing data in view

@csrf_exempt
def handle_geolocation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Process the latitude and longitude as needed
        # For example, you can save them to a database or perform other actions
        # print(request.method, latitude, longitude)
        variable = process_geolocation(latitude, longitude)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def process_geolocation(latitude, longitude):
    # Access latitude and longitude in this function
    # Process the data as needed
    print(f"Received latitude: {latitude} & longitude: {longitude}")
    geoCoordinates = {"latitude": latitude, "longitude": longitude}
    return geoCoordinates

