from django.urls import path
from . import views

urlpatterns = [
    
    path("dz1/", views.index, name='index'),
    path('dz1/about/', views.about, name='about'),
]
