from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, ** kwargs):
        if request.user.is_authenticated:
        	return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper( request, *args, **kwargs):
            role = None
            if request.user.groups.exists():
                role = request.user.groups.all()[0].name # extract the admin's name group
                if role in allowed_roles:
                    return view_func(request, *args, *kwargs)
                else:
                    return HttpResponse('you are not authenticated to view this page')
           
        return wrapper
    return decorator

def admin_only(view_func):
    def wrapper( request, *args, **kwargs):
        role = None
        if request.user.groups.exists():
            role = request.user.groups.all()[0].name # extract the admin's name group
            if role == 'customer':
                return redirect('user_page')
            else:
                return view_func(request, *args, **kwargs)

    return wrapper
