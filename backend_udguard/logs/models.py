from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Logs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField()
