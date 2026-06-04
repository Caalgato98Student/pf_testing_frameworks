from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Registro de rutas de la API REST
router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='api_producto')
router.register(r'lotes', views.LoteViewSet, basename='api_lote')

urlpatterns = [
    # Panel de control
    path('', views.DashboardView.as_view(), name='index'),
    
    # Autenticación
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # CRUD productos
    path('productos/', views.ProductosListView.as_view(), name='productos_list'),
    path('productos/crear/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_edit'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    
    # Productos desactivados
    path('productos/desactivados/', views.ProductosDesactivadosListView.as_view(), name='productos_desactivados'),
    path('productos/<int:pk>/reactivar/', views.ProductoReactivarView.as_view(), name='producto_reactivar'),
    
    # CRUD lotes
    path('lotes/', views.LotesListView.as_view(), name='lotes_list'),
    path('lotes/crear/', views.LoteCreateView.as_view(), name='lote_create'),
    path('lotes/<int:pk>/editar/', views.LoteUpdateView.as_view(), name='lote_edit'),
    path('lotes/<int:pk>/eliminar/', views.LoteDeleteView.as_view(), name='lote_delete'),
    path('lotes/alerta/', views.LotesAlertaListView.as_view(), name='lotes_alerta'),
    
    # Lotes desactivados
    path('lotes/desactivados/', views.LotesDesactivadosListView.as_view(), name='lotes_desactivados'),
    path('lotes/<int:pk>/reactivar/', views.LoteReactivarView.as_view(), name='lote_reactivar'),
    
    # Manejo de inventario
    path('inventario/<int:producto_id>/<str:accion>/', views.AjustarInventarioView.as_view(), name='ajustar_inventario'),
    
    # Rutas de la API REST
    path('api/', include(router.urls)),
]