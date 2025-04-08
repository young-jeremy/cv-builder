from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from templates_app.models import ResumeTemplate

from .models import Plan, Subscription, Payment
from .forms import PlanSelectionForm, PaymentForm

import stripe
import json

from resume.forms import ResumeExportForm

# Initialize Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


class ResumeExport:
    pass


@login_required
def export_resume(request, slug):
    resume = get_object_or_404(ResumeTemplate, slug=slug, user=request.user)

    # Check if user has an active subscription that allows exports
    has_export_permission = False
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if active_subscription and active_subscription.plan.allow_resume_export:
        has_export_permission = True

    if not has_export_permission:
        # Store the resume slug in session for redirect after payment
        request.session['export_resume_slug'] = slug
        messages.warning(request, 'You need a subscription to export your resume. Please choose a plan.')
        return redirect('subscription:plan_selection')

    if request.method == 'POST':
        form = ResumeExportForm(request.POST)
        if form.is_valid():
            format_type = form.cleaned_data['format']

            # Here you would implement the actual export logic
            # For now, we'll just create a placeholder export record
            export = ResumeExport.objects.create(
                resume=resume,
                format=format_type,
                # In a real implementation, you would generate the file here
                # file=generated_file
            )

            messages.success(request, f'Resume exported as {format_type.upper()} successfully!')

            # In a real implementation, you would return the file for download
            # return redirect(export.file.url)
            return redirect('resume:detail', slug=resume.slug)

    return redirect('resume:detail', slug=resume.slug)


