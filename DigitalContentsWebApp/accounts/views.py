from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group

# Create your views here.
from .forms import UserRegistrationForm
# from .decorators import permitted_only
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def registerPage(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Viewer')
            user.groups.add(group)

            messages.success(request, 'User account was successfully created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid username or password!')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutFn(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Viewer'])
# @allowed_users(allowed_roles=['Subscriber'])
# @permitted_only
def homePage(request):
    return render(request, 'accounts/dashboard.html')
