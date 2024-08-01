from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.documento_tipo import DocumentoTipo
from general.models.resolucion import Resolucion
from general.serializers.documento_tipo import GenDocumentoTipoSerializador

class DocumentoTipoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoTipo.objects.all().order_by('id')
    serializer_class = GenDocumentoTipoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response({'mensaje': 'No es posible crear un registro nuevo'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'asignar-resolucion')
    def asignar_resolucion(self, request):
        raw = request.data
        resolucion_id = raw.get('resolucion_id')
        if resolucion_id:
            try:                
                documento_tipo = DocumentoTipo.objects.get(pk=1)
                if documento_tipo.resolucion_id == None:
                    resolucion = Resolucion.objects.get(pk=resolucion_id)
                    documento_tipo.resolucion = resolucion
                    documento_tipo.save()                
                    return Response({'asignado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje': 'El documento ya tiene resolucion', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)  
            except Resolucion.DoesNotExist:
                return Response({'mensaje':'La resolucion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                         
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)      