@login_required
def plan_selection(request):
    """View for selecting a subscription plan"""
    # Check if user already has an active subscription
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if request.method == 'POST':
        form = PlanSelectionForm(request.POST)
        if form.is_valid():
            selected_plan = form.cleaned_data['plan']
            # Store the selected plan ID in session for the payment step
            request.session['selected_plan_id'] = selected_plan.id
            return redirect('subscription:payment')
    else:
        form = PlanSelectionForm()

    plans = Plan.objects.filter(is_active=True)
    return render(request, 'payments/subscription/plan_selection.html', {
        'form': form,
        'plans': plans,
        'active_subscription': active_subscription,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def payment(request):
    """View for processing payment"""
    # Get the selected plan from session
    plan_id = request.session.get('selected_plan_id')
    if not plan_id:
        messages.error(request, 'Please select a plan first.')
        return redirect('subscription:plan_selection')

    plan = get_object_or_404(Plan, id=plan_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                # Create a Stripe token (in a real implementation, this would be done client-side)
                # This is just for demonstration purposes
                token = request.POST.get('stripeToken')

                if not token:
                    messages.error(request, 'Payment processing failed. Please try again.')
                    return redirect('subscription:payment')

                # Create a charge or subscription in Stripe
                if plan.billing_cycle == 'one_time':
                    # One-time payment
                    charge = stripe.Charge.create(
                        amount=int(plan.price * 100),  # Amount in cents
                        currency='usd',
                        description=f"{plan.name} Plan",
                        source=token,
                        metadata={'user_id': request.user.id}
                    )

                    # Create subscription with end date based on plan
                    if plan.billing_cycle == 'monthly':
                        end_date = timezone.now() + timezone.timedelta(days=30)
                    elif plan.billing_cycle == 'yearly':
                        end_date = timezone.now() + timezone.timedelta(days=365)
                    else:  # one_time
                        end_date = None

                    # Create subscription record
                    subscription = Subscription.objects.create(
                        user=request.user,
                        plan=plan,
                        status='active',
                        start_date=timezone.now(),
                        end_date=end_date,
                        payment_id=charge.id
                    )

                    # Create payment record
                    Payment.objects.create(
                        user=request.user,
                        subscription=subscription,
                        amount=plan.price,
                        payment_method='credit_card',
                        transaction_id=charge.id,
                        status='completed'
                    )

                    messages.success(request, f'Payment successful! You now have access to the {plan.name} plan.')

                    # Redirect to the resume list or the specific resume they were trying to export
                    resume_slug = request.session.get('export_resume_slug')
                    if resume_slug:
                        del request.session['export_resume_slug']
                        return redirect('resume:export_resume', slug=resume_slug)
                    else:
                        return redirect('resume:list')

                else:
                    # Subscription payment (monthly/yearly)
                    # Create a customer in Stripe
                    customer = stripe.Customer.create(
                        email=request.user.email,
                        source=token
                    )

                    # Create a subscription plan in Stripe
                    interval = 'month' if plan.billing_cycle == 'monthly' else 'year'
                    stripe_plan = stripe.Plan.create(
                        amount=int(plan.price * 100),
                        currency='usd',
                        interval=interval,
                        product={'name': plan.name},
                        nickname=f"{plan.name} {plan.billing_cycle}"
                    )

                    # Subscribe the customer to the plan
                    stripe_subscription = stripe.Subscription.create(
                        customer=customer.id,
                        items=[{'plan': stripe_plan.id}]
                    )

                    # Calculate end date based on billing cycle
                    if plan.billing_cycle == 'monthly':
                        end_date = timezone.now() + timezone.timedelta(days=30)
                    else:  # yearly
                        end_date = timezone.now() + timezone.timedelta(days=365)

                    # Create subscription record
                    subscription = Subscription.objects.create(
                        user=request.user,
                        plan=plan,
                        status='active',
                        start_date=timezone.now(),
                        end_date=end_date,
                        payment_id=stripe_subscription.latest_invoice.payment_intent.id,
                        subscription_id=stripe_subscription.id
                    )

                    # Create payment record
                    Payment.objects.create(
                        user=request.user,
                        subscription=subscription,
                        amount=plan.price,
                        payment_method='credit_card',
                        transaction_id=stripe_subscription.latest_invoice.payment_intent.id,
                        status='completed'
                    )

                    messages.success(request, f'Subscription successful! You now have access to the {plan.name} plan.')

                    # Redirect to the resume list or the specific resume they were trying to export
                    resume_slug = request.session.get('export_resume_slug')
                    if resume_slug:
                        del request.session['export_resume_slug']
                        return redirect('resume:export_resume', slug=resume_slug)
                    else:
                        return redirect('resume:list')

            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                messages.error(request, f"Card error: {e.error.message}")
            except stripe.error.RateLimitError:
                # Too many requests made to the API too quickly
                messages.error(request, "Rate limit error")
            except stripe.error.InvalidRequestError:
                # Invalid parameters were supplied to Stripe's API
                messages.error(request, "Invalid parameters")
            except stripe.error.AuthenticationError:
                # Authentication with Stripe's API failed
                messages.error(request, "Authentication failed")
            except stripe.error.APIConnectionError:
                # Network communication with Stripe failed
                messages.error(request, "Network error")
            except stripe.error.StripeError:
                # Display a very generic error to the user
                messages.error(request, "Something went wrong. You were not charged.")
            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = PaymentForm()

    return render(request, 'payments/subscription/payment.html', {
        'form': form,
        'plan': plan,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def subscription_success(request):
    """View for successful subscription"""
    return render(request, 'payments/subscription/success.html')


@login_required
def subscription_cancel(request):
    """View for canceling a subscription"""
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active'
    ).first()

    if not active_subscription:
        messages.error(request, 'You do not have an active subscription to cancel.')
        return redirect('subscription:plan_selection')

    if request.method == 'POST':
        try:
            # Cancel the subscription in Stripe if it's a recurring subscription
            if active_subscription.subscription_id:
                stripe.Subscription.delete(active_subscription.subscription_id)

            # Update the subscription status in our database
            active_subscription.status = 'canceled'
            active_subscription.save()

            messages.success(request, 'Your subscription has been canceled successfully.')
            return redirect('resume:list')

        except Exception as e:
            messages.error(request, f"An error occurred while canceling your subscription: {str(e)}")

    return render(request, 'payments/subscription/cancel.html', {
        'subscription': active_subscription
    })


@login_required
def subscription_details(request):
    """View for showing subscription details"""
    subscriptions = Subscription.objects.filter(user=request.user).order_by('-start_date')
    active_subscription = subscriptions.filter(status='active').first()

    return render(request, 'payments/subscription/details.html', {
        'subscriptions': subscriptions,
        'active_subscription': active_subscription
    })