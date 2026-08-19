import pytest
from rest_framework.test import APIClient
from usuarios.models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken


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

@pytest.mark.django_db
class TestLogin:
    def test_login_exitoso(self, api_client, usuario_cliente):
        response = api_client.post('/api/auth/login/', {
            'correo': 'cliente@test.com',
            'password': 'clave12345',
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_password_incorrecta(self, api_client, usuario_cliente):
        response = api_client.post('/api/auth/login/', {
            'correo': 'cliente@test.com',
            'password': 'password_equivocada',
        })
        assert response.status_code == 401


@pytest.mark.django_db
class TestPerfil:
    def test_ver_perfil_autenticado(self, api_client, usuario_cliente):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.get('/api/usuarios/me/')
        assert response.status_code == 200
        assert response.data['correo'] == 'cliente@test.com'

    def test_ver_perfil_sin_autenticar(self, api_client):
        response = api_client.get('/api/usuarios/me/')
        assert response.status_code == 401

    def test_editar_perfil(self, api_client, usuario_cliente):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.patch('/api/usuarios/me/', {
            'direccion': 'Calle 45 #12-30',
        })
        assert response.status_code == 200
        assert response.data['direccion'] == 'Calle 45 #12-30'

    def test_no_puede_cambiar_correo_desde_perfil(self, api_client, usuario_cliente):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.patch('/api/usuarios/me/', {
            'correo': 'hackeado@test.com',
        })
        assert response.status_code == 200
        usuario_cliente.refresh_from_db()
        assert usuario_cliente.correo == 'cliente@test.com'


@pytest.mark.django_db
class TestListaUsuarios:
    def test_admin_puede_listar(self, api_client, usuario_admin):
        api_client.force_authenticate(user=usuario_admin)
        response = api_client.get('/api/usuarios/')
        assert response.status_code == 200

    def test_cliente_no_puede_listar(self, api_client, usuario_cliente):
        api_client.force_authenticate(user=usuario_cliente)
        response = api_client.get('/api/usuarios/')
        assert response.status_code == 403

    def test_anonimo_no_puede_listar(self, api_client):
        response = api_client.get('/api/usuarios/')
        assert response.status_code == 401


@pytest.mark.django_db
class TestRefreshYLogout:
    def test_refresh_exitoso(self, api_client, usuario_cliente):
        refresh = RefreshToken.for_user(usuario_cliente)
        response = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh),
        })
        assert response.status_code == 200
        assert 'access' in response.data

    def test_logout_invalida_el_refresh(self, api_client, usuario_cliente):
        refresh = RefreshToken.for_user(usuario_cliente)
        api_client.force_authenticate(user=usuario_cliente)

        response_logout = api_client.post('/api/auth/logout/', {
            'refresh': str(refresh),
        })
        assert response_logout.status_code == 205

        # Intentar usar el mismo refresh de nuevo debe fallar (blacklist)
        api_client.force_authenticate(user=None)
        response_refresh = api_client.post('/api/auth/refresh/', {
            'refresh': str(refresh),
        })
        assert response_refresh.status_code == 401