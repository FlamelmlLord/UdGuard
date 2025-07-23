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


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            log_action(request.user, "create", request.user)
            return Response(
                {"message": "Usuario creado con exito"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, num_page=5):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        users = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = num_page
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def delete(self, request, user_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        User = get_user_model()
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        log_action(request.user, "delete", request.user)
        return Response({"detail": "User eliminado"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, user_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        User = get_user_model()
        user = get_object_or_404(User, pk=user_id)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            log_action(request.user, "update", request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
