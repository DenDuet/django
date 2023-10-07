# import datetime
import time
from datetime import datetime, date, timedelta, time
from django.forms import Form
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from dz3.models import User, Goods, Orders
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm, UserForm
# from django.views.decorators.csrf import csrf_protect

import logging

logger = logging.getLogger(__name__)

import random
import time
    
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))

# time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(time.strptime( , '%Y-%m-%d %H:%M')))
            #   datetime.today().strftime('%Y-%m-%d %H:%M')
def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M', prop)
    
# print(random_date("1/1/2000 1:30 PM", "10/10/2022 4:50 AM", random.random()))


def init_bases(request):
    
    User.objects.all().delete()
    Goods.objects.all().delete()        
    Orders.objects.all().delete()            
            
    dt = random_date("2022-10-02 11:30", "2023-10-02 14:50", random.random())        
    persons = [User(username="John",email="i@mail.ru",phone="123-45-67",address="Florida, st.", reg_date=dt), User(username="Bony",email="g@mail.ru",phone="321-22-55",address="California", reg_date=dt), User(username="Claid",email="c@mail.ru",phone="231-01-12",address="NewYork city", reg_date=dt)]
    
    usr = User.objects.bulk_create(persons)

    dt = random_date("2022-10-02 11:30", "2023-10-02 14:50", random.random())
    goods = [Goods(goods_name="TV", description="Телевизор с диагональю 200 дюймов. Показывает офигительно круто. Вау", price=200.0, quantity=10, add_date=dt), Goods(goods_name="TV_2", description="Телевизор с диагональю 300 дюймов. Показывает офигительно круче первого. Вау-Вау", price=300.0, quantity=5, add_date=dt), Goods(goods_name="TV_3", description="Телевизор с диагональю 400 дюймов. Показывает круче вареного яйца. Без комментариев", price=1000.50, quantity=3, add_date=dt), Goods(goods_name="Тумба TV", description="Тумба для телевизора. Для всех моделей.", price=500.90, quantity=11, add_date=dt)]
    
    prod = Goods.objects.bulk_create(goods)

    for i in range(50):
        dt = random_date("2022-10-02 11:30", "2023-10-02 14:50", random.random())
        print(dt)
        order = Orders(customer=User.objects.get(username=usr[random.randint(0,len(usr)-1)].username), total_price=200, date_ordered=dt)                                
        order.save()
        print(order.date_ordered)        
        for j in range(random.randint(1,3)):
            order.goods.add(Goods.objects.filter(goods_name=goods[j].goods_name).first())  
        order.save()   
   
    return render(request, "dz3/base.html", context = {"body": "index page", "title":"Главная страница"})   
    

def index(request):
    logger.info('Index page accessed')
    return render(request, "dz3/base.html", context = {"body": "index page", "title":"Главная страница"})



def read_users(request):
    user = User.objects.all()
    return render(request, "dz3/users.html", context = {"users": user, "title":"Главная страница"})    

def read_goods(request): 
    goods = Goods.objects.all()
    return render(request, "dz3/goods.html", context = {"goods": goods, "title":"Главная страница"})     

def read_orders(request):
    vars = ["за последние 7 дней (неделю)", "за последние 30 дней (месяц)", "за последние 365 дней (год)"]

    goods = Goods.objects.all()
    user = User.objects.all()
    for usr in user:
        orders = usr.orders_set.all()

    return render(request, "dz3/orders1.html", context = {"orders": orders, "users": user, "goods": goods, "title":"Главная страница", "vars":vars})     

