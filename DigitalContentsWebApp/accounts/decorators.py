from django.http import HttpResponse
from django.shortcuts import redirect


# The following function verifies if the user is authenticated or not. If the user is authenticated it redirects the
# user to url = 'dashboard' else it returns the user's request to function associated with this function in views.py
# i.e the request is passed to the function having @unauthenticated_user on its top in views.py
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# This function defines the functionality of allowing only the users in allowed roles to access the specified
# functionality in the application.
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Unauthorized access!")

        return wrapper_func

    return decorator

# todo this function will be used later when allowing only subscriber to access some of the features. same for other
#  permitted users

# def permitted_only(view_func):
#     def wrapper_function(request, *args, **kwargs):
#
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name
#
#         if group == 'Viewer':
#             return view_func(request, *args, **kwargs)
#
#         if group == 'Subscriber':
#             return redirect('----any url other than unauthenticatedViews/permitted_onlyViews if not permitted--')
#
#     return wrapper_function
