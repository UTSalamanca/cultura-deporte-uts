from django.shortcuts import redirect
from functools import wraps
from Login.models import UsuarioAcceso
from Sistema.models import UsuarioGrupoSeguridad

def role_required(role, redirect_to):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                usuario_acceso = UsuarioAcceso.objects.filter(login=request.user).first()

                if usuario_acceso:
                    cve_persona = usuario_acceso.cve_persona
                    grupo_seguridad = UsuarioGrupoSeguridad.objects.filter(cve_persona=cve_persona).first()

                    if grupo_seguridad:
                        if grupo_seguridad.cve_grupo_seguridad_id == role:
                            return view_func(request, *args, **kwargs)

                        return redirect(redirect_to)
                return redirect('login')
            return redirect('login')

        return _wrapped_view

    return decorator

# Decorador para las vistas de alumno
def alumno_required(view_func):
    return role_required(role=9, redirect_to='profesor:inicio')(view_func)

# Decorador para las vistas de profesor
def profesor_required(view_func):
    return role_required(role=189, redirect_to='alumno:inicio')(view_func)

# Decorador para las vistas de administrador
""" def administrador_required(view_func):
    return role_required(role=270, redirect_to='administrador:inicio')(view_func) """