from django.contrib.auth import get_user_model
from django.db import models
import uuid


class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(null=False)
    fecha_evento = models.DateTimeField()
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
