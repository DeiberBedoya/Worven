from drf_spectacular.utils import extend_schema
from rest_framework import  generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from core.permissions import EsAdmin
from .models import Producto, VarianteProducto
from .serializers import(
    ActualizarVarianteProductoSerializer,
    CrearActualizarProductoSerializer,
    CrearVarianteProductoSerializer,
    ProductoSerializer,
)

class ProductoPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'

class ProductoListCreateView(generics.ListCreateAPIView):
    pagination_class = ProductoPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [EsAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CrearActualizarProductoSerializer
        return ProductoSerializer

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True)
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria)
        return queryset

class ProductoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Producto.objects.all()

    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT'):
            return [EsAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return CrearActualizarProductoSerializer
        return ProductoSerializer

class ProductoDesactivarView(APIView):
    permission_classes = [EsAdmin]

    def patch(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        producto.activo = False
        producto.save(update_fields=['activo'])
        return Response(ProductoSerializer(producto).data, status=status.HTTP_200_OK)

class VarianteCreateView(APIView):
    permission_classes = [EsAdmin]

    @extend_schema(request=CrearVarianteProductoSerializer, responses=CrearVarianteProductoSerializer)
    def post(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CrearVarianteProductoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(producto=producto)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VarianteUpdateView(generics.UpdateAPIView):
    queryset = VarianteProducto.objects.all()
    serializer_class = ActualizarVarianteProductoSerializer
    permission_classes = [EsAdmin]