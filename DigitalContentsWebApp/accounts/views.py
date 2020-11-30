from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group

# Create your views here.
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm
# from .decorators import permitted_only
from .decorators import unauthenticated_user, allowed_users

from .models import *
from .forms import *
from .filters import FileFilter, CustomerFilter

# TODO review these imports
import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime
from datetime import date, timedelta, datetime
from .models import StripeCustomer


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
    premium_files = File.objects.filter(premium=True)
    freemium_files = File.objects.filter(premium=False)

    # query count is reduced by 1 to match the for loop counter in template
    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    # all premium and freemium files are passed to total query objects for search feature
    # query count is reduced by 1 to match the for loop counter in template
    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    # try and except checks if the subscription status is active or inactive to add/remove video poster for
    # premium content
    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/dashboard.html', context)

    # if stripe customer doesnot exist it means subscription status is inactive
    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/dashboard.html', context)


# function gets current customer and prints all of its information on the template using attributes of the
# Customer model
@login_required(login_url='login')
def viewProfilePage(request):
    if request.user.is_authenticated:
        curr_customer = Customer.objects.get(user=request.user)
        contents = File.objects.filter(customer=curr_customer)
        my_contents_count = contents.count()
    context = {'curr_customer': curr_customer, 'my_contents_count': my_contents_count}
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


# authenticates the user and provides user a form to upload video file
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

        # get current customer, premium and freemium files
        current_customer = Customer.objects.get(user=current_user)
        premium_files = File.objects.filter(customer=current_customer, premium=True)
        freemium_files = File.objects.filter(customer=current_customer, premium=False)

        content_category = 'My Contents'  # category is for the template

        # count is reduced by 1 to match the for loop counter in template tag
        premium_count = premium_files.count() - 1
        freemium_count = freemium_files.count() - 1

        # total query for search we need all objects for search query
        total_query_files = premium_files | freemium_files
        searchFilter = FileFilter(request.GET, queryset=total_query_files)
        total_query_files = searchFilter.qs
        total_query_files_count = total_query_files.count() - 1

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/viewMyContentPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def comedyCategoryPage(request):
    premium_files = File.objects.filter(category='Comedy', premium=True)
    freemium_files = File.objects.filter(category='Comedy', premium=False)
    content_category = 'Comedy Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def fitnessCategoryPage(request):
    premium_files = File.objects.filter(category='Fitness', premium=True)
    freemium_files = File.objects.filter(category='Fitness', premium=False)
    content_category = 'Fitness Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def cookingCategoryPage(request):
    premium_files = File.objects.filter(category='Cooking', premium=True)
    freemium_files = File.objects.filter(category='Cooking', premium=False)
    content_category = 'Cooking Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def entertainmentCategoryPage(request):
    premium_files = File.objects.filter(category='Entertainment', premium=True)
    freemium_files = File.objects.filter(category='Entertainment', premium=False)
    content_category = 'Entertainment Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def technologyCategoryPage(request):
    premium_files = File.objects.filter(category='Technology', premium=True)
    freemium_files = File.objects.filter(category='Technology', premium=False)
    content_category = 'Technology Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def musicCategoryPage(request):
    premium_files = File.objects.filter(category='Music', premium=True)
    freemium_files = File.objects.filter(category='Music', premium=False)
    content_category = 'Music Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def otherCategoryPage(request):
    premium_files = File.objects.filter(category='Other', premium=True)
    freemium_files = File.objects.filter(category='Other', premium=False)
    content_category = 'Other Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/contentCategoriesPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/contentCategoriesPage.html', context)


# function that counts the views of the file
@login_required(login_url='login')
def contentViewersCount(request, pk):
    file = get_object_or_404(File, pk=pk)

    # if the user isn't in viewers list of the file then add it to the list
    if request.user not in file.content_viewers.all():
        file.content_viewers.add(request.user)
    context = {'file': file}
    return render(request, 'accounts/videoPlayerPage.html', context)


# TODO explore more about this function
@login_required(login_url='login')
def roomShowChatHome(request):
    if request.user.is_authenticated:
        current_user = request.user
        customer = Customer.objects.get(user=request.user)
    context = {'person_name': customer}
    return render(request, "accounts/room_chat_home.html", context)


# this function diaplays the chat page for chat room
@login_required(login_url='login')
def roomShowChatPage(request, room_name, person_name):
    if request.user.is_authenticated:
        current_user = request.user

        customer = Customer.objects.get(user=current_user)
    context = {'customer': customer}
    return render(request, "accounts/room_chat_screen.html", {'room_name': room_name, 'person_name': person_name})


