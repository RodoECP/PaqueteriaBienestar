from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('paquetes.urls')),  # Todas las rutas de paquetes gestionadas aquí
]
