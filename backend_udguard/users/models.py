from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    documento = models.CharField(max_length=20, null=False)
    tipo_user = models.CharField(max_length=20, null=False)
    tipo_estudio = models.CharField(max_length=20, null=False)
    experiencia_laboral = models.TextField()

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def status(self):
        return "Activo" if self.is_active else "Inactivo"
