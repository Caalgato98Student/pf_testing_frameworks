from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import Coalesce
from ..models import Producto, Lote

class AjustarInventarioView(LoginRequiredMixin, View):
    # Vista para ajustar el inventario de productos por venta usando lotes FIFO

    def post(self, request, producto_id, accion, *args, **kwargs):
        try:
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            
            if accion == 'decrementar':
                lotes_activos = Lote.objects.filter(
                    producto=producto, 
                    activo=True,
                    cantidad_actual__gt=0
                ).order_by('fecha_elaboracion')
                
                if lotes_activos.exists():
                    lote = lotes_activos.first()
                    if lote.cantidad_actual > 0:
                        lote.cantidad_actual -= 1
                        lote.save()
                        
                        stock_total = Lote.objects.filter(producto=producto, activo=True).aggregate(
                            total=Coalesce(Sum('cantidad_actual'), 0)
                        )['total']
                        
                        return JsonResponse({
                            'success': True,
                            'nuevo_stock': stock_total,
                            'mensaje': f'Se vendió 1 unidad de {producto.nombre}'
                        })
                    else:
                        return JsonResponse({
                            'success': False,
                            'mensaje': 'No hay stock disponible para este producto'
                        })
                else:
                    return JsonResponse({
                        'success': False,
                        'mensaje': 'No hay lotes activos para este producto'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'mensaje': 'Solo se permite decrementar inventario. Para agregar productos, crear un nuevo lote.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Error: {str(e)}'
            })
