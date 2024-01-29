# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from datetime import date
from django.http import HttpResponse
from .models import Activity, ActivityCategory, Location, UserProfile
from .tasks import update_activity_location_from_google_maps


# Create your views here.
# views.py
# **creating API calls may cause latency problems here** || using celery for asynchronous tasks

def create_activity(request):
    # Assume you get the necessary data from the request
    # For example, category_name, date, etc.
    category_name = request.POST.get('category_name', 'Default Category')
    date = request.POST.get('date')  # Adjust this based on your actual form data

    # Create the activity
    activity = Activity.objects.create(
        user=request.user,
        enjoyability_score=5,
        latitude=0.0,
        longitude=0.0,
        review="",
        category=ActivityCategory.objects.get_or_create(name=category_name)[0],
        location=Location.objects.get_or_create(
            name='Default Location',
            latitude=37.7749, #should change lat and long to default, or form created location || when user form is created, define activity location there?
            longitude=-122.4194,
            address='Default Address'
        )[0],
        date=date,
    )

    # Asynchronously update activity location using Celery task
    update_activity_location_from_google_maps.delay(activity.id)

    # Render a template or redirect as needed
    return render(request, 'your_template.html', {'activity': activity})

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)
            # Redirect to the user's homepage
            return redirect('home', username=user.username)
            #return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class RegisterView(CreateView):
    template_name = 'registration/register.html'  # Create this template
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

@login_required
def homepage(request, username=None):
    if username:
        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)
        return render(request, 'homepage.html', {'user': user})
    else:
        return render(request, 'homepage.html')  # You can modify this based on your needs

@login_required
def profile(request, username):
    # Retrieve activities associated with the current user
    user_activities = Activity.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get(user__username=username)
    # Pass the activities to the template
    return render(request, 'profile.html', {'user_activities': user_activities})

def logout_view(request):
    # Custom logic before logout if needed
    return LogoutView.as_view()(request)