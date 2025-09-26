from django.contrib.auth import get_user_model
from django.db import models
import uuid


class Events(models.Model):
    # ⭐ AGREGAR CHOICES PARA LOGS DESCRIPTIVOS
    TIPO_EVENTO_CHOICES = [
        ('meeting', 'Reunión'),
        ('deadline', 'Fecha Límite'),
        ('event', 'Evento'),
        ('holiday', 'Feriado'),
        ('exam', 'Examen'),
        ('presentation', 'Presentación'),
        ('workshop', 'Taller'),
        ('conference', 'Conferencia'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(null=False)
    fecha_inicio = models.DateTimeField()
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=100, choices=TIPO_EVENTO_CHOICES, null=False)
    fecha_fin = models.DateTimeField(auto_now_add=False)

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.strftime('%Y-%m-%d')}"
