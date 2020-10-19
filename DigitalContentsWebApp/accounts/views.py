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

from .models import *
from .forms import *


@unauthenticated_user
def homePage(request):
    return render(request, "accounts/homePage.html")


# Unauthenticated users are redirected to this function. The user's post request is validated and user's accounts is
# registered.
@unauthenticated_user
def registerPage(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account successfully created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# Unauthenticated users are redirected to login page and this function validates the post request i.e login
# information entered on login page to allows user into their account.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
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
def viewDashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
def viewProfilePage(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
    context = {'customer': customer}
    return render(request, 'accounts/viewProfilePage.html', context)


# login is required to access profile update feature. The function below receives the profile information and if the
# information is valid it updates it into the user's account.
@login_required(login_url='login')
def editProfilePage(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)

    form = CustomerForm(instance=customer)
    context = {'form': form, 'customer': customer}

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('view_profile')
        else:
            messages.warning(request, 'PLease enter valid information following specified formats.')
    return render(request, 'accounts/editProfilePage.html', context)


@login_required(login_url='login')
def uploadVideoPage(request):
    if request.user.is_authenticated:
        current_user = request.user

    form = VideoUploadForm()

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect('upload_video')
        else:
            messages.warning(request, 'Error uploading file!')

    context = {'form': form}
    return render(request, 'accounts/uploadVideoPage.html', context)


@login_required(login_url='login')
def viewMyContentsPage(request):
    if request.user.is_authenticated:
        current_user = request.user

        current_customer = Customer.objects.get(user=current_user)
        files = File.objects.filter(customer=current_customer)
        context = {'files': files, 'current_customer': current_customer}

    return render(request, 'accounts/viewMyContentPage.html', context)

#todo will be done soon
# @login_required(login_url='login')
# def ComedyVideoPage(request):
#     if request.user.is_authenticated:
#         files = File.objects.filter(category='Technology')
#         context = {'files': files}
#     return render(request, 'accounts/ComedyVideoPage.html', context)

