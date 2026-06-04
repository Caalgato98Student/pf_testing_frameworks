from django import forms
from django.utils import timezone
from django.db.models import Q
from .models import Producto, Lote

class ProductoForm(forms.ModelForm):
    """Crear y editar productos"""
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto',
                'rows': 3
            })
        }

class LoteForm(forms.ModelForm):
    """Crear y editar lotes con validación de cantidades"""
    class Meta:
        model = Lote
        fields = ['producto', 'fecha_elaboracion', 'cantidad_inicial', 'cantidad_actual']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_elaboracion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cantidad_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Cantidad inicial'
            }),
            'cantidad_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Cantidad actual'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar el dropdown de productos
        if self.instance and self.instance.pk:
            # En edición: permitir productos activos o el producto actual del lote (incluso si está inactivo)
            self.fields['producto'].queryset = Producto.objects.filter(
                Q(activo=True) | Q(id=self.instance.producto_id)
            )
        else:
            # En creación: solo productos activos
            self.fields['producto'].queryset = Producto.objects.filter(activo=True)
            # En creación, cantidad_actual es opcional; si se omite, se igualará a cantidad_inicial
            self.fields['cantidad_actual'].required = False
            self.fields['cantidad_actual'].widget.attrs['placeholder'] = 'Cantidad actual (dejar en blanco para igualar a inicial)'

    def clean_fecha_elaboracion(self):
        fecha = self.cleaned_data.get('fecha_elaboracion')
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError('La fecha de elaboración no puede ser una fecha futura.')
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        cantidad_inicial = cleaned_data.get('cantidad_inicial')
        cantidad_actual = cleaned_data.get('cantidad_actual')
        
        # Validar cantidad_inicial mínima programáticamente
        if cantidad_inicial is not None and cantidad_inicial < 1:
            self.add_error('cantidad_inicial', 'La cantidad inicial debe ser al menos 1.')

        # Si es creación y cantidad_actual no se proporciona, igualarla a cantidad_inicial
        if cantidad_actual is None and cantidad_inicial is not None:
            cantidad_actual = cantidad_inicial
            cleaned_data['cantidad_actual'] = cantidad_actual
            
            # Si el modelo tiene la instancia asociada, también la actualizamos
            if self.instance:
                self.instance.cantidad_actual = cantidad_actual

        if cantidad_actual is not None and cantidad_actual < 0:
            self.add_error('cantidad_actual', 'La cantidad actual no puede ser menor a 0.')

        # Validar que cantidad_actual <= cantidad_inicial
        if cantidad_inicial is not None and cantidad_actual is not None:
            if cantidad_actual > cantidad_inicial:
                raise forms.ValidationError('La cantidad actual no puede ser mayor a la cantidad inicial.')
        
        return cleaned_data