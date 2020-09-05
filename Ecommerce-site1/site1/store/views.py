from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from . utils import cookieCart, cartData, guestOrder
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import CreateUserForm
from .models import *
import datetime
import json


# Create your views here.

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created for ' + user + '.')
            return redirect('store-login')

    context = {'form': form}
    return render(request, 'store/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('store-home')
        else:
            messages.info(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('store-login')


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = ProductMdl.objects.all()
    # 3rd 1 pair of key and value change made after copying here ----
    context = {'products': products, 'cartItems': cartItems}
    # Cart count-2-Close
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Cart count - 4 3rd 1 pair of key and value change
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    # Cart count - 4 - Close
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # 3rd 1 pair of key and value change
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    # Cart count - 5 - Close
    return render(request, 'store/checkout.html', context)


#  Add to cart button
def updateItem(request):
    data = json.loads(request.body)
    # Now Let's catch the id of a product
    # whose 'Add to cart' button is clicked
    productId = data['productId']
    # # This ['productId'] is coming from the line body:
    # JSON.stringify({'productId': productId, 'action': action})
    # from views.py
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    # Procedure of Creating order
    #>>1. take logged in customer's name to create order
    customer = request.user.customermdl
    #>>2. take product id to create order
    product = ProductMdl.objects.get(id=productId)
    #>>3. create a complete order
    order, created = OrderMdl.objects.get_or_create(customer=customer, complete=False)
    #>>if the same product is selected more than once
    # then it should either add or decrease its quantity
    orderItem, created = OrderItemMdl.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    # If the quantity is or below 0 then delete the product
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item added', safe=False)

def processOrder(request):
    # print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customermdl
        order, created = OrderMdl.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddressMdl.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)

def weather(request):
    return render(request, 'store/weather.html')