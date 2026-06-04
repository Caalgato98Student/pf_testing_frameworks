from django.contrib import admin
from django.utils.html import format_html
from .models import Producto, Lote


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion_corta', 'get_stock_total', 'get_lotes_count', 'activo', 'estado_display']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']
    list_per_page = 20
    ordering = ['nombre']
    
    def descripcion_corta(self, obj):
        """Muestra descripción"""
        if obj.descripcion:
            return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
        return "-"
    descripcion_corta.short_description = "Descripción"
    
    def get_stock_total(self, obj):
        """Calcula y muestra el stock total del producto"""
        stock = sum(lote.cantidad_actual for lote in obj.lote_set.filter(activo=True))
        if stock > 0:
            return format_html('<span style="color: green; font-weight: bold;">{} unidades</span>', stock)
        else:
            return format_html('<span style="color: red;">Sin stock</span>')
    get_stock_total.short_description = "Stock Total"
    
    def get_lotes_count(self, obj):
        """Cuenta los lotes activos del producto"""
        count = obj.lote_set.filter(activo=True).count()
        return f"{count} lotes"
    get_lotes_count.short_description = "Lotes activos"
    
    def estado_display(self, obj):
        """Muestra el estado con colores"""
        if obj.activo:
            return format_html('<span style="color: green; font-weight: bold;">✓ Activo</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Inactivo</span>')
    estado_display.short_description = "Estado"


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad_inicial', 'cantidad_actual', 'estado_cantidad', 
                   'fecha_elaboracion', 'dias_transcurridos_display', 'estado_display']
    list_filter = ['activo', 'fecha_elaboracion', 'producto']
    search_fields = ['producto__nombre']
    list_editable = ['cantidad_actual']
    date_hierarchy = 'fecha_elaboracion'
    list_per_page = 25
    ordering = ['-fecha_elaboracion']
    
    def estado_cantidad(self, obj):
        """Muestra el estado de la cantidad con colores"""
        if obj.cantidad_actual <= 0:
            return format_html('<span style="color: red; font-weight: bold;">Agotado</span>')
        elif obj.cantidad_actual < obj.cantidad_inicial * 0.3:
            return format_html('<span style="color: orange; font-weight: bold;">Bajo</span>')
        else:
            return format_html('<span style="color: green; font-weight: bold;">Normal</span>')
    estado_cantidad.short_description = "Estado stock"

    def dias_transcurridos_display(self, obj):
        """Muestra días transcurridos con colores según el tiempo"""
        dias = obj.dias_transcurridos()
        if dias > 15:
            return format_html('<span style="color: red; font-weight: bold; background-color: #ffebee; padding: 2px 6px; border-radius: 3px;">⚠️ {} días</span>', dias)
        elif dias > 10:
            return format_html('<span style="color: orange; font-weight: bold; background-color: #fff3e0; padding: 2px 6px; border-radius: 3px;">⚡ {} días</span>', dias)
        else:
            return format_html('<span style="color: green; font-weight: bold;">{} días</span>', dias)
    dias_transcurridos_display.short_description = "Días transcurridos"
    
    def estado_display(self, obj):
        """Muestra el estado con colores"""
        if obj.activo:
            return format_html('<span style="color: green; font-weight: bold;">✓ Activo</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Inactivo</span>')
    estado_display.short_description = "Estado"


admin.site.site_header = "Administración"
admin.site.site_title = "Panel de control"
admin.site.index_title = "Gestión de inventario"
