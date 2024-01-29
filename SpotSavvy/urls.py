from django.urls import include, path
from .views import homepage, RegisterView, registration_view

urlpatterns = [
    path('', homepage, name='home'),  # Handle the root URL
    path('homepage/<str:username>/', homepage, name='home'),  # Adjust the path based on your needs
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
]

