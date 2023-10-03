import datetime
from django.forms import Form
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from dz2.models import User, Goods, Orders
from django.views.decorators.csrf import csrf_protect

import logging

logger = logging.getLogger(__name__)
# Create your views here.

# app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'

# csrf = CSRFProtect(app)

# const csrftoken = Cookies.get('csrftoken');

def init_bases(request):
    
    User.objects.all().delete()
    Goods.objects.all().delete()        
    Orders.objects.all().delete()            
            
            
    persons = [User(username="John",email="i@mail.ru",phone="123-45-67",address="Florida, st.", reg_date=datetime.datetime), User(username="Bony",email="g@mail.ru",phone="321-22-55",address="California", reg_date=datetime.datetime), User(username="Claid",email="c@mail.ru",phone="231-01-12",address="NewYork city", reg_date=datetime.datetime)]
    
    usr = User.objects.bulk_create(persons)


    goods = [Goods(goods_name="TV", description="Телевизор с диагональю 200 дюймов. Показывает офигительно круто. Вау", price=200.0, quantity=10, add_date=datetime.datetime), Goods(goods_name="TV_2", description="Телевизор с диагональю 300 дюймов. Показывает офигительно круче первого. Вау-Вау", price=300.0, quantity=5, add_date=datetime.datetime), Goods(goods_name="TV_3", description="Телевизор с диагональю 400 дюймов. Показывает круче вареного яйца. Без комментариев", price=1000.50, quantity=3, add_date=datetime.datetime), Goods(goods_name="Тумба TV", description="Тумба для телевизора. Для всех моделей.", price=500.90, quantity=11, add_date=datetime.datetime)]
    
    prod = Goods.objects.bulk_create(goods)


    order = Orders(customer=User.objects.get(username="John"), total_price=200, date_ordered=datetime.datetime)
    order.save()
    # g=Goods.objects.filter(goods_name="TV").first()
    # print(g)
    order.goods.add(Goods.objects.filter(goods_name="TV").first())  
    order.goods.add(Goods.objects.filter(goods_name="TV_1").first())
    order.save()   
    
    order = Orders(customer=User.objects.get(username="John"), total_price=250, date_ordered=datetime.datetime)
    order.save()
    order.goods.add(Goods.objects.filter(goods_name="TV_2").first())
    order.save()
    
    order = Orders(customer=User.objects.get(username="Bony"), total_price=210, date_ordered=datetime.datetime)
    order.save()
    order.goods.add(Goods.objects.filter(goods_name="TV_2").first())
    order.goods.add(Goods.objects.filter(goods_name="TV_1").first())
    order.goods.add(Goods.objects.filter(goods_name="TV").first())
    order.save()
    
    order = Orders(customer=User.objects.get(username="Claid"), total_price=215.5, date_ordered=datetime.datetime)
    order.save() 
    order.goods.add(Goods.objects.filter(goods_name="TV").first())
    order.goods.add(Goods.objects.filter(goods_name="TV_1").first())
    order.save()
    return render(request, "base.html", context = {"body": "index page", "title":"Главная страница"})   
    

def index(request):
    logger.info('Index page accessed')
    return render(request, "dz2/base.html", context = {"body": "index page", "title":"Главная страница"})



def read_users(request):
    user = User.objects.all()
    return render(request, "dz2/users.html", context = {"users": user, "title":"Главная страница"})    

def read_goods(request): 
    goods = Goods.objects.all()
    return render(request, "dz2/goods.html", context = {"goods": goods, "title":"Главная страница"})     

def read_orders(request):
    # orders = Orders.objects.all()
    # .join(User).join(Goods)
    goods = Goods.objects.all()
    user = User.objects.all()
    for usr in user:
        orders = usr.orders_set.all()
        # print(f"user = {usr},  order = {orders}")
    # orders = Orders.objects.all()
    # for order in orders:
    #     print(f"user = {order.customer.username}, order = {order}")
    return render(request, "dz2/orders.html", context = {"orders": orders, "users": user, "goods": goods, "title":"Главная страница"})     



def create_user(request):
    username = request.POST.get("username")    
    email = request.POST.get("email")  
    phone = request.POST.get("phone")      
    address = request.POST.get("address")      
    user = User(username=username, email=email, phone=phone, address=address, reg_date=datetime.datetime) 
    user.save()  
    return render(request, "dz2/base.html", context = {"users": user, "title":"Главная страница"})  

def create_good(request):
    goods_name = request.POST.get("goods_name")    
    description = request.POST.get("description")  
    price = request.POST.get("price")      
    quantity = request.POST.get("quantity")     
    good = Goods(goods_name=goods_name, description=description, price=price, quantity=quantity, add_date=datetime.datetime)    
    good.save()
    return render(request, "dz2/base.html", context = {"goods": good, "title":"Главная страница"})     

def create_order(request):
    username = request.POST.get("username")    
    goods_name = request.POST.get("goods_name")  
    total_price = request.POST.get("total_price")       
    user_id = User.objects.filter(username=username).first()     
    orders = Orders(customer=user_id, total_price=total_price, date_ordered=datetime.datetime)    
    orders.save()
    goods_id = Goods.objects.filter(goods_name = goods_name).first()
    orders.goods.add(goods_id)    
    return render(request, "dz2/base.html", {"request":request, "message": "Заказ добавлен"}) 



def delete_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    # if user==None:  
    #     return JsonResponse(status_code=404, content={ "message": "Пользователь не найден"})
    user.delete()  
    return render(request, "dz2/base.html", {"request":request, "message": "Заказ добавлен"})

def delete_good(request, goods_id: int):
    good = Goods.objects.get(id=goods_id)
    # if good==None:  
    #     return JSONResponse(status_code=404, content={ "message": "Товар не найден"})
    good.delete()  # удаляем объект
    return render(request, "dz2/base.html", {"request":request, "message": "Заказ добавлен"})

def delete_order(request, orders_id: int):
    order = Orders.objects.get(id=orders_id)
    # if order==None:  
    #     return JSONResponse(status_code=404, content={ "message": "Заказ не найден"})
    order.delete()  # удаляем объект
    return render(request, "dz2/base.html", {"request":request, "message": "Заказ добавлен"})