from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
# Create your views here.
def home(request):
    return render(request,'home.html')
def signup(request):
    if request.method == 'POST':
        user_form = forms.SignupForm(request.POST)
        profile_form = forms.ProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile_form = forms.ProfileForm(request.POST,instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = forms.SignupForm()
        profile_form = forms.ProfileForm()
        context = {
            'user_form' : user_form,
            'profile_form' : profile_form
        }
        return render(request,'signup.html',context)
            
        