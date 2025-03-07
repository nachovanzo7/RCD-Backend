from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from obras.models import Obra
from fotos.models import Fotos
from usuarios.permisos import RutaProtegida
from fotos.serializers import FotosSerializer

class AgregarImagenesObra(APIView):
    """
    Permite agregar varias imágenes a una obra, cada una con descripción y fecha.
    Se espera que en el request.FILES se envíen múltiples archivos con la clave "imagenes",
    y en request.data se envíen listas (paralelas) en "descripciones" y "fechas".
    """
    permission_classes = [RutaProtegida(['superadmin', 'tecnico'])]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        images = request.FILES.getlist('imagenes')
        descripciones = request.data.getlist('descripciones')
        fechas = request.data.getlist('fechas')
        
        if not images:
            return Response({'error': 'No se proporcionaron imágenes.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not descripciones:
            descripciones = [""] * len(images)
        if not fechas:
            fechas = [None] * len(images)
        
        for idx, image in enumerate(images):
            desc = descripciones[idx] if idx < len(descripciones) else ""
            fecha = fechas[idx] if idx < len(fechas) and fechas[idx] != "" else None
            Fotos.objects.create(obra=obra, imagen=image, descripcion=desc, fecha=fecha)
        
        return Response({'mensaje': 'Imágenes agregadas correctamente.'}, status=status.HTTP_200_OK)

class VerImagenesObra(APIView):
    """
    Devuelve todas las imágenes de una obra, incluyendo descripción y fecha.
    """
    permission_classes = [RutaProtegida(['superadmin', 'tecnico', 'coordinador', 'coordinadorlogistico'])]

    def get(self, request, obra_pk):
        try:
            obra = Obra.objects.get(pk=obra_pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        imagenes = obra.imagenes_set.all()
        serializer = FotosSerializer(imagenes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)