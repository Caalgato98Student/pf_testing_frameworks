import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin import AdminSite
from inventario_reposteria.models import Producto, Lote
from inventario_reposteria.admin import ProductoAdmin, LoteAdmin

# Creamos una clase simulada para inicializar las clases de administración de Django
class MockSite:
    pass

@pytest.mark.django_db
def test_creacion_producto_y_model_str():
    """Prueba básica del modelo Producto"""
    producto = Producto.objects.create(
        nombre="Pastel de Chocolate",
        descripcion="Pastel clásico de chocolate belga",
        activo=True
    )
    assert str(producto) == "Pastel de Chocolate"
    assert producto.activo is True


@pytest.mark.django_db
def test_creacion_lote_y_model_str():
    """Prueba básica del modelo Lote"""
    producto = Producto.objects.create(nombre="Galletas")
    fecha_elaboracion = timezone.now().date() - timedelta(days=5)
    lote = Lote.objects.create(
        producto=producto,
        fecha_elaboracion=fecha_elaboracion,
        cantidad_inicial=100,
        cantidad_actual=80,
        activo=True
    )
    assert str(lote) == f"Galletas - {fecha_elaboracion}"
    assert lote.dias_transcurridos() == 5


# ==========================================
# TESTS PARA PRODUCTO_ADMIN
# ==========================================

@pytest.mark.django_db
def test_producto_admin_descripcion_corta():
    producto_admin = ProductoAdmin(Producto, MockSite())
    
    # Caso 1: Sin descripción (debe retornar "-")
    prod_sin_desc = Producto(nombre="A")
    assert producto_admin.descripcion_corta(prod_sin_desc) == "-"
    
    # Caso 2: Descripción corta (<= 50 caracteres)
    prod_desc_corta = Producto(nombre="B", descripcion="Hola mundo")
    assert producto_admin.descripcion_corta(prod_desc_corta) == "Hola mundo"
    
    # Caso 3: Descripción larga (> 50 caracteres)
    desc_larga = "Esta es una descripcion extremadamente larga diseñada para superar los cincuenta caracteres."
    prod_desc_larga = Producto(nombre="C", descripcion=desc_larga)
    resultado = producto_admin.descripcion_corta(prod_desc_larga)
    assert resultado.endswith("...")
    assert len(resultado) == 53 # 50 caracteres + 3 puntos suspensivos


@pytest.mark.django_db
def test_producto_admin_get_stock_total_y_lotes_count():
    producto_admin = ProductoAdmin(Producto, MockSite())
    producto = Producto.objects.create(nombre="Muffin")
    
    # Caso sin stock y sin lotes activos
    assert "Sin stock" in producto_admin.get_stock_total(producto)
    assert "0 lotes" in producto_admin.get_lotes_count(producto)
    
    # Agregamos lotes activos
    Lote.objects.create(producto=producto, cantidad_inicial=50, cantidad_actual=30, activo=True)
    Lote.objects.create(producto=producto, cantidad_inicial=50, cantidad_actual=20, activo=True)
    # Lote inactivo (no debería sumarse)
    Lote.objects.create(producto=producto, cantidad_inicial=50, cantidad_actual=10, activo=False)
    
    assert "50 unidades" in producto_admin.get_stock_total(producto)
    assert "color: green" in producto_admin.get_stock_total(producto)
    assert "2 lotes" in producto_admin.get_lotes_count(producto)


@pytest.mark.django_db
def test_producto_admin_estado_display():
    producto_admin = ProductoAdmin(Producto, MockSite())
    
    prod_activo = Producto(activo=True)
    assert "✓ Activo" in producto_admin.estado_display(prod_activo)
    assert "color: green" in producto_admin.estado_display(prod_activo)
    
    prod_inactivo = Producto(activo=False)
    assert "✗ Inactivo" in producto_admin.estado_display(prod_inactivo)
    assert "color: red" in producto_admin.estado_display(prod_inactivo)


# ==========================================
# TESTS PARA LOTE_ADMIN
# ==========================================

@pytest.mark.django_db
def test_lote_admin_estado_cantidad():
    lote_admin = LoteAdmin(Lote, MockSite())
    producto = Producto.objects.create(nombre="Base")
    
    # Caso 1: Agotado (cantidad_actual <= 0)
    lote_agotado = Lote(producto=producto, cantidad_inicial=100, cantidad_actual=0)
    assert "Agotado" in lote_admin.estado_cantidad(lote_agotado)
    assert "color: red" in lote_admin.estado_cantidad(lote_agotado)
    
    # Caso 2: Bajo (< 30% del inicial)
    lote_bajo = Lote(producto=producto, cantidad_inicial=100, cantidad_actual=29)
    assert "Bajo" in lote_admin.estado_cantidad(lote_bajo)
    assert "color: orange" in lote_admin.estado_cantidad(lote_bajo)
    
    # Caso 3: Normal (>= 30% del inicial)
    lote_normal = Lote(producto=producto, cantidad_inicial=100, cantidad_actual=30)
    assert "Normal" in lote_admin.estado_cantidad(lote_normal)
    assert "color: green" in lote_admin.estado_cantidad(lote_normal)


@pytest.mark.django_db
def test_lote_admin_dias_transcurridos_display():
    lote_admin = LoteAdmin(Lote, MockSite())
    producto = Producto.objects.create(nombre="Base")
    hoy = timezone.now().date()
    
    # Caso 1: Más de 15 días (Rojo con emoji ⚠️)
    lote_critico = Lote.objects.create(producto=producto, fecha_elaboracion=hoy - timedelta(days=16), cantidad_inicial=10, cantidad_actual=10)
    res_critico = lote_admin.dias_transcurridos_display(lote_critico)
    assert "16 días" in res_critico
    assert "color: red" in res_critico
    
    # Caso 2: Más de 10 días y hasta 15 días (Naranja con emoji ⚡)
    lote_alerta = Lote.objects.create(producto=producto, fecha_elaboracion=hoy - timedelta(days=11), cantidad_inicial=10, cantidad_actual=10)
    res_alerta = lote_admin.dias_transcurridos_display(lote_alerta)
    assert "11 días" in res_alerta
    assert "color: orange" in res_alerta
    
    # Caso 3: 10 días o menos (Verde común)
    lote_bien = Lote.objects.create(producto=producto, fecha_elaboracion=hoy - timedelta(days=5), cantidad_inicial=10, cantidad_actual=10)
    res_bien = lote_admin.dias_transcurridos_display(lote_bien)
    assert "5 días" in res_bien
    assert "color: green" in res_bien


@pytest.mark.django_db
def test_lote_admin_estado_display():
    lote_admin = LoteAdmin(Lote, MockSite())
    
    lote_activo = Lote(activo=True)
    assert "✓ Activo" in lote_admin.estado_display(lote_activo)
    
    lote_inactivo = Lote(activo=False)
    assert "✗ Inactivo" in lote_admin.estado_display(lote_inactivo)