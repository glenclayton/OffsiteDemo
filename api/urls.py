"""
URL configuration for the API app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('nigel-number/', views.NigelNumberAPIView.as_view(), name='nigel-number'),
]