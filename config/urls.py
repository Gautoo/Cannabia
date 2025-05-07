# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cultivo/', include('gestion_cultivo.urls')), # Las URLs de tu app
    path('cuentas/', include('django.contrib.auth.urls')), # URLs de autenticación de Django (login, logout, etc.)
    # Esta línea anterior añade URLs como:
    # cuentas/login/
    # cuentas/logout/
    # cuentas/password_change/
    # ... y otras.
]