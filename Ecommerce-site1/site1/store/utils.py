import json
from . models import *


def cookieCart(request):
    # Cookie for guest - 3
    # Getting our cookie
    try:
        cart = json.loads(request.COOKIES['cart'])
    # Here, json.loads() converts string cart value into dictionary to be used in here in python
    # ['cart'] is the name we have given to our cookie
    except:  # If we dont do try and except here, we get an error called KeyError at /cart/
        cart = {}

    print('Cart:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    # Cart count - 4 2nd 1 line of change
    cartItems = order['get_cart_items']

    # Looping through the items in the cart.

    for i in cart:
        try:
            # Looping to access each item to increase/decrease its quantity
            # Now, we can see the cart count for guest user as well.
            cartItems += cart[i]['quantity']

            # Calculating total items and total amount
            product = ProductMdl.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            # Displaying image, its price, its quantity, its sub total
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
            # This try except is here to pass one issue in one case
            # That is if guest user keeps an item in the cart and left without purchasing.
            # and, at the same same time if admin delets that item (for any reason)
            # then when guest user comes back and check his/her cart (cart.html)
            # then there will be an error. Instead cart.html page will show up without that particular item.

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customermdl
        order, created = OrderMdl.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmdl_set.all()
        #  here order is a parent value (field in OrderItemMdl model)
        #  which referes to Ordermdl object(parent table) as a foreign key
        # here, orderitemmdl is OrderItemMdl object(child table)

        # Cart count - 5 - Start
        # 1st 1 line of change
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print('User is not logged in.......7')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = CustomerMdl.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = OrderMdl.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = ProductMdl.objects.get(id=item['product']['id'])

        orderItems = OrderItemMdl.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order