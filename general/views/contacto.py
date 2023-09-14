from rest_framework import viewsets, permissions, status
from general.models.contacto import Contacto
from general.models.documento import Documento
from general.serializers.contacto import ContactoSerializador
from rest_framework.response import Response


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializador    
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        contacto = self.get_object()

        # Verificar si el contacto está siendo utilizado en algún documento
        if Documento.objects.filter(contacto=contacto).exists():
            return Response({'mensaje':'No se puede eliminar el contacto, se encuentras usado en un documento'}, status=status.HTTP_400_BAD_REQUEST)

        # Si no está siendo utilizado en documentos, se puede eliminar
        contacto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)