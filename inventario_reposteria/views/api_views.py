from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Producto, Lote
from ..serializers import ProductoSerializer, LoteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    # API para gestionar productos
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class LoteViewSet(viewsets.ModelViewSet):
    # API para gestionar lotes
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [IsAuthenticated]
