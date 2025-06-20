from django.contrib.auth import logout
from bson import ObjectId
from .models import Usuario

def auth_context(request):
    usuario_id = request.session.get('usuario_id')
    autenticado = bool(usuario_id)
    usuario_nombre = None
    
    if autenticado:
        try:
            usuario = Usuario.objects.get(_id=ObjectId(usuario_id))
            usuario_nombre = usuario.nombre_usuario
        except Usuario.DoesNotExist:
            logout(request)  # Limpia sesión inválida
    
    return {
        'autenticado': autenticado,
        'usuario_nombre': usuario_nombre
    }