from django.shortcuts import render, redirect, get_object_or_404
# para creacion por defecto de forulario de autenticacion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm     #importar los campos del formulario personalizado
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required  #para anteponer login en las paginas

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':  #UserCreationForm es un formulario predefinido
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        #password1 es inicial, password2 es "comprobar contraseña"
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()   #salva en memoria el usuario
                login(request, user)  #funcion de django para hacer login con el usuario
                return redirect('tasks')

            except IntegrityError: #se coloa para diferencia el error con la DB
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })

@login_required  #se coloca antes de la funcion para reconocer que primero debe esta logeado
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_done(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': 'TaskForm',
                'error': 'please provide valid data'
            })

@login_required
def task_detail(request, task_id):
    #task = Task.objects.get(pk=task_id)   #forma convencional
    task = get_object_or_404(Task, pk=task_id, user=request.user) #buscar or el id, y tambien, que la tarea sea exclusiva de manejar por su respectivo usuario
    if request.method == 'GET':
        form = TaskForm(instance=task) #personalizar formulario con la instancia
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'error Updating Task'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()  #la tarea se completa porque ya hay fecha cumplida
        task.save()  #se actualiza
        return redirect('tasks')

@login_required  
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()     #borrar
        return redirect('tasks')

@login_required
def signout(request):  #funcion cerrar sesion, no poner logout como nombre debido a conflicto de nombres
    logout(request)   #funcion de Django para cerrar sesion
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        #AuthenticationForm es una plantilla de login predefinida de django
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  #funcion authenticate es para autenticar los datos con la tabla de usuarios, especificar los campos
        if user is None:  #si no encontro el usuario
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
