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
from accounts.stripe import (VideosPlan, set_paid_until)
from django.http import HttpResponse

# Defining API key
API_KEY = settings.STRIPE_SECRET_KEY


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

    premium_count = premium_files.count()-1
    freemium_count = freemium_files.count()-1

    total_query_files = premium_files | freemium_files
    searchFilter = FileFilter(request.GET, queryset=total_query_files)
    total_query_files = searchFilter.qs
    total_query_files_count = total_query_files.count()-1

    if total_query_files.count() != premium_files.count()+freemium_files.count():
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter,
                   'total_query_files_count': total_query_files_count}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/dashboard.html', context)


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
        premium_files = File.objects.filter(customer=current_customer, premium=True)
        freemium_files = File.objects.filter(customer=current_customer, premium=False)

        content_category = 'My Contents'
        premium_count = premium_files.count() - 1
        freemium_count = freemium_files.count() - 1

        total_query_files = premium_files | freemium_files
        searchFilter = FileFilter(request.GET, queryset=total_query_files)
        total_query_files = searchFilter.qs

        if total_query_files.count() == 1:
            context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
            return render(request, 'accounts/querySearchList.html', context)
        else:
            context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                       'content_category': content_category, 'searchFilter': searchFilter,
                       'premium_count': premium_count, 'freemium_count': freemium_count}
            return render(request, 'accounts/viewMyContentPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)


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

    if total_query_files.count() == 1:
        context = {'total_query_files': total_query_files, 'searchFilter': searchFilter}
        return render(request, 'accounts/querySearchList.html', context)
    else:
        context = {'freemium_files': freemium_files, 'premium_files': premium_files,
                   'content_category': content_category, 'searchFilter': searchFilter,
                   'premium_count': premium_count, 'freemium_count': freemium_count}
        return render(request, 'accounts/contentCategoriesPage.html', context)

def contentViewersCount(request, pk):
    file = get_object_or_404(File, pk=pk)
    if request.user not in file.content_viewers.all():
        file.content_viewers.add(request.user)
    context = {'file': file}
    return render(request, 'accounts/videoPlayerPage.html', context)


def roomShowChatHome(request):
    if request.user.is_authenticated:
        current_user = request.user
        customer = Customer.objects.get(user=request.user)
    context = {'person_name': customer}
    return render(request, "accounts/room_chat_home.html", context)


def roomShowChatPage(request, room_name, person_name):
    if request.user.is_authenticated:
        current_user = request.user

        customer = Customer.objects.get(user=current_user)
    context = {'customer': customer}
    return render(request, "accounts/room_chat_screen.html", {'room_name': room_name, 'person_name': person_name})


def customersListPage(request):
    customers = Customer.objects.all()
    curr_user = request.user

    searchFilter = CustomerFilter(request.GET, queryset=customers)
    customers = searchFilter.qs
    query_set_count = customers.count()

    context = {'customers': customers, 'curr_user': curr_user, 'searchFilter': searchFilter,
               'query_set_count': query_set_count}
    return render(request, 'accounts/customersListPage.html', context)


def ShowChatHome(request):
    if request.user.is_authenticated:
        current_user = request.user
        customer = Customer.objects.get(user=request.user)
    context = {'person_name': customer}
    return render(request, context)


def ShowChatPage(request, pk):
    sender_id = request.user.id

    if sender_id == 1 or pk == 1:
        room_name = str(0)
    else:
        room_name = str((sender_id * pk) * (sender_id + pk))

    person_name = request.user.first_name
    context = {'room_name': room_name, 'person_name': person_name}
    return render(request, "accounts/chat_screen.html", context)


# After the payment is done, payment gateway sends djnago an HHTP POST request with details of completed transactions.
# Stripe calls http post request "webhooks".
# Add basic validation to make sure this POST comes from Stripe. Do this by adding Http header which contains string called signature.
def stripe_webhooks(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SIGNING_KEY
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'charge.succeeded':
        # object has  payment_intent attr
        set_paid_until(event.data.object)
    # return status should be 200 or else stripe will keep on posting the event
    return HttpResponse(status=200)


@login_required(login_url='login')
def upgrade(request):
    return render(request, 'accounts/upgrade.html')


@login_required(login_url='login')
def payment_method(request):
    stripe.api_key = API_KEY
    plan = request.POST.get('plan', 'm')
    automatic = request.POST.get('automatic', 'on')
    payment_method = request.POST.get('payment_method', 'card')
    context = {}

    plan_inst = VideosPlan(plan_id=plan)

    # Instantiating Payment Intent object.
    # It contains temporary secret key which is used for client side JS to render the card
    payment_intent = stripe.PaymentIntent.create(
        amount=plan_inst.amount,
        currency=plan_inst.currency,
        payment_method_types=['card']
    )

    if payment_method == 'card':
        context['secret_key'] = payment_intent.client_secret
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['customer_email'] = request.user.email
        # Payment Intent requires a payment method. Set an existing payment method on the PaymentIntent.
        # So, passing PI to context
        context['payment_intent_id'] = payment_intent.id

        context['automatic'] = automatic
        context['stripe_plan_id'] = plan_inst.stripe_plan_id
        # Now in card.html, create hidden input elements with above 2 values and subscription will work
        return render(request, 'accounts/card.html', context)


# Stripe subscription needs a cutomer/subsciber and plan. Customer/subscriber is a new stripe object, we need to create.
# Plan is a stripe object which has already been created in OG stripe API dashboard.
@login_required(login_url='login')
def card(request):
    stripe.api_key = API_KEY

    # Creating payment. It contains subscription and one time payment.

    # Extracting id's and later passing it to context of payment_method
    payment_intent_id = request.POST['payment_intent_id']
    payment_method_id = request.POST['payment_method_id']

    # Extracting parameters to make subscription work:- stripe_plan_id and automatic
    stripe_plan_id = request.POST['stripe_plan_id']
    automatic = request.POST['automatic']

    if automatic == 'on':
        # Create Subscriptions and customers

        # Create customers
        # Subscriber will be identified by email address and should have assoicated PMobject
        customer = stripe.Customer.create(
            name=request.user.username,
            email=request.user.email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
        # create subscription
        # It shsould be associated with subscriber and plan
        stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    'plan': stripe_plan_id
                },
            ]
        )
        # retrieving latest invoice. It contains payment associated.
        # latest_invoice = stripe.Invoice.retrieve(s.latest_invoice)

        stripe.PaymentIntent.modify(
            payment_intent_id,
            payment_method=payment_method_id,
            customer=customer.id
        )

        '''After creating customer and subscription, stripe automatically creates an invoice and associates latest invoice
        with created subscription and this invoice is open and needs to be paid.
        After subscription is created, we need to extract latest invoice and from that latest invoice we will get a 
        different payment and we need to confirm new payment intent instead of old PI.'''

        # Confirming payment intent
        '''ret = stripe.PaymentIntent.confirm(
            latest_invoice.payment_intent
        )

        # In case of card requiring 3d secure, the return status of npaymemnt intent confirm will be "requires_action".
        # Handling this case by displaying this 3d secure template.
        if ret.status == 'requires_action':
            # payment intent secret/client secret is retrieved from payment intent
            pi = stripe.PaymentIntent.retrieve(  # pi = payment intent
                latest_invoice.payment_intent
            )
            context = {}

            context['payment_intent_secret'] = pi.client_secret
            context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

            return render(request, 'accounts/3dsec.html', context)'''
    else:
        # One time payment.
        # Using stripe API, assoicating PIid with PMid
        stripe.PaymentIntent.modify(
            payment_intent_id,
            payment_method=payment_method_id
        )

    return render(request, 'accounts/thankyou.html')
