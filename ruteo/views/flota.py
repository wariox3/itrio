from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.flota import RutFlota
from ruteo.models.vehiculo import RutVehiculo
from ruteo.serializers.flota import RutFlotaSerializador
from django.db import transaction

class RutFlotaViewSet(viewsets.ModelViewSet):
    queryset = RutFlota.objects.all()
    serializer_class = RutFlotaSerializador
    permission_classes = [permissions.IsAuthenticated]                 

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            vehiculo_id = request.data.get('vehiculo')
            nueva_prioridad = request.data.get('prioridad')

            vehiculo = RutVehiculo.objects.filter(id=vehiculo_id).first()
            if not vehiculo:
                return Response(
                    {'error': 'El vehículo especificado no existe'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            flota_data = {
                'vehiculo': vehiculo_id,
            }
            serializer = self.get_serializer(data=flota_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            vehiculo.prioridad = nueva_prioridad
            vehiculo.save()

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
