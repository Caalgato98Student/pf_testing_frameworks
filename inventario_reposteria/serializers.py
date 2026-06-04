from rest_framework import serializers
from .models import Producto, Lote

class ProductoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Producto
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'activo']

class LoteSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Lote
    dias_transcurridos = serializers.ReadOnlyField()

    class Meta:
        model = Lote
        fields = [
            'id', 'producto', 'fecha_elaboracion', 'fecha_entrada',
            'cantidad_inicial', 'cantidad_actual', 'activo', 'dias_transcurridos'
        ]
