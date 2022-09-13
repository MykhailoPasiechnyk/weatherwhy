from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import City
from .service import WeatherService
from .forms import CitySearchForm, UserRegisterForm, UserLoginForm
from .exceptions import TitleCityException


def index(request):
    context = {'form': CitySearchForm()}

    cities = City.objects.filter(users=request.user.id)
    context['cities'] = []

    for city in cities:
        context['cities'].append(WeatherService.get_weather_context(city.title))

    return render(request, 'weather/index.html', context)


@require_http_methods(['GET', 'POST'])
def search(request):
    context = {'form': CitySearchForm()}
    if request.method == 'POST':
        form = CitySearchForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                context.update(WeatherService.get_weather_context(form.cleaned_data['city_name']))
            except TitleCityException:
                messages.error(request, f"Failed name: {form.cleaned_data['city_name']}, try another city name ")

    return render(request, 'weather/search.html', context)


@login_required(login_url='/login')
def add_city(request):
    if 'city_title' in request.POST:
        city_title = request.POST['city_title']
        find_city = City.objects.filter(title=city_title)
        if not find_city:
            city = City(title=city_title)
            city.save()
            city.users.add(request.user.id)
        elif request.user not in find_city[0].users.all():
            find_city[0].users.add(request.user.id)
        else:
            messages.success(request, f"You already have: {city_title} in your city list.")
    return redirect('home')


@login_required(login_url='/login')
def remove_city(request):
    if 'city_remove' in request.POST:
        city = City.objects.filter(title=request.POST['city_remove'])
        city[0].users.remove(request.user.id)
        if not city[0].users:
            city.delete()
    return redirect('home')


@require_http_methods(['GET', 'POST'])
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


@require_http_methods(['GET', 'POST'])
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
