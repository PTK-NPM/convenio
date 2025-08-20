from  django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginv, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('autorizacao', views.autorizacao, name='autorizacao')
]
