import pytest
from rest_framework.test import APIClient

from productos.models import Producto, VarianteProducto
from usuarios.models import Usuario


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def usuario_cliente(db):
    return Usuario.objects.create_user(
        correo='cliente@test.com',
        password='clave12345',
        nombre='Juan',
        apellido='Pérez',
    )


@pytest.fixture
def usuario_admin(db):
    return Usuario.objects.create_superuser(
        correo='admin@test.com',
        password='clave12345',
        nombre='Admin',
        apellido='Worven',
    )


@pytest.fixture
def producto(db):
    return Producto.objects.create(
        nombre='Camiseta Básica',
        descripcion='Camiseta de algodón',
        precio=59900,
        categoria='camisetas',
    )

def crear_productos(cantidad, categoria='camisetas'):
    productos = []
    for i in range(cantidad):
        productos.append(Producto(
            nombre=f'Camiseta {i}',
            precio=10000 + i,
            categoria=categoria,
        ))
    Producto.objects.bulk_create(productos)


@pytest.mark.django_db
class TestListaProductos:
    def test_paginacion_minimo_12_por_pagina(self, api_client):
        crear_productos(15)
        response = api_client.get('/api/productos/')
        assert response.status_code == 200
        assert len(response.data['results']) == 12
        assert response.data['count'] == 15

    def test_filtro_por_categoria(self, api_client):
        crear_productos(3, categoria='camisetas')
        crear_productos(2, categoria='pantalones')
        response = api_client.get('/api/productos/?categoria=pantalones')
        assert response.status_code == 200
        assert response.data['count'] == 2
        assert all(p['categoria'] == 'pantalones' for p in response.data['results'])

    def test_sin_resultados(self, api_client):
        response = api_client.get('/api/productos/?categoria=inexistente')
        assert response.status_code == 200
        assert response.data['count'] == 0

    def test_producto_inactivo_no_aparece_en_catalogo(self, api_client, producto):
        producto.activo = False
        producto.save()
        response = api_client.get('/api/productos/')
        assert response.data['count'] == 0


@pytest.mark.django_db
class TestDetalleProducto:
    def test_detalle_incluye_variantes(self, api_client, producto):
        VarianteProducto.objects.create(producto=producto, talla='S', color='Blanco', stock=5, sku='CAM-S-BLA')
        response = api_client.get(f'/api/productos/{producto.id}/')
        assert response.status_code == 200
        assert len(response.data['variantes']) == 1


@pytest.mark.django_db
class TestCrearProducto:
    def test_admin_puede_crear(self, api_client, usuario_admin):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.post('/api/productos/', {
            'nombre': 'Camiseta Nueva',
            'precio': '45000',
            'categoria': 'camisetas',
            'activo': True,
        })
        assert response.status_code == 201
        assert response.data['activo'] is True

    def test_cliente_no_puede_crear(self, api_client, usuario_cliente):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.post('/api/productos/', {
            'nombre': 'Camiseta Nueva',
            'precio': '45000',
            'categoria': 'camisetas',
        })
        assert response.status_code == 403

    def test_anonimo_no_puede_crear(self, api_client):
        response = api_client.post('/api/productos/', {
            'nombre': 'Camiseta Nueva',
            'precio': '45000',
            'categoria': 'camisetas',
        })
        assert response.status_code == 401

    def test_precio_en_cero_es_invalido(self, api_client, usuario_admin):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.post('/api/productos/', {
            'nombre': 'Camiseta Gratis',
            'precio': '0',
            'categoria': 'camisetas',
        })
        assert response.status_code == 400

@pytest.mark.django_db
class TestActualizarProducto:
    def test_admin_puede_editar(self, api_client, usuario_admin, producto):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.patch(f'/api/productos/{producto.id}/', {'precio': '75000'})
        assert response.status_code == 200
        assert response.data['precio'] == '75000.00'

    def test_cliente_no_puede_editar(self, api_client, usuario_cliente, producto):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.patch(f'/api/productos/{producto.id}/', {'precio': '75000'})
        assert response.status_code == 403


@pytest.mark.django_db
class TestDesactivarProducto:
    def test_admin_puede_desactivar(self, api_client, usuario_admin, producto):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.patch(f'/api/productos/{producto.id}/desactivar/')
        assert response.status_code == 200

        producto.refresh_from_db()
        assert producto.activo is False

    def test_desactivar_no_borra_de_bd(self, api_client, usuario_admin, producto):
        api_client.force_authenticate(user=usuario_admin)
        api_client.patch(f'/api/productos/{producto.id}/desactivar/')
        assert Producto.objects.filter(id=producto.id).exists()

    def test_cliente_no_puede_desactivar(self, api_client, usuario_cliente, producto):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.patch(f'/api/productos/{producto.id}/desactivar/')
        assert response.status_code == 403


@pytest.mark.django_db
class TestVariantes:
    def test_admin_puede_agregar_variante(self, api_client, usuario_admin, producto):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.post(f'/api/productos/{producto.id}/variantes/', {
            'talla': 'L',
            'color': 'Azul',
            'stock': 20,
            'sku': 'CAM-L-AZU',
        })
        assert response.status_code == 201

    def test_no_permite_sku_repetido(self, api_client, usuario_admin, producto):
        VarianteProducto.objects.create(producto=producto, talla='M', color='Negro', stock=10, sku='CAM-M-NEG')
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.post(f'/api/productos/{producto.id}/variantes/', {
            'talla': 'L',
            'color': 'Azul',
            'stock': 20,
            'sku': 'CAM-M-NEG',
        })
        assert response.status_code == 400

    def test_stock_negativo_es_invalido(self, api_client, usuario_admin, producto):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.post(f'/api/productos/{producto.id}/variantes/', {
            'talla': 'L',
            'color': 'Azul',
            'stock': -5,
            'sku': 'CAM-L-AZU',
        })
        assert response.status_code == 400

    def test_cliente_no_puede_agregar_variante(self, api_client, usuario_cliente, producto):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.post(f'/api/productos/{producto.id}/variantes/', {
            'talla': 'L',
            'color': 'Azul',
            'stock': 20,
            'sku': 'CAM-L-AZU',
        })
        assert response.status_code == 403

    def test_admin_puede_editar_variante(self, api_client, usuario_admin, producto):
        variante = VarianteProducto.objects.create(
            producto=producto, talla='M', color='Negro', stock=10, sku='CAM-M-NEG',
        )
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.patch(f'/api/productos/variantes/{variante.id}/', {'stock': 3})
        assert response.status_code == 200
        variante.refresh_from_db()
        assert variante.stock == 3