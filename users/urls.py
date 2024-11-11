from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('cuenta/', views.cuenta_view, name='cuenta'),
    path('login/', views.login_view, name='login')
]