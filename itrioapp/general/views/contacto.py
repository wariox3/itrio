from rest_framework import viewsets, permissions
from general.models.contacto import Contacto
from general.serializers.contacto import ContactoSerializador


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def handle_exception(self, exc):
        response = super().handle_exception(exc)

        if response is None:
            return None

        if response.status_code == 400:
            response.data = {
                'mensaje': 'Mensajes de validacion',
                'codigo': 14,
                'validacion': response.data
            }

        return response