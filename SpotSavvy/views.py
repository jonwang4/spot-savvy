# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Activity, ActivityCategory, Location

# Create your views here.
# views.py

def create_activity(request):
    # Assume you get the necessary data from the request
    # For example, category_name, date, etc.

    # Create the activity
    activity = Activity.objects.create(
        enjoyability_score=5,  # Provide a default value or get it from the request
        latitude=0.0,  # Provide a default value or get it from the request
        longitude=0.0,  # Provide a default value or get it from the request
        review="",  # Provide a default value or get it from the request
        category=ActivityCategory.objects.get_or_create(name=category_name)[0],
        location=Location.objects.get_or_create(
            name='Default Location',
            latitude=37.7749,  # Placeholder latitude (e.g., central point of a city)
            longitude=-122.4194,  # Placeholder longitude (e.g., central point of a city)
            address='Default Address'
        )[0],
        date=date,  # Get it from the request
    )

    # Your logic to update the activity's location from Google Maps API
    activity.update_location_from_google_maps()

    # Render a template or redirect as needed
    return render(request, 'your_template.html', {'activity': activity})
