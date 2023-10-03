from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.index, name='index'),
    path('dz1/about/', views.about, name='about'),
]
