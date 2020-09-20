from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
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
                return HttpResponse("Unauthorized access!")

        return wrapper_func

    return decorator


# todo this function will be later used when allowing only subscriber to access some of the features. same for other
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
