from rest_framework import serializers
from .models import Usuario

class RegistroSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True, min_length=8)

    class Meta: 
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo', 'password']
        extra_kwargs = {
            'correo': {'validators': []},
        }

    def validate_correo(self, value):
        if Usuario.objects.filter(correo=value).exists():
            raise serializers.ValidationError('Este correo ya esta registrado')
        return value

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']
        read_only_fields = ['id', 'correo']

class ActualizarPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'direccion', 'telefono']

class ListaUsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo', 'rol', 'direccion', 'telefono']