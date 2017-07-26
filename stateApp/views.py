from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate, login,logout
from .forms import Sign_up,Location_form
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from django.views.decorators.http import require_http_methods,require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from stateApp.models import Location
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings



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



class SearchStateView(View):
    form_class = Location_form


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SearchStateView, self).dispatch(request, *args, **kwargs)


    @method_decorator(login_required,csrf_exempt)
    def get(self, request, *args, **kwargs):
        city = request.GET.get('city',None)
        print(settings.STATIC_ROOT)
        if city:
            url = "http://maps.googleapis.com/maps/api/geocode/json?address="+city + "&sensor=false"
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
                    'location_name' : str(city),
                    'state_name' : str(state_name),
                    'latitude' : latitude,
                    'longitude' : longitude
                }
            return render(request,'stateApp/new_index.html',{'data':data_returned})
        else:
            return render(request,'stateApp/index.html')


    @method_decorator(login_required,csrf_exempt)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            location = form.save_location()
        return HttpResponse(reverse('location'))


@login_required
@csrf_exempt
def getLocations(request):
    location = Location.objects.all()
    return render(request,'stateApp/show_table.html',{'data':location})




