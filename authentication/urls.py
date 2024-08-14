from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_authentication, name='check_auth'),
    path('register/', views.signup, name= 'register'),
    path('login/', views.signin, name= 'login'),
    path('logout/', views.logout, name='logout'),

]