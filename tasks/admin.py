from django.contrib import admin
from .models import Task   #traer el modelo, al venir de la misma capreta es ".models"
# Register your models here. para que lo vea el admin

class TaskAdmin(admin.ModelAdmin): #crear clase para ver parametros de solo lectura
    readonly_fields = ("created", )

admin.site.register(Task, TaskAdmin)