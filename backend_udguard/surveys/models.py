from django.db import models
from django.contrib.auth import get_user_model
import uuid

from assessment.models import Indicator


class surveys(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    indicador = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    resultado = models.FloatField()
    fecha = models.DateTimeField()
    creador_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
