from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistroView, LogoutView, PerfilView, ListaUsuariosView

urlpatterns = [
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('usuarios/me/', PerfilView.as_view(), name='perfil'),
    path('usuarios/', ListaUsuariosView.as_view(), name='lista-usuarios'),
]