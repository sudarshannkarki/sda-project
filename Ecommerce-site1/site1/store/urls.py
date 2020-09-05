from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store-home'),

    path('register/', views.registerPage, name='store-register'),
    path('login/', views.loginPage, name='store-login'),
    path('logout/', views.logoutUser, name='store-logout'),

    path('cart/', views.cart, name='store-cart'),
    path('checkout/', views.checkout, name='store-checkout'),
    path('update-item/', views.updateItem, name='store-update-item'),
    path('process-order/', views.processOrder, name='store-process-order'),

    path('weather/', views.weather, name='store-weather'),
]
