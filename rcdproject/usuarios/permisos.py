from rest_framework.permissions import BasePermission

def RutaProtegida(roles_permitidos):
    """
    Retorna una clase de permiso que permite el acceso solo a usuarios con alguno de los roles especificados.
    Ejemplo de uso:
        permission_classes = [RutaProtegida(['cliente', 'tecnico'])]
    """
    class _RutaProtegida(BasePermission):
        def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.rol in roles_permitidos
    return _RutaProtegida

