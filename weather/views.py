from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):

    # try using this URL rather than the one given by the website API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0dbddeed1abbb01c830df7799fe1fd1e'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        req = requests.get(url.format(city)).json()

        weather = {
            'city' : city,
            'temperature' : round(((req['main']['temp'])-32)/1.8,2), # convert to celcius
            'description' : req['weather'][0]['description'],
            'icon' : req['weather'][0]['icon'],
        }

        weather_data.append(weather)

    context = {'weather_data' : weather_data,'form':form}

    return render(request, 'weather/index.html',context)
