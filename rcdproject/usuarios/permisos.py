from rest_framework.permissions import BasePermission

class RutaProtegida(BasePermission):
    """
    Permiso que permite el acceso solo a usuarios con alguno de los roles especificados.
    Ejemplo de uso en la vista:
        permission_classes = [RutaProtegida(['cliente', 'tecnico'])]
    """
    def __init__(self, roles_permitidos):
        self.roles_permitidos = roles_permitidos

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in self.roles_permitidos

