from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from stateApp.models import Location



class Login_form(forms.Form):
	username = forms.CharField(label = "Your name",max_length = "100")
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

	def check_login(self):
	     username = self.cleaned_data['username']
	     password = self.cleaned_data['password'] 
	     user = authenticate(username = username,password = password)
	     return user

class Sign_up(forms.Form):
	username = forms.CharField(label = "your name",max_length = "100")
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

	def create_new_user(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user_exists = User.objects.filter(username=username)
		if len(user_exists) == 0:
			user = User.objects.create_user(username,username,password)
			user.save()
			return user
		else:
			return False


class Location_form(forms.Form):
	#Do i need this? will check later
	location_name = forms.CharField(max_length = "100")
	state_name = forms.CharField(max_length = "100")
	latitude = forms.CharField(max_length = "100")
	longitude = forms.CharField(max_length = "100")

	def save_location(self):
		location_name = self.cleaned_data['location_name']
		state_name = self.cleaned_data['state_name']
		latitude = self.cleaned_data['latitude']
		longitude = self.cleaned_data['longitude']
		location = Location(city=location_name,state=state_name,latitude=latitude,longitude=longitude)
		location.save()
		return location
