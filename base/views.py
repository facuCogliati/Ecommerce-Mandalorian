from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .form import creatUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.


def home(request):
    return render(request, 'base/home.html', {})


def session_register(request):
    if request.user.is_authenticated:
        return redirect('market')

    form = creatUser()
    if request.method == 'POST':
        form = creatUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse('hecho', safe=False)
        else:
            return JsonResponse({'status' : False}, safe=False)
    context = {'session' : True, 'form' : form}
    return render(request, 'base/login_register.html', context)


def session_login(request):
    if request.method == 'GET':
        username = request.GET.get('email')
        password = request.GET.get('password')

        try:
            user = authenticate(request, username = username, password = password)
            login(request, user)
            return JsonResponse({'status' : True}, safe=False)
        except:
            return JsonResponse({'status' : False, 'message' : 'usuario o contraseña incorrectos'}, safe=False)

        
def session_logOut(request):
    logout(request)
    return redirect('session')


def market(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    products = Product.objects.filter(category__name__icontains = q)
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order , created = Order.objects.get_or_create(client = request.user, complete = False)
    else:
        order = {}

    return render(request, 'base/market.html', {'products' : products, 'order' : order, 'categories' : categories})


def addItemsCard(request):
    print(request.method)
    try:
        id = request.POST.get('id')
        type = request.POST.get('type')
        product = Product.objects.get(id = id)
        order , created = Order.objects.get_or_create(client = request.user, complete = False)
        orderItems, created = OrderItems.objects.get_or_create(order = order, product = product)

        if type == 'plus':
            orderItems.quantify += 1
            orderItems.save()
        else:
            if orderItems.quantify <= 1:
                orderItems.delete()
            else:
                orderItems.quantify -= 1
                orderItems.save()
        return JsonResponse({'status': True}, safe=False)
    except:
        return JsonResponse({'status': False}, safe=False)


def card(request):
    if request.user.is_authenticated:
        order , created = Order.objects.get_or_create(client = request.user, complete = False)
        itemsOrder = order.orderitems_set.all()
    else:
        order = {}
        itemsOrder = {}
    return render(request, 'base/card.html', {'itemsOrder' : itemsOrder, 'order' : order})


@login_required(login_url='session')
def checkOut(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        barrio = request.POST.get('barrio')
        zip = request.POST.get('zip')
        order , created = Order.objects.get_or_create(client = request.user, complete = False)
        order.complete = True
        order.save()
        ClientAddres.objects.create(
            client = request.user,
            order = order,
            address = address,
            city = city,
            zipcode = zip,
        )
        return JsonResponse('ordern realizada', safe=False)
    return render(request, 'base/check-out.html', {})