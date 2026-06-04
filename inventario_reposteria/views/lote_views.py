from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from ..models import Lote
from ..forms import LoteForm

class LotesListView(LoginRequiredMixin, ListView):
    # Vista para listar lotes activos de productos activos
    model = Lote
    template_name = 'lotes/list.html'
    context_object_name = 'lotes'
    
    def get_queryset(self):
        return Lote.objects.filter(activo=True, producto__activo=True).select_related('producto').order_by('-fecha_entrada')

class LoteCreateView(LoginRequiredMixin, CreateView):
    # Vista para crear un nuevo lote
    model = Lote
    form_class = LoteForm
    template_name = 'lotes/form.html'
    success_url = reverse_lazy('lotes_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 'Lote creado exitosamente.')
        return super().form_valid(form)

class LoteUpdateView(LoginRequiredMixin, UpdateView):
    # Vista para editar un lote existente
    model = Lote
    form_class = LoteForm
    template_name = 'lotes/form.html'
    success_url = reverse_lazy('lotes_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        context['lote'] = self.object
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 'Lote actualizado exitosamente.')
        return super().form_valid(form)

class LoteDeleteView(LoginRequiredMixin, View):
    # Vista para desactivar un lote
    
    def get(self, request, pk, *args, **kwargs):
        lote = get_object_or_404(Lote, pk=pk)
        return render(request, 'lotes/delete.html', {'lote': lote})
        
    def post(self, request, pk, *args, **kwargs):
        lote = get_object_or_404(Lote, pk=pk)
        lote.activo = False
        lote.save()
        messages.success(request, 'Lote desactivado exitosamente.')
        return redirect('lotes_list')

class LotesAlertaListView(LoginRequiredMixin, ListView):
    # Vista para mostrar lotes con más de 10 días de productos activos
    model = Lote
    template_name = 'lotes/alerta.html'
    context_object_name = 'lotes_alerta'
    
    def get_queryset(self):
        fecha_limite = timezone.now().date() - timezone.timedelta(days=10)
        return Lote.objects.filter(
            activo=True, 
            producto__activo=True,
            fecha_elaboracion__lt=fecha_limite
        ).select_related('producto').order_by('fecha_elaboracion')

class LotesDesactivadosListView(LoginRequiredMixin, ListView):
    # Vista para mostrar los lotes desactivados
    model = Lote
    template_name = 'lotes/desactivados.html'
    context_object_name = 'lotes'
    
    def get_queryset(self):
        return Lote.objects.filter(activo=False).select_related('producto').order_by('-fecha_entrada')

class LoteReactivarView(LoginRequiredMixin, View):
    # Vista para reactivar un lote desactivado
    
    def get(self, request, pk, *args, **kwargs):
        lote = get_object_or_404(Lote, pk=pk, activo=False)
        context = {
            'lote': lote,
            'producto_activo': lote.producto.activo
        }
        return render(request, 'lotes/reactivar.html', context)
        
    def post(self, request, pk, *args, **kwargs):
        lote = get_object_or_404(Lote, pk=pk, activo=False)
        if not lote.producto.activo:
            messages.error(request, 'No se puede reactivar el lote porque el producto está desactivado.')
            return redirect('lotes_desactivados')
            
        lote.activo = True
        lote.save()
        messages.success(request, 'Lote reactivado exitosamente.')
        return redirect('lotes_list')
