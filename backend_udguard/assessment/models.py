from django.db import models
import uuid


class Factors(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.TextField()


class Characteristics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    factors = models.ForeignKey(Factors, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField()


class Indicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caracteristica = models.ForeignKey(Characteristics, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=511, null=False)
    link_evidencia = models.CharField(max_length=512, null=True, blank=True)
    ponderacion = models.IntegerField()
    meta = models.IntegerField()
    calificacion = models.FloatField()

    @property
    def puntos(self):
        return self.ponderacion * self.calificacion

    @property
    def porcentaje(self):
        if self.meta:
            return round((self.puntos / self.meta) * 100, -1)
        return 0
