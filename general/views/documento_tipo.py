from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.documento_tipo import DocumentoTipo
from general.serializers.documento_tipo import DocumentoTipoSerializador

class DocumentoTipoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoTipo.objects.all().order_by('id')
    serializer_class = DocumentoTipoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response({'mensaje': 'No es posible crear un registro nuevo'}, status=status.HTTP_400_BAD_REQUEST)