from django.contrib.auth import authenticate, login
from common.forms import UserForm
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpRequest

# Create your views here.

def signup(request:HttpRequest):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = UserForm()
	return render(request, 'common/signup.html', {'form':form})
