from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Other URL patterns...
    path('discipleship/series/<slug:slug>/', views.track_detail, name='track_detail'),
    path('discipleship/series/<slug:slug>/add-note/', views.add_track_note, name='add_track_note'),
    # Add other URL patterns as needed
]

