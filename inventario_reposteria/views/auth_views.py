import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.generic import View

class LoginView(View):
    # Vista para iniciar sesión de usuarios
    
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html')
        
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Debe ingresar nombre de usuario y contraseña.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                
        return render(request, 'registration/login.html')

class LogoutView(View):
    # Vista para cerrar sesión de usuarios
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, '¡Has cerrado sesión exitosamente!')
        return redirect('login')

class RegisterView(View):
    # Vista para registrar nuevos usuarios
    
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/register.html')
        
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Reglas de validación para registro
        validation_rules = [
            (not first_name, 'El nombre es obligatorio.'),
            (first_name and len(first_name) < 2, 'El nombre debe tener al menos 2 caracteres.'),
            (not last_name, 'El apellido es obligatorio.'),
            (last_name and len(last_name) < 2, 'El apellido debe tener al menos 2 caracteres.'),
            (not username, 'El nombre de usuario es obligatorio y no puede estar vacío.'),
            (username and len(username) < 3, 'El nombre de usuario debe tener al menos 3 caracteres.'),
            (username and not re.match(r'^[\w.@+-]+$', username), 'El nombre de usuario solo puede contener letras, números y los caracteres @, ., +, - y _.'),
            (username and User.objects.filter(username=username).exists(), 'El nombre de usuario ya existe.'),
            (not password1, 'La contraseña es obligatoria.'),
            (password1 and password1 != password2, 'Las contraseñas no coinciden.'),
            (password1 and len(password1) < 8, 'La contraseña es muy corta. Debe tener al menos 8 caracteres.'),
        ]
        
        errors = [message for is_error, message in validation_rules if is_error]
        
        # Validación nativa de contraseñas de Django
        if not errors and password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors.extend(e.messages)
                
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'registration/register.html', {
                'form': {
                    'username': {'value': username},
                    'first_name': {'value': first_name},
                    'last_name': {'value': last_name},
                }
            })
            
        try:
            user = User.objects.create_user(
                username=username,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
        except Exception:
            messages.error(request, 'Error al crear la cuenta. Intenta de nuevo.')
            return render(request, 'registration/register.html', {
                'form': {
                    'username': {'value': username},
                    'first_name': {'value': first_name},
                    'last_name': {'value': last_name},
                }
            })
