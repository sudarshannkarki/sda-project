from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomerMdl(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # here one to one relationship with User because one user can be one customer
    # on_delete=CASCADE - if user is deleted then this item/entity will also get deleted.
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class ProductMdl(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    # price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    # Here, default value for digital is False which means this particular item is a physical item.
    # >>If digital = False - It means this is a physical item,
    # that needs to be shipped physically and it needs shipping address.
    # >>If digital = True - It means this is a digital item (ebook, source code etc)or non-physical item
    # and does not need shipping address and can be transferred by the Internet.
    image = models.ImageField(null=True, blank=True)
    # this image field is added later
    # While adding images for product from the admin panel,
    # do not stroe the images in static folder.
    # Add the images from any random location.
    # Once images are added, they will reside in static folder themselves.
    # So, do not store the images in static folder in advance.

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# OrderMdl is cart
class OrderMdl(models.Model):
    customer = models.ForeignKey(CustomerMdl, on_delete=models.SET_NULL, null=True, blank=True)
    # here many to one relationship is created to CustomerMdl by using foreign key
    # which means one customer can make multiple orders
    # on_delete=models.SET_NULL - if customer is deleted then also order will not be cancelled/deleted
    # and customer value will remain null
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    # this is status of the cart.
    # if complete is false that is an open cart we can continue adding items to that cart
    # if complete is true this is a closed cart we need to create items and add them to a different order.
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitemmdl_set.all()

        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitemmdl_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitemmdl_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItemMdl(models.Model):
    product = models.ForeignKey(ProductMdl, on_delete=models.SET_NULL, null=True)
    # connecting to ProductMdl to know what product is being attached
    order = models.ForeignKey(OrderMdl, on_delete=models.SET_NULL, null=True)
    # many to one relationship with OrderMdl so multiple orderitems can be in one order
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(self.product.name)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddressMdl(models.Model):
    customer = models.ForeignKey(CustomerMdl, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderMdl, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
