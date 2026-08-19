from rest_framework import serializers
from .models import Producto, VarianteProducto

class VarianteProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarianteProducto
        fields = ['id', 'talla', 'color', 'stock', 'sku']

class CrearVarianteProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarianteProducto
        fields = ['id', 'talla', 'color', 'stock', 'sku']

    def validate_sku(self, value):
        if VarianteProducto.objects.filter(sku=value).exists():
            raise serializers.ValidationError('Este SKU ya está en uso por otra variante.')
        return value

class ActualizarVarianteProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarianteProducto
        fields = ['id', 'talla', 'color', 'stock', 'sku']
        extra_kwargs = {
            'talla': {'required': False},
            'color': {'required': False},
            'stock': {'required': False},
            'sku': {'required': False},
        }

    def validate_sku(self, value):
        qs = VarianteProducto.objects.filter(sku=value).exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Este SKU ya está en uso por otra variante.')
        return value

class ProductoSerializer(serializers.ModelSerializer):
    variantes = VarianteProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'categoria',
            'imagen_principal', 'activo', 'fecha_creacion', 'variantes',
        ]
        read_only_fields = ['id', 'fecha_creacion']

class CrearActualizarProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'categoria',
            'imagen_principal', 'activo', 'fecha_creacion',
        ]
        read_only_fields = ['id', 'fecha_creacion']