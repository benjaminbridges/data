from django.http import HttpResponse, request
from django.shortcuts import redirect

# redirects logged in users away from pages like login and register
# https://www.youtube.com/watch?v=eBsc65jTKvw&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=15
def unauthenticted_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            permission = None
            #if request.user.profile.site_permission.exists():
                # group = request.user.groups.all()[0].name
            permission = request.user.profile.site_permission
            if permission in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorised to view this page")
        return wrapper_func
    return decorator
