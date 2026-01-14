from django.urls import path
from . import views

urlpatterns = [
    path('', views.mailer_list, name='mailer_list'),
    path('create/', views.mailer_create, name='mailer_create')
]
