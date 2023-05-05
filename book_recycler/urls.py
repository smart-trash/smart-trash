from django.urls import path
from . import views

urlpatterns = [
    path('recycler/booking/create', views.recycler_booking, name='recycler_booking'),
    path('recycler/booking-recycler', views.list_recycler_booking, name='list_recycler_booking'),
    path('recycler_booking/detailed_view/<int:recycler_booking_id>', views.recycler_booking_detailed_view, name='recycler_booking_detailed_view'),
    path('recycler/collect/<int:recycler_booking_id>', views.recycler_collect, name='recycler_collect'),
    path('recycler/verify/<int:recycler_booking_id>', views.recycler_verify, name='recycler_verify'),
    path('recycler/booking-history', views.recycler_history, name='recycler_history'),


]