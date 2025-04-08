from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.plan_selection, name='plan_selection'),
    path('payment/', views.payment, name='payment'),
    path('success/', views.subscription_success, name='success'),
    path('cancel/', views.subscription_cancel, name='cancel'),
    path('details/', views.subscription_details, name='details'),
]