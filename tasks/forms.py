#from django.forms import ModelForm  #para crear formularios de modelos ya establecidos
from .models import Task     #se importa el modelo
from django import forms

class TaskForm(forms.ModelForm): #se
    class Meta:
        model = Task
        fields= ['title', 'description', 'important'] #se colocan los campos necesarios para el formulario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'put a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        } #los widgets es para que, desde el form cuando son formularios propios, contengan estilos de bootstrap, pues no es posible manejarlos en el html para modificarlo como tal, son diccionarios, nombre_variable=valor_segun_bootstrap