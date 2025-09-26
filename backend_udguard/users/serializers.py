from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["tipo_user"] = user.tipo_user
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        self.user.last_login = now()
        self.user.save(update_fields=["last_login"])
        data["tipo_user"] = self.user.tipo_user
        return data


# Verificar que el UserListSerializer incluya todos los campos que necesitamos
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",            # Propiedad calculada
            "first_name",      # ⭐ AGREGAR CAMPOS SEPARADOS
            "last_name",       # ⭐ AGREGAR CAMPOS SEPARADOS
            "username",
            "status",
            "is_active",
            "tipo_user",
            "date_joined",
            "last_login",
            "email"
        ]
        read_only_fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "documento",
            "tipo_user",
            "tipo_estudio",
            "experiencia_laboral",
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)  # ⭐ AGREGAR CAMPO PASSWORD
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "tipo_user", "is_active", "documento", "password"]  # ⭐ INCLUIR PASSWORD
        read_only_fields = ["id", "username"]

    def validate_email(self, value):
        # ⭐ VALIDAR EMAIL SOLO SI ES DIFERENTE AL ACTUAL
        user = self.instance
        if user and User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Este correo ya está registrado por otro usuario.")
        return value
    
    def validate_password(self, value):
        """Validar contraseña si se proporciona"""
        if value:
            if len(value) < 8:
                raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            
            # Validaciones adicionales de seguridad
            if not any(c.isupper() for c in value):
                raise serializers.ValidationError("La contraseña debe contener al menos una mayúscula.")
            if not any(c.islower() for c in value):
                raise serializers.ValidationError("La contraseña debe contener al menos una minúscula.")
            if not any(c.isdigit() for c in value):
                raise serializers.ValidationError("La contraseña debe contener al menos un número.")
            if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in value):
                raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial.")
        
        return value
    
    def update(self, instance, validated_data):
        """Actualizar usuario con encriptación de contraseña"""
        password = validated_data.pop('password', None)
        
        # Actualizar campos normales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Si se proporciona contraseña, encriptarla
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
