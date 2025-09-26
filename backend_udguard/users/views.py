from django.shortcuts import get_object_or_404
from users.serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from logs.views import log_action
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail


# ⭐ CREAR PAGINADOR PERSONALIZADO PARA USUARIOS
class UserPagination(PageNumberPagination):
    page_size = 8  # ⭐ COINCIDE CON EL FRONTEND
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # ⭐ LOG DEL LOGIN EXITOSO
        if response.status_code == 200:
            username = request.data.get('username', '')
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                # ⭐ LOG ESPECIAL PARA LOGIN (no usa la instancia del usuario sino la acción directa)
                from logs.models import Logs
                Logs.objects.create(
                    usuario=user,
                    accion=f"LOGIN EXITOSO: {user.first_name} {user.last_name}".strip() or user.username,
                )
            except User.DoesNotExist:
                pass
        
        return response


class RegisterUserViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # ⭐ LOG MEJORADO CON TIPO DE USUARIO
            user_type_map = {
                'admin': 'Administrador',
                'consultor': 'Consultor',
                'user': 'Usuario',
                'auxiliar': 'Auxiliar'
            }
            tipo_user_display = user_type_map.get(user.tipo_user, user.tipo_user)
            extra_info = f"tipo: {tipo_user_display}, email: {user.email}"
            log_action(user, "create", request.user, extra_info)
            
            return Response(
                {"message": "Usuario creado con exito"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, num_page=None):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
        User = get_user_model()
        users = User.objects.all().order_by('-date_joined')  # ⭐ ORDENAR POR FECHA DE REGISTRO
        
        # ⭐ SI NO SE ESPECIFICA num_page, DEVOLVER TODOS LOS USUARIOS CON PAGINACIÓN ESTÁNDAR
        if num_page is None:
            paginator = UserPagination()
            result_page = paginator.paginate_queryset(users, request)
            serializer = UserListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # ⭐ SI SE ESPECIFICA num_page, USARLO COMO page_size (RETROCOMPATIBILIDAD)
        paginator = PageNumberPagination()
        paginator.page_size = int(num_page) if str(num_page).isdigit() else 8
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def delete(self, request, user_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        user = get_object_or_404(User, pk=user_id)
        
        # ⭐ CAMBIAR ESTADO EN LUGAR DE ELIMINAR
        if user.is_active:
            # Cambiar a inactivo
            user.is_active = False
            action_text = "disable"
            status_text = "inhabilitado"
        else:
            # Cambiar a activo
            user.is_active = True
            action_text = "enable" 
            status_text = "habilitado"
        
        user.save()
        
        # ⭐ GUARDAR INFORMACIÓN PARA EL LOG
        user_name = f"{user.first_name} {user.last_name}".strip() or user.username
        user_email = user.email
        user_type_map = {
            'admin': 'Administrador',
            'consultor': 'Consultor', 
            'user': 'Usuario',
            'auxiliar': 'Auxiliar'
        }
        tipo_user_display = user_type_map.get(user.tipo_user, user.tipo_user)
        extra_info = f"tipo: {tipo_user_display}, email: {user_email}"
        
        # ⭐ LOG DE LA ACCIÓN
        log_action(user, action_text, request.user, extra_info)
        
        return Response({
            "detail": f"Usuario {status_text} correctamente",
            "user": {
                "id": user.id,
                "is_active": user.is_active,
                "status": "Activo" if user.is_active else "Inactivo"
            }
        }, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        User = get_user_model()
        user = get_object_or_404(User, pk=user_id)

        # ⭐ DETECTAR SI ES UNA ACCIÓN DE DESHABILITACIÓN O CAMBIO DE CONTRASEÑA
        is_disabling = 'is_active' in request.data and not request.data['is_active']
        is_enabling = 'is_active' in request.data and request.data['is_active']
        is_password_change = 'password' in request.data and request.data['password']  # ⭐ NUEVO

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            
            # ⭐ LOG ESPECÍFICO SEGÚN LA ACCIÓN
            user_type_map = {
                'admin': 'Administrador',
                'consultor': 'Consultor',
                'user': 'Usuario', 
                'auxiliar': 'Auxiliar'
            }
            tipo_user_display = user_type_map.get(updated_user.tipo_user, updated_user.tipo_user)
            extra_info = f"tipo: {tipo_user_display}, email: {updated_user.email}"
            
            if is_disabling:
                log_action(updated_user, "disable", request.user, extra_info)
            elif is_enabling:
                log_action(updated_user, "enable", request.user, extra_info)
            elif is_password_change:  # ⭐ NUEVO LOG PARA CAMBIO DE CONTRASEÑA
                log_action(updated_user, "password_change", request.user, f"contraseña actualizada - {extra_info}")
            else:
                log_action(updated_user, "update", request.user, extra_info)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ⭐ RESTO DE CLASES SIN CAMBIOS...
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Correo no registrado"}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"http://localhost:3000/reset-password?uid={uid}&token={token}"

        send_mail(
            subject="Recupera tu contraseña",
            message=f"Recupera tu contraseña desde este enlace:\n{reset_url}",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response({"detail": "email de recuperacion enviado"})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            User = get_user_model()

            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"detail": "Usuario inválido"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token inválido o expirado"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Contraseña actualizada correctamente"})


class UserByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserListSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

