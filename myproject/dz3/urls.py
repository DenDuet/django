from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.index, name='index'),
    path('init_bases/', views.init_bases, name='initialize bases'),    
    path('users/', views.read_users, name='read users base'),   
    path('goods/', views.read_goods, name='read goods base'),       
    path('orders/', views.read_orders, name='read orders base'),  
    path('orders/show/', views.orders_show, name='show orders base'),     

]
