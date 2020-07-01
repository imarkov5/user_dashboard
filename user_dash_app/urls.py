from django.urls import path
from . import views

urlpatterns = [
    path('new_user', views.new_user),
    path('admin', views.admin),
    path('user_info', views.user_info),
]