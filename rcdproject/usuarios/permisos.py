from rest_framework.permissions import BasePermission

def RutaProtegida(roles_permitidos):
    """
    Retorna una clase de permiso que permite el acceso solo a usuarios con alguno de los roles especificados
    """
    class _RutaProtegida(BasePermission):
        def has_permission(self, request, view):
            print("Usuario autenticado:", request.user)
            print("Rol del usuario:", getattr(request.user, 'rol', None))
            return request.user.is_authenticated and request.user.rol in roles_permitidos
    return _RutaProtegida

