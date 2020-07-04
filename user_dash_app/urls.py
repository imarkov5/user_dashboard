from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path('new_user', views.new_user),
    path('admin', views.admin),
    path('user_info', views.user_info),
    path('profile', views.profile),
    path('<int:user_id>/edit_user', views.edit_user),
    path('<int:user_id>/delete_user', views.delete_user),
    path('update_password', views.update_password),
    path('profile_password', views.profile_password),
    path('description', views.edit_description)
]