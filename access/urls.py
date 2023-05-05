from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us', views.contact_us, name='contact_us'),

    path('customer', views.customer, name='customer'),
    path('customer/login', views.customer_login, name='customer_login'),

    path('agent', views.agent, name='agent'),
    path('agent/login', views.agent_login, name='agent_login'),

    path('municipality', views.municipality, name='municipality'),
    path('municipality/login', views.municipality_login, name='municipality_login'),

    path('recycler', views.recycler, name='recycler'),
    path('recycler/login', views.recycler_login, name='recycler_login'),

    path('admin/', views.admin, name='admin'),
    path('admin/login', views.admin_login, name='admin_login'),

    path('customer/signup', views.customer_signup, name='customer_signup'),
    path('agent/signup', views.agent_signup, name='agent_signup'),
    # path('recycler/signup', views.recycler_signup, name='recycler_signup'),

    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:reset_id>', views.reset_password, name='reset_password'),
    path('logout', views.logout, name='logout'),
]
