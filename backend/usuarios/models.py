from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico.")
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=ROL_CHOICES, default='cliente')
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return self.correo