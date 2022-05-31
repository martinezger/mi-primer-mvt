from django.urls import path
from familia import views


urlpatterns = [
    path('', views.index, name="index"),
    path('agregar/', views.agregar, name="agregar"),
    path('borrar/<identificador>', views.borrar, name="borrar"),
    path('actualizar/', views.actualizar, name="actualizar_action"),
    path('actualizar/<identificador>', views.actualizar, name="actualizar"),
    path('buscar/', views.buscar, name="buscar"),
]
