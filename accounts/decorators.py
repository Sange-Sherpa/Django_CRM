from django.shortcuts import redirect

def unauthenticated_user(view_func): 
    # view_func is the name of the function where the decorator is used eg. userLogin in views.py
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('user')
        return wrapper_func
    return decorator



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Customer':
            return redirect('user')

        if group == 'Admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func


