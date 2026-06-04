from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from ..models import Producto, Lote
from ..forms import ProductoForm

class ProductosListView(LoginRequiredMixin, ListView):
    # Vista para listar productos activos con stock calculado
    model = Producto
    template_name = 'productos/list.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        return Producto.objects.filter(activo=True).annotate(
            stock_total=Coalesce(Sum('lote__cantidad_actual', filter=Q(lote__activo=True)), 0),
            lotes_activos=Count('lote', filter=Q(lote__activo=True))
        )

class ProductoCreateView(LoginRequiredMixin, CreateView):
    # Vista para crear un nuevo producto
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/form.html'
    success_url = reverse_lazy('productos_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 'Producto creado exitosamente.')
        return super().form_valid(form)

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    # Vista para editar un producto activo
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/form.html'
    success_url = reverse_lazy('productos_list')
    
    def get_queryset(self):
        return Producto.objects.filter(activo=True)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        context['producto'] = self.object
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return super().form_valid(form)

class ProductoDeleteView(LoginRequiredMixin, View):
    # Vista para desactivar un producto y sus lotes asociados
    
    def get(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk, activo=True)
        lotes_activos = Lote.objects.filter(producto=producto, activo=True).count()
        context = {
            'producto': producto,
            'lotes_activos': lotes_activos
        }
        return render(request, 'productos/delete.html', context)
        
    def post(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk, activo=True)
        producto.activo = False
        producto.save()
        
        lotes_desactivados = Lote.objects.filter(producto=producto, activo=True).update(activo=False)
        
        mensaje = f'Producto "{producto.nombre}" desactivado exitosamente.'
        if lotes_desactivados > 0:
            mensaje += f' También se desactivaron {lotes_desactivados} lote(s) asociado(s).'
            
        messages.success(request, mensaje)
        return redirect('productos_list')

class ProductosDesactivadosListView(LoginRequiredMixin, ListView):
    # Vista para mostrar los productos desactivados
    model = Producto
    template_name = 'productos/desactivados.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        return Producto.objects.filter(activo=False).annotate(
            total_lotes=Count('lote'),
            lotes_activos_count=Count('lote', filter=Q(lote__activo=True))
        ).order_by('-id')

class ProductoReactivarView(LoginRequiredMixin, View):
    # Vista para reactivar un producto desactivado
    
    def get(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk, activo=False)
        lotes_count = Lote.objects.filter(producto=producto).count()
        lotes_desactivados = Lote.objects.filter(producto=producto, activo=False).count()
        context = {
            'producto': producto,
            'lotes_count': lotes_count,
            'lotes_desactivados': lotes_desactivados
        }
        return render(request, 'productos/reactivar.html', context)
        
    def post(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk, activo=False)
        producto.activo = True
        producto.save()
        messages.success(request, f'Producto "{producto.nombre}" reactivado exitosamente.')
        return redirect('productos_list')
