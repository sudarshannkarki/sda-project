from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomerMdl)
admin.site.register(ProductMdl)
admin.site.register(OrderMdl)
admin.site.register(OrderItemMdl)
admin.site.register(ShippingAddressMdl)
