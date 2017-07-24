from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate, login,logout
from .forms import Sign_up ,Login_form ,Location_form
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from django.views.decorators.http import require_http_methods,require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from stateApp.models import Location


def login_user(request):
    form = Login_form(request.POST or None)
    if request.method == "POST":     
        if form.is_valid():
            user = form.check_login()
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else :
                return HttpResponse("Invalid Email and password")
    else :
        form = Login_form()
    return render(request,'stateApp/login.html', {'form': form })


def signup(request):
    if request.method == "POST":
        form = Sign_up(request.POST)
        if form.is_valid():
            user = form.create_new_user()
            if user:
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponse("A user with this username already exists , please choose other username")
    else:
        form = Sign_up()
    return render(request,'stateApp/register.html', {'form': form })


@login_required
@csrf_exempt
def index(request):
    location_name = request.GET.get('city',None)
    if request.method == "GET" and location_name is not None:
        url = "http://maps.googleapis.com/maps/api/geocode/json?address="+location_name + "&sensor=false"
        # fetching the data from google api , can also be done on frontend
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            if not data['results']:
                return HttpResponse("No Information Found")
            data = data['results'][0]
            state_name = data['formatted_address']
            state_name = state_name.split(',')[-3:]
            if len(state_name) > 2:
                state_name = state_name[1]
            else:
                state_name = state_name[0]
            geometry = data['geometry']['location']
            latitude,longitude = geometry['lat'],geometry['lng']
            data_returned = {
                'location_name' : str(location_name),
                'state_name' : str(state_name),
                'latitude' : latitude,
                'longitude' : longitude
            }
        return render(request,'stateApp/new_index.html',{'data':data_returned})
    if request.method == "POST":
        form = Location_form(request.POST)
        if form.is_valid():
            location = form.save_location()
        return HttpResponse(reverse('location'))
    return render(request,'stateApp/index.html')


@login_required
@csrf_exempt
def savelocation(request):
    location = Location.objects.all()
    return render(request,'stateApp/show_table.html',{'data':location})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


