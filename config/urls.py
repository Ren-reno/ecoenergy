from django.contrib import admin
from django.urls import include, path

from monitor.views import vista_resumen_zonas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('zonas/', include('monitor.urls')),
    path('resumen-zonas/', vista_resumen_zonas, name='resumen_zonas'),
]