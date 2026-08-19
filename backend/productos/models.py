from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    categoria = models.CharField(max_length=100)
    imagen_principal = models.ImageField(upload_to='productos/',blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

class VarianteProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='variantes', on_delete=models.CASCADE)
    talla = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.producto.nombre} - {self.talla}/{self.color} ({self.sku})'
