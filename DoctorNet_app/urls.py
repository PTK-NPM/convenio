from  django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginv, name='home'),
    path('login', views.loginv, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('autorizacao', views.sol_autorizacao, name='autorizacao'),
    path('autorizacao/<int:id>', views.detalhes_autorizada, name='detalhes_autorizada')
]
