"""
Configuración de URL para el proyecto CRUD.

La lista `urlpatterns` enruta URLs a vistas (views). Para más información, ver:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Ejemplos:
Vistas basadas en funciones (Function views)
    1. Añadir un import:  from my_app import views
    2. Añadir una URL a urlpatterns:  path('', views.home, name='home')
Vistas basadas en clases (Class-based views)
    1. Añadir un import:  from other_app.views import Home
    2. Añadir una URL a urlpatterns:  path('', Home.as_view(), name='home')
Incluir otra configuración de URLs (URLconf)
    1. Importar la función include(): from django.urls import include, path
    2. Añadir una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario_reposteria.urls')),
]
