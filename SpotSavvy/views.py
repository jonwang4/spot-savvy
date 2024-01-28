# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

def homepage(request, username):
    # Retrieve the user based on the provided username
    user = get_object_or_404(User, username=username)
    return render(request, 'homepage.html', {'user': user})

@login_required
def profile(request, username):
    # Retrieve activities associated with the current user
    user_activities = Activity.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get(user__username=username)
    # Pass the activities to the template
    return render(request, 'profile.html', {'user_activities': user_activities})