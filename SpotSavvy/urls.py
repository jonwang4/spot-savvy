from django.urls import include, path
from django.contrib.auth.decorators import login_required
from .views import homepage, RegisterView, registration_view, profile, logout_view

urlpatterns = [
    path('', homepage, name='home'),  # Handle the root URL
    path('homepage/<str:username>/', homepage, name='home_with_username'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/', login_required(profile), name='profile'),
    path('logout/', logout_view, name='logout'),
]
