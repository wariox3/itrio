from rest_framework import viewsets, permissions
from general.models.contacto import Contacto
from general.serializers.contacto import ContactoSerializador


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializador    
    permission_classes = [permissions.IsAuthenticated]