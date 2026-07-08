from django.urls import path
from . import views

urlpatterns = [
    path('ingreso/', views.ingreso_inventario, name='ingreso_inventario'),
    path('salida/', views.salida_inventario, name='salida_inventario'),
]