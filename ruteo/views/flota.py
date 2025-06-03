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
            vehiculo_id = request.data.get('id')
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
        
    @action(detail=False, methods=['post'], url_path=r'cambiar-prioridad')
    def cambiar_prioridad(self, request, *args, **kwargs):
        with transaction.atomic():
                # Obtener datos del request
                vehiculo_id = request.data.get('id')
                nueva_prioridad = int(request.data.get('prioridad'))

                # Validar que exista el vehículo a modificar
                vehiculo_actual = RutVehiculo.objects.filter(id=vehiculo_id).first()
                if not vehiculo_actual:
                    return Response(
                        {'error': 'El vehículo especificado no existe'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Obtener el conteo total de vehículos en la flota
                total_vehiculos = RutVehiculo.objects.filter(rutflota__isnull=False).count()

                # Validar que la nueva prioridad esté dentro del rango permitido
                if nueva_prioridad < 1 or nueva_prioridad > total_vehiculos:
                    return Response(
                        {
                            'error': f'Prioridad inválida',
                            'mensaje': f'La prioridad debe estar entre 1 y {total_vehiculos}',
                            'prioridad_maxima_permitida': total_vehiculos
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Buscar el vehículo que tiene actualmente esa prioridad
                vehiculo_con_prioridad = RutVehiculo.objects.filter(
                    prioridad=nueva_prioridad
                ).exclude(id=vehiculo_id).first()

                # Guardar la prioridad actual del vehículo que estamos modificando
                prioridad_actual = vehiculo_actual.prioridad

                # Intercambiar prioridades
                vehiculo_actual.prioridad = nueva_prioridad
                vehiculo_actual.save()

                if vehiculo_con_prioridad:
                    vehiculo_con_prioridad.prioridad = prioridad_actual
                    vehiculo_con_prioridad.save()

                return Response(
                    {
                        'mensaje': 'Prioridades intercambiadas exitosamente',
                        'vehiculo_actual': {
                            'id': vehiculo_actual.id,
                            'nueva_prioridad': nueva_prioridad
                        },
                        'vehiculo_afectado': {
                            'id': vehiculo_con_prioridad.id if vehiculo_con_prioridad else None,
                            'nueva_prioridad': prioridad_actual if vehiculo_con_prioridad else None
                        }
                    },
                    status=status.HTTP_200_OK
                )