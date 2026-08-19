import pytest
from rest_framework.test import APIClient
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


@pytest.mark.django_db
class TestRegistro:
    def test_registro_exitoso(self, api_client):
        response = api_client.post('/api/auth/registro/', {
            'nombre': 'Ana',
            'apellido': 'Torres',
            'correo': 'ana@test.com',
            'password': 'clave12345',
        })
        assert response.status_code == 201
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_correo_duplicado(self, api_client, usuario_cliente):
        response = api_client.post('/api/auth/registro/', {
            'nombre': 'Otro',
            'apellido': 'Usuario',
            'correo': 'cliente@test.com',
            'password': 'clave12345',
        })
        assert response.status_code == 400
        assert response.data['correo'][0] == 'Este correo ya está registrado'

    def test_contrasena_corta(self, api_client):
        response = api_client.post('/api/auth/registro/', {
            'nombre': 'Ana',
            'apellido': 'Torres',
            'correo': 'ana2@test.com',
            'password': '1234',
        })
        assert response.status_code == 400