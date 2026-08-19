from django.urls import path 
from .views import (
    ProductoDesactivarView,
    ProductoDetailView,
    ProductoListCreateView,
    VarianteCreateView,
    VarianteUpdateView,
)

urlpatterns = [
    path('productos/', ProductoListCreateView.as_view(), name='productos-lista'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detalle'),
    path('productos/<int:pk>/desactivar/', ProductoDesactivarView.as_view(), name='producto-desactivar'),
    path('productos/<int:pk>/variantes/', VarianteCreateView.as_view(), name='producto-variantes-crear'),
    path('productos/variantes/<int:pk>/', VarianteUpdateView.as_view(), name='variante-actualizar'),
]