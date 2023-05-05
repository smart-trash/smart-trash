from django.urls import path
from . import views

urlpatterns = [
    path('booking/create', views.booking_create, name='booking_create'),
    path('booking/manual', views.manual_booking, name='manual_booking'),
    path('list/task', views.list_booking, name='list_booking'),
    path('navigate/<int:location_id>/', views.navigate_view, name='navigate'),
    path('booking/detailed_view/<int:booking_id>', views.detailed_view, name='detailed_view'),
    path('booking/view-history', views.booking_history, name='booking_history'),
    path('collect', views.collect, name='collect'),
]