from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets

from .forms import CustomUserCreationForm
from .models import User
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action in ['list', 'retrieve']:
            return UserDefaultSerializer
        return super().get_serializer_class()


# =============================================
# Metodo para registrar usuarios
# =============================================
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Usuario registrado exitosamente")
            # Redirige a la página de login después de registrar al usuario
            return redirect('users:login')  # Asegúrate de que 'users:login' coincide con tu configuración de URL
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# =============================================
# Metodo para loguear usuarios
# =============================================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Intentando login con email: {email}")  # Debug para ver email y contraseña

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            print(f"Usuario autenticado correctamente: {user.email}")
            next_url = request.GET.get('next', 'users:cuenta')
            return redirect(next_url)
        else:
            print("Autenticación fallida")
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')

# =============================================
# Metodo para redirigir al usuario a su cuenta
# =============================================

@login_required
def cuenta_view(request):
    # Lógica de la vista
    return render(request, 'cuenta.html')


