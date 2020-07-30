from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.
from .forms import OrderForm, CustomerForm, CreateUserForm
from .filters import OrderFilter
from .models import *
from .decorators import unauthenticated_user, allowed_users, admin_only

# @unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm( request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Acccount was created for '+ username) # the messages stored outside and last long until the it is showed

            # add the new aacoiunt to customer group
            group = Group.objects.get( name='customer')
            user.groups.add(group)


            username = request.POST.get('username')
            email = request.POST.get('email')
            # password =request.POST.get('email')
            Customer.objects.create(user = user, name = username, email=email)
            return redirect('login')

    context ={'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)
    # if request.method == 'POST':
    #         username = request.POST.get('username')
    #         password =request.POST.get('password')

    #         user = authenticate(request, username=username, password=password)

    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')
    #         else:
    #             messages.info(request, 'Username OR password is incorrect')

    # context = {}
    # return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    pending = orders.filter(status = 'Pending').count()
    delivered = orders.filter(status = 'Delivered').count()
    print(pending)
    
    context = {'orders': orders, 
    'total_orders': total_orders, 
    'pending': pending, 
    'delivered': delivered}

    return render(request, 'user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    delivered = Order.objects.filter(status = "Deliveried").count()
    pending = Order.objects.filter(status = "Pending").count()

    context = {'orders':orders, 'customers' : customers, 'total_orders': total_orders, 'delivered':delivered, 'pending': pending }
    return render(request,'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def products(request):
    products = Product.objects.all()

    return render(request,'products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def customer(request, id):

    customer = Customer.objects.get(id = id) 
    order_number = customer.order_set.all().count()
    orders = customer.order_set.all()
    print (request.GET)
    myFilter = OrderFilter(request.GET, queryset = orders)
    filtered_orders = myFilter.qs

    context = {'customer': customer, 'order_number': order_number, 'orders': filtered_orders, 'myFilter': myFilter}
    return render(request,'customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def create_order(request, id):
    # customer will be autofilled, and stored in Order table 
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status')) # customer is parent , order is child
    customer = Customer.objects.get(id = id)
    # form = OrderForm(initial={'customer':customer})
    # formset = OrderFormSet(instance = customer)
    formset = OrderFormSet(queryset = Order.objects.none(),instance = customer)

    if (request.method == "POST"):
        formset = OrderFormSet(request.POST, instance = customer ) 
        if formset.is_valid(): # form is not valid
            formset.save()
            return redirect('/customer/'+ str(id))

    context = {'forms': formset, 'customer': customer.name}
    return render (request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def update_order(request, id):
    order = Order.objects.get(id = id)
    form = OrderForm(instance= order) # pre-filled the order for new update 
    if (request.method == "POST"):
        print(request.POST)
        form = OrderForm(request.POST, instance=order) # grap all new infor and store it into instance 
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render (request, 'update_order_form.html', context)

def delete_order(request, id):
    order = Order.objects.get(id = id)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    context = {'item' : order}
    return render (request, 'delete_form.html', context)
    

def create_customer (request):
    form = CustomerForm()
    if (request.method == "POST"):
        print(request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render (request, 'customer_form.html', context)


def delete_customer(request, id):
    customer = Customer.objects.get(id = id)
    if request.method == "POST":
        customer.delete()
        return redirect('/')
    
    context = {'item' : customer}
    return render (request, 'delete_form.html', context)


def update_customer(request, id):
    customer = Customer.objects.get(id = id)
    form = CustomerForm(instance= customer) # pre-filled the order for new update 
    if (request.method == "POST"):
        print(request.POST)
        form = CustomerForm(request.POST, instance=customer) # grap all new infor and store it into instance 
        if form.is_valid():
            form.save()
            return redirect('/customer/' + str(id))
    context = {'form' : form}
    return render (request, 'customer_form.html', context)

def cr_order(request ):
    form = OrderForm()

    if (request.method == "POST"):
        print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render (request, 'update_order_form.html', context)

