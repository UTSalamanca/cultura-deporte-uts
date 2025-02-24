from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.contrib import messages
from Login.models import UsuarioAcceso
from Sistema.models import Usuario, UsuarioGrupoSeguridad
from Login.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('alumno:inicio')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login = form.cleaned_data['login']
        password = form.cleaned_data['password']
        usuario_existente = Usuario.objects.filter(login=login, password=password).first()

        if usuario_existente:
            sistema_usuario = UsuarioAcceso.objects.filter(login=usuario_existente.login).first()

            if sistema_usuario:
                if not check_password(usuario_existente.password, sistema_usuario.password):
                    sistema_usuario.set_password(usuario_existente.password)
                    sistema_usuario.save()


                usuario = authenticate(request, username=login, password=password)
                if usuario:
                    auth_login(request, usuario)
                    return redirect(request.GET.get('next', 'alumno:inicio'))
                else:
                    messages.error(request, "Por favor introduzca un nombre de usuario y contraseña correctos.")
                    return redirect('login:login')

            else:
                sistema_usuario = UsuarioAcceso.objects.create(
                    cve_persona=usuario_existente.cve_persona,
                    login=usuario_existente.login,
                    activo=True,
                    staff=True
                )
                sistema_usuario.set_password(password)
                sistema_usuario.save()

                usuario_grupo_seguridad = UsuarioGrupoSeguridad.objects.filter(cve_persona=usuario_existente.cve_persona)
                for grupo in usuario_grupo_seguridad:
                    group, created = Group.objects.get_or_create(name=grupo.cve_grupo_seguridad)
                    sistema_usuario.groups.add(group)

                auth_login(request, sistema_usuario)
                return redirect(request.GET.get('next', 'alumno:inicio'))

        else:
            messages.error(request, "Por favor introduzca un nombre de usuario y contraseña correctos.")
            return redirect('login:login')

    return render(request, 'Login.html', {'form': form})

                  

def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return render(request, 'Login.html')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)