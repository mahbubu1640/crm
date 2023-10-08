# crm_app/urls.py
from django.urls import path
from . import views
app_name = 'crm_app'

urlpatterns = [
    #path('register/', views.register_user, name='register'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('create_dynamic_field/', views.create_dynamic_field, name='create_dynamic_field'),
    path('edit_dynamic_field/<int:field_id>/', views.edit_dynamic_field, name='edit_dynamic_field'),
    path('delete_dynamic_field/<int:field_id>/', views.delete_dynamic_field, name='delete_dynamic_field'),
    # Add more URL patterns as needed
]


