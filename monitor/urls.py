from django.urls import path

from . import views

app_name = 'monitor'

urlpatterns = [
    path('', views.vista_listado, name='listado'),
    path('<int:zona_id>/', views.vista_detalle, name='detalle'),
]