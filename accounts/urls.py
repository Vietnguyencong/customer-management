from django.urls import path, include 
from . import views

urlpatterns = [
    path('register/', views.registerpage, name = 'register'),
    path('login/', views.loginpage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('user/', views.user_page, name='user_page'),

    path('', views.home, name = 'home'),
    path('products/', views.products, name = 'product'),
    path('customer/<int:id>', views.customer, name = 'customer'),
    path('create_order/<int:id>', views.create_order, name = 'create_order'),
    path('update_order/<int:id>', views.update_order, name = 'update_order'),
    path('delete_order/<int:id>', views.delete_order, name = 'delete_order'),

    path('create_customer/', views.create_customer, name = 'create_customer'),
    path('delete_customer/<int:id>', views.delete_customer, name = 'delete_customer'),
    path('update_customer/<int:id>', views.update_customer, name = 'update_customer'),

    path('create_order/', views.cr_order, name = 'cr_order'),


]

