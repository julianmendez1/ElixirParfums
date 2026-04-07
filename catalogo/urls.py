from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_list, name='catalogo_list'),
    path('perfume/<int:pk>/', views.perfume_detalle, name='perfume_detalle'),
]
