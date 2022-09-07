from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import City
from .service import WeatherService
from .forms import CitySearchForm, UserRegisterForm, UserLoginForm


def index(request):
    context = WeatherService.get_weather_context('')
    context['form'] = CitySearchForm()

    if request.method == 'POST':
        form = CitySearchForm(request.POST)
        if 'city_name' in request.POST and form.is_valid():
            context.update(WeatherService.get_weather_context(form.cleaned_data['city_name']))
            context['form'] = form

    cities = City.objects.filter(users=request.user.id)
    context['cities'] = []

    for city in cities:
        context['cities'].append(WeatherService.get_weather_context(city.title))

    return render(request, 'weather/index.html', context)


def add_city(request):
    if 'city_title' in request.POST:
        city = City(title=request.POST['city_title'])
        city.save()
        city.users.add(request.user.id)
    return redirect('home')


def remove_city(request):
    if 'city_remove' in request.POST:
        city = City.objects.filter(title=request.POST['city_remove'])
        city.delete()
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return redirect('login')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegisterForm()
    return render(request, 'weather/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'weather/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
