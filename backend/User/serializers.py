from datetime import time
from rest_framework import serializers
from .models import Role, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from decimal import Decimal
import cloudinary
import cloudinary.uploader
import time
from rest_framework.validators import UniqueValidator
import re

class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este correo ya está registrado.")]
    )
    confirmPassword = serializers.CharField(write_only=True)
    terms = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'password', 'confirmPassword', 'address', 'phone', 'image', 'terms'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # Validaciones
    def validate_first_name(self, value):
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ]+$', value):
            raise serializers.ValidationError(
                "El nombre solo puede contener letras, sin espacios ni símbolos."
            )
        if '<' in value or '>' in value:
            raise serializers.ValidationError(
                "El nombre no puede contener los caracteres '<' o '>'."
            )
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ]+$', value):
            raise serializers.ValidationError(
                "El apellido solo puede contener letras, sin espacios ni símbolos."
            )
        if '<' in value or '>' in value:
            raise serializers.ValidationError(
                "El apellido no puede contener los caracteres '<' o '>'."
            )
        return value

    def validate_phone(self, value):
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("El teléfono debe tener exactamente 10 números.")
        return value

    def validate(self, data):
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')

        if len(password) < 8 or len(password) > 30:
            raise serializers.ValidationError({"password": "La contraseña debe tener entre 8 y 30 caracteres."})
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            raise serializers.ValidationError({"password": "La contraseña debe tener mayúsculas y minúsculas."})
        if not re.search(r'[\d!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError({"password": "La contraseña debe tener al menos un número o símbolo."})
        if ' ' in password:
            raise serializers.ValidationError({"password": "La contraseña no debe contener espacios."})

        # Validación de confirmación de contraseña
        if confirm_password != '' and password != confirm_password:
            raise serializers.ValidationError({"non_field_errors": ["Las contraseñas no coinciden."]})

        return data

    def validate_terms(self, value):
        if not value:
            raise serializers.ValidationError("Debes aceptar los términos y condiciones.")
        return value

    def to_internal_value(self, data):
        allowed = set(self.fields)
        extra = set(data) - allowed
        if extra:
        # Devuelve un dict, no un string
            raise serializers.ValidationError({"non_field_errors": [f"Campos no permitidos: {', '.join(extra)}"]})
        return super().to_internal_value(data)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            address=validated_data.get('address', ''),
            phone=validated_data.get('phone', ''),
            image=validated_data.get('image')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        image = validated_data.get('image', None)
        if image:
            instance.image = image

        instance.save()
        return instance

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'