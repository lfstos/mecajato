from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name='clientes'),
    path('atualiza_cliente/', views.atualiza_cliente, name='atualiza_cliente'),
]