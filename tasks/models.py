from django.db import models
from django.contrib.auth.models import User #para las relaciones de tabla con el usuario
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) #guardar fecha y hora de cuando fue creado, el valor auto_now_add=True es para que no se ponga el campo en formulario debido que se rellena automaticament
    datecompleted = models.DateTimeField(null=True, blank=True)  #el usuario debe poner cuando completo la tarea, blank s para dejar como campo opcional
    important = models.BooleanField(default=False) #coloca la tarea como no importante por defecto
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): #para que el admin vea la tarea por titulo
        return self.title + '-by ' + self.user.username