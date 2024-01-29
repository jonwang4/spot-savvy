# -*- coding: utf-8 -*-
# admin.py
from __future__ import unicode_literals
from django.contrib import admin
from .models import Activity, ActivityCategory, Location, UserProfile

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'category', 'location')  # Customize fields displayed in the list view
    search_fields = ('user__username', 'category__name', 'location__name')  # Add search functionality based on specified fields
    list_filter = ('category', 'date')  # Add filters for certain fields

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'address')
    search_fields = ('name', 'address')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')
    search_fields = ('user__username', 'bio')
