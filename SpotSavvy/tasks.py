# tasks.py

from celery import shared_task
from .models import Activity

@shared_task
def update_activity_location_from_google_maps(activity_id):
    activity = Activity.objects.get(pk=activity_id)
    # Make API call to update location from Google Maps API
    # Update the activity's location based on the API response
    activity.save()
