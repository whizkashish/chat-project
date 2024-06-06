import stripe
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from core.models import Membership, MembershipPayment
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def membership_view(request):
    context = {
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'membership/membership.html', context)

@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=request.user.email,
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Pro Membership',
                            },
                            'unit_amount': 1000,
                            'recurring': {
                                'interval': 'month',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=domain_url + 'membership/success/',
                cancel_url=domain_url + 'membership/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })

@login_required
def membership_success(request):
    return render(request, 'membership/membership_success.html')

@login_required
def membership_cancel(request):
    return render(request, 'membership/membership_cancel.html')

@login_required
def upgrade_membership(request):
    if request.method == 'POST':
        try:
            user_membership = Membership.objects.get(user=request.user)
            current_subscription = stripe.Subscription.retrieve(user_membership.stripe_subscription_id)
            new_price_id = 'price_1POfJoAVy2I36xvX8TQmBo9N'  # Replace with your Premium price ID

            updated_subscription = stripe.Subscription.modify(
                current_subscription.id,
                cancel_at_period_end=False,
                proration_behavior='always_invoice',
                items=[{
                    'id': current_subscription['items']['data'][0].id,
                    'price': new_price_id,
                }],
            )

            user_membership.membership_type = 'Premium'
            user_membership.save()

            return JsonResponse({'status': 'success'})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Membership.DoesNotExist:
            return JsonResponse({'error': 'Membership not found'}, status=404)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_email']
        stripe_customer_id = session['customer']
        stripe_subscription_id = session['subscription']
        user = User.objects.get(email=customer_email)
        membership, created = Membership.objects.get_or_create(user=user)
        membership.stripe_customer_id = stripe_customer_id
        membership.stripe_subscription_id = stripe_subscription_id
        membership.membership_type = 'Pro'
        membership.start_date = timezone.now()
        membership.end_date = timezone.now() + timedelta(days=30)
        membership.save()
    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        amount = invoice['total'] / 100
        subscription = invoice['subscription']
        membership = Membership.objects.filter(stripe_subscription_id=subscription).first()
        if membership:
            membership_payment = MembershipPayment.objects.create(membership=membership, amount=amount)
        else:
            invoice = session = event['data']['object']
            customer_email = session['customer_email']
            stripe_customer_id = session['customer']
            stripe_subscription_id = session['subscription']
            user = User.objects.get(email=customer_email)
            membership, created = Membership.objects.get_or_create(user=user)
            membership.stripe_customer_id = stripe_customer_id
            membership.stripe_subscription_id = stripe_subscription_id
            membership.membership_type = 'Pro'
            membership.start_date = timezone.now()
            membership.end_date = timezone.now() + timedelta(days=30)
            membership.save()
            amount = invoice['total'] / 100
            membership_payment = MembershipPayment.objects.create(membership=membership, amount=amount)
       
    return JsonResponse({'status': 'success'})