def orders_show(request):
    vars = ["за последние 7 дней (неделю)", "за последние 30 дней (месяц)", "за последние 365 дней (год)"]

    username = request.POST.get("username")
    choice = request.POST.get("choice")
    index = vars.index(choice)
    print(username, choice, index)
    goods = Goods.objects.all()
    user = User.objects.get(username=username)
    current_date = datetime.today()
    # .strftime('%Y-%m-%d %H:%M')
    # datetime.datetime.now().date().strftime('%Y-%m-%d %a %H:%M')

    if index==0:
        start_date = current_date - timedelta(days=7)
        orders = user.orders_set.filter(date_ordered__range=(start_date, current_date)).order_by('date_ordered__day')        
    elif index==1:
        start_date = current_date - timedelta(days=30)
        orders = user.orders_set.filter(date_ordered__range=(start_date, current_date)).order_by('date_ordered__month')          
    else:
        start_date = current_date - timedelta(days=356)
        orders = user.orders_set.filter(date_ordered__range=(start_date, current_date)).order_by('date_ordered__year')        
    return render(request, "dz3/orders2.html", context = {"orders": orders, "user": user ,"goods": goods, "title":"Главная страница","period": choice})     


def upload_image(request, goods_id):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            file_url = fs.url(filename)
            good = Goods.objects.get(pk=goods_id)
            good.image = file_url
            good.save()
    else:
        form = ImageForm()
    return render(request, 'dz3/upload_image.html', {'form':
form})
    
def delete_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    # if user==None:  
    #     return JsonResponse(status_code=404, content={ "message": "Пользователь не найден"})
    user.delete()  
    return render(request, "dz3/base.html", {"request":request, "message": "Товар удален"})

def delete_good(request, goods_id: int):
    good = Goods.objects.get(id=goods_id)
    # if good==None:  
    #     return JSONResponse(status_code=404, content={ "message": "Товар не найден"})
    good.delete()  # удаляем объект
    return render(request, "dz3/base.html", {"request":request, "message": "Товар удален"})

def delete_order(request, orders_id: int):
    order = Orders.objects.get(id=orders_id)
    # if order==None:  
    #     return JSONResponse(status_code=404, content={ "message": "Заказ не найден"})
    order.delete()  # удаляем объект
    return render(request, "dz3/base.html", {"request":request, "message": "Заказ удален"})    


def create_user(request):
    username = request.POST.get("username")    
    email = request.POST.get("email")  
    phone = request.POST.get("phone")      
    address = request.POST.get("address")      
    user = User(username=username, email=email, phone=phone, address=address, reg_date=datetime.today().strftime('%Y-%m-%d %H:%M')) 
    user.save()  
    return render(request, "dz3/base.html", context = {"users": user, "title":"Главная страница"})  

def create_good(request):
    goods_name = request.POST.get("goods_name")    
    description = request.POST.get("description")  
    price = request.POST.get("price")      
    quantity = request.POST.get("quantity")     
    good = Goods(goods_name=goods_name, description=description, price=price, quantity=quantity, add_date=datetime.today().strftime('%Y-%m-%d %H:%M'))    
    good.save()
    return render(request, "dz3/base.html", context = {"goods": good, "title":"Главная страница"})     

def create_order(request):
    username = request.POST.get("username")    
    goods_name = request.POST.get("goods_name")  
    total_price = request.POST.get("total_price")       
    user_id = User.objects.filter(username=username).first()     
    orders = Orders(customer=user_id, total_price=total_price, date_ordered=datetime.today().strftime('%Y-%m-%d %H:%M'))    
    orders.save()
    goods_id = Goods.objects.filter(goods_name = goods_name).first()
    orders.goods.add(goods_id)    
    return render(request, "dz3/base.html", {"request":request, "message": "Заказ добавлен"}) 


def edit_user(request, user_id: int):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST)
        user = User.objects.get(pk=user_id)
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.save()
        logger.info(f'Успешно обновили пользователя {user}.')    
        print(f"Заполненная форма прошла проверка данных  {user}")       
        return render(request, 'dz3/base.html', {"request":request, 'users': user})

    else:
        form = UserForm({'users': user})
        print("Пустая форма")
    return render(request, 'dz3/edituser.html', {'users': user, 'form': form})