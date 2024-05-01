from rest_framework import viewsets, permissions, status
from general.models.contacto import Contacto
from general.models.documento import Documento
from general.serializers.contacto import ContactoSerializador
from rest_framework.response import Response
from django.db.models import ProtectedError

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializador    
    permission_classes = [permissions.IsAuthenticated]               

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        relaciones = instance.contactos_rel.first()
        if relaciones:
            modelo_asociado = relaciones.__class__.__name__           
            return Response({'mensaje':f"El registro no se puede eliminar porque tiene registros asociados en {modelo_asociado}", 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)