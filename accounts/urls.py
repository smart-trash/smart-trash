from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/change_password', views.change_password, name='change_password'),
    path('add-location', views.add_location, name='add_location'),

    path('list/customer', views.list_customer, name='list_customer'),
    path('customer/add', views.add_customer, name='add_customer'),
    path('customer/remove/<int:user_id>', views.remove_customer, name='remove_customer'),
    path('customer/change-status/<int:user_id>',views.change_status_customer,name="change_status_customer"),


    path('list/collection-agent', views.list_agent, name='list_agent'),
    path('collection-agent/add', views.add_agent, name='add_agent'),
    path('collection-agent/remove/<int:user_id>', views.remove_agent, name='remove_agent'),
    path('collection-agent/change-status/<int:user_id>',views.change_status_agent,name="change_status_agent"),

    path('list/municipalities', views.list_municipalities, name='list_municipalities'),
    path('add/municipality', views.add_municipalities, name='add_municipalities'),
    path('remove/municipality<int:user_id>', views.remove_municipalities, name='remove_municipalities'),
    path('change-status/municipality/<int:user_id>',views.change_status_municipalities,name="change_status_municipalities"),

    path('list/recyclers', views.list_recyclers, name='list_recyclers'),
    path('recyclers/add', views.add_recyclers, name='add_recycler'),
    path('recyclers/remove/<int:user_id>', views.remove_recycler, name='remove_recycler'),
    path('recyclers/change-status/<int:user_id>',views.change_status_recycler,name="change_status_recycler"),


]