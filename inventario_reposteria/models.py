from django.db import models
from django.utils import timezone


class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    fecha_elaboracion = models.DateField()
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    cantidad_inicial = models.PositiveIntegerField()
    cantidad_actual = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha_elaboracion}"

    def dias_transcurridos(self):
        fecha_actual = timezone.now().date()
        diferencia = fecha_actual - self.fecha_elaboracion
        return diferencia.days
