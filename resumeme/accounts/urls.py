from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('subscription/', views.subscription_view, name='subscription'),
    path('settings/', views.settings_view, name='settings'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('settings/', views.update_settings, name='update_settings'),

]