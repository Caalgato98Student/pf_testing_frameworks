from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from ..models import Producto, Lote

class DashboardView(LoginRequiredMixin, TemplateView):
    # Vista para mostrar el panel de control con estadísticas del inventario
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fecha_limite = timezone.now().date() - timezone.timedelta(days=10)
        
        context['lotes_alerta'] = Lote.objects.filter(
            activo=True,
            producto__activo=True,
            fecha_elaboracion__lt=fecha_limite
        ).count()
        
        context['productos_inventario'] = Producto.objects.filter(activo=True).annotate(
            stock_total=Coalesce(Sum('lote__cantidad_actual', filter=Q(lote__activo=True)), 0)
        ).order_by('nombre')
        
        return context
