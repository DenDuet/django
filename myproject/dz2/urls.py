from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.index, name='index'),
    path('init_bases/', views.init_bases, name='initialize bases'),
    path('users/', views.read_users, name='read users base'),   
    path('goods/', views.read_goods, name='read goods base'),       
    path('orders/', views.read_orders, name='read orders base'),      
    path('users/create/', views.create_user, name='create user'),   
    path('goods/create/', views.create_good, name='create good'),       
    path('orders/create/', views.create_order, name='create order'),   
    path('users/delete/<int:user_id>/', views.delete_user, name='delete user'),   
    path('goods/delete/<int:goods_id>/', views.delete_good, name='delete good'),       
    path('orders/delete/<int:orders_id>/', views.delete_order, name='delete order'),            
]
