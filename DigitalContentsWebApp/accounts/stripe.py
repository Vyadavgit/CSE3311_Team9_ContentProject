import stripe
from .models import Customer
from .views import *

from django.conf import settings

MONTH = 'm'
ANNUAL = 'a'

API_KEY = settings.STRIPE_SECRET_KEY


class VideosMonthPlan:
    def __init__(self):
        self.stripe_plan_id = settings.STRIPE_PLAN_MONTHLY_ID
        self.amount = 1000 #equivalent to $10


class VideosAnnualPlan:
    def __init__(self):
        self.stripe_plan_id = settings.STRIPE_PLAN_ANNUAL_ID
        self.amount = 12000 #equivalent to $120


class VideosPlan:
    def __init__(self, plan_id):
        """
        plan_id is either string 'm' (stands for monthly)
        or a string letter 'a' (which stands for annual)
        """
        if plan_id == MONTH:
            self.plan = VideosMonthPlan()
            self.id = MONTH
        elif plan_id == ANNUAL:
            self.plan = VideosAnnualPlan()
            self.id = ANNUAL
        else:
            raise ValueError('Invalid plan_id value')

        self.currency = 'usd'

    @property
    def stripe_plan_id(self):
        return self.plan.stripe_plan_id

    @property
    def amount(self):
        return self.plan.amount












def set_paid_until(charge):

    stripe.api_key = API_KEY
    #retrieving payment intent
    pi = stripe.PaymentIntent.retrieve(charge.payment_intent)

    if pi.customer:
        #is customer exists, retrieve.
        customer = stripe.Customer.retrieve(pi.customer)
        email = customer.email
        #from customer, extract subscription object which contains a field called "current_period_end.
        if customer:
            subscriptions = stripe.Subscription.retrieve(
                customer['subscriptions'].data[0].id
            )
            current_period_end = subscriptions['current_period_end']

        #From email field from above, we get associated user from our Customer model
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return False
        #If user found, update paid until field using set_paid_until method
        user.set_paid_until(current_period_end)
    else:
        pass
        #if there is no stripe customer object, it means user did a single payment

        # charge.amount  1000 | 12000
        # this was one time payment, update
        # paid_until (e.g. paid_until = current_date + 31 days) using
        # charge.paid + charge.amount attrs