from django.urls import path
from . import views

urlpatterns = [
    path('smartbin', views.smartbin, name='smartbin'),
    path('smartbin/link', views.link_bin, name='link_bin'),
    path('smartbin/collect/verify', views.smartbin_collect_verify,name='smartbin_collect_verify'),
    path('smartbin/unlink', views.unlink_bin, name='unlink_bin'),

]
