# models.py
from django.contrib.auth.models import User
from django.db import models
import requests

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"

class ActivityCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Activity(models.Model):
    enjoyability_score = models.PositiveIntegerField(default=5)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    review = models.TextField(blank=True)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)  # Making 'location' nullable || may need to fix later, is default scraped from API?
    date = models.DateField()
    date = models.DateField()

    def __str__(self):
        return f"{self.category.name} - {self.date}"

    def update_location_from_google_maps(self):
        # Make a request to Google Maps API to retrieve location details
        response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params={
                'address': f'{self.category.name}, {self.date}',  # Use a meaningful address for better results
                'key': 'Your Google Maps API Key',
            }
        )

        # Parse the response and update the activity's location
        if response.status_code == 200:
            data = response.json()
            # Extract latitude, longitude, and address from the API response
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            address = data['results'][0]['formatted_address']

            # Update the activity's location
            self.location.latitude = latitude
            self.location.longitude = longitude
            self.location.address = address
            self.location.save()
