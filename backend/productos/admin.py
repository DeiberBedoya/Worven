from django.contrib import admin
from .models import Producto, VarianteProducto

class VarianteProductoInline(admin.TabularInline):
    model = VarianteProducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'activo', 'fecha_creacion')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'categoria')
    inlines = [VarianteProductoInline]

@admin.register(VarianteProducto)
class VarienteProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'talla', 'color', 'stock', 'sku')
    search_fields = ('sku',)