# this function takes you to chat screen and lists the user available for chat
@login_required(login_url='login')
def customersListPage(request):
    customers = Customer.objects.all()
    curr_user = request.user

    searchFilter = CustomerFilter(request.GET, queryset=customers)
    customers = searchFilter.qs
    query_set_count = customers.count()

    context = {'customers': customers, 'curr_user': curr_user, 'searchFilter': searchFilter,
               'query_set_count': query_set_count}
    return render(request, 'accounts/chat_screen.html', context)


# TODO explore more about this function
@login_required(login_url='login')
def ShowChatHome(request):
    if request.user.is_authenticated:
        current_user = request.user
        customer = Customer.objects.get(user=request.user)
    context = {'person_name': customer}
    return render(request, context)


# This function displays the chat page and customer list for one-on-one chat
@login_required(login_url='login')
def ShowChatPage(request, pk):
    # code segment for listing the user for chat and search feature associated with it
    customers = Customer.objects.all()
    curr_user = request.user
    searchFilter = CustomerFilter(request.GET, queryset=customers)
    customers = searchFilter.qs
    query_set_count = customers.count()
    # code segment for creating unique room for a pair of users
    sender_id = request.user.customer.id

    # unique room number is created for every unique pair if id is 0 it is an exception so a hardcoded uniqued room 0
    # is manually assigned to room name
    if sender_id == 1 or pk == 1:
        room_name = str(0)
    else:
        # unique room number is created for every unique pair
        room_name = str((sender_id * pk) * (sender_id + pk))

    # person_name is passed to chat page to move texts left or right based on sender/reciver
    person_name = request.user.customer.user

    context = {'room_name': room_name, 'person_name': person_name, 'customers': customers, 'curr_user': curr_user,
               'searchFilter': searchFilter,
               'query_set_count': query_set_count}
    return render(request, "accounts/chat_screen.html", context)


# This function saves the files to saved files list
@login_required(login_url='login')
def savedFiles(request, pk):
    file = get_object_or_404(File, pk=pk)
    customer = get_object_or_404(Customer, user=request.user)

    if file not in customer.saved_files.all():
        customer.saved_files.add(file)
    return redirect('saved_files_list')


# this function removes the files from customer's saved files list
@login_required(login_url='login')
def deleteSavedFiles(request, pk):
    file = get_object_or_404(File, pk=pk)
    customer = get_object_or_404(Customer, user=request.user)
    customer.saved_files.remove(file)
    return redirect('saved_files_list')


# This function filters the  premium and freemium files
# all files are stored in total_query_files for search feature
# counter are reduced by 1 to match for loop counter in template
# try and except checks if the user's subscription status is active and passes context based on that
# total_query_files.count() != premium_files.count() + freemium_files.count() :- if the query count is not
# premium + freemium files count i.e if all the files aren't requested to display on the page it means search has been
# called so we print search files only
@login_required(login_url='login')
def listSavedFiles(request):
    curr_customer = get_object_or_404(Customer, user=request.user)

    premium_files = curr_customer.saved_files.filter(premium=True)
    freemium_files = curr_customer.saved_files.filter(premium=False)

    content_category = 'My Saved Contents'

    premium_count = premium_files.count() - 1
    freemium_count = freemium_files.count() - 1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count() - 1

    try:
        # code segment to verify subscription status
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count, 'subscription': subscription}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count, 'subscription': subscription}
            return render(request, 'accounts/savedFilesListPage.html', context)

    except StripeCustomer.DoesNotExist:
        if total_query_files.count() != premium_files.count() + freemium_files.count():
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                       'total_query_files_count': total_query_files_count}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/savedFilesListPage.html', context)


# this function receives request if the user goes to subscribe and gets stripe_customer from StripeCustomer objects
@login_required(login_url='login')
def subscribe(request):
    try:
        # Retrieving subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)
        # More additional data from subscription or product
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'accounts/subscribe.html', {
            'subscription': subscription,
            'product': product,
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'accounts/subscribe.html')

# it is used to handle the ajax request
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

# this function sends ajax request to the server and generate a new checkout id
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# this function prints subscription successful message
@login_required(login_url='login')
def success(request):
    return render(request, 'accounts/success.html')


# TODO cancel subscription
@login_required(login_url='login')
def cancel(request):
    return render(request, 'accounts/cancel.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)
