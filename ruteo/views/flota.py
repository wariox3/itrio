from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.flota import RutFlota
from ruteo.models.vehiculo import RutVehiculo
from ruteo.serializers.flota import RutFlotaSerializador
from django.db import transaction
from django.db.models import Max
from django.db import transaction

class RutFlotaViewSet(viewsets.ModelViewSet):
    queryset = RutFlota.objects.all()
    serializer_class = RutFlotaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        vehiculo_id = request.data.get('vehiculo')
        if not vehiculo_id:
            return Response({'error': 'vehiculo es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehiculo = RutVehiculo.objects.get(id=vehiculo_id)
        except RutVehiculo.DoesNotExist:
            return Response({'error': 'Vehículo no existe.'}, status=status.HTTP_404_NOT_FOUND)

        flota = RutFlota(vehiculo=vehiculo, prioridad=0)
        flota.save()

        def actualizar_prioridad():
            with transaction.atomic():
                RutFlota.objects.select_for_update().first()  # Fuerza bloqueo
                
                max_prioridad = RutFlota.objects.aggregate(
                    max_val=Max('prioridad')
                )['max_val'] or 0
                
                RutFlota.objects.filter(id=flota.id).update(
                    prioridad=max_prioridad + 1
                )

        transaction.on_commit(actualizar_prioridad)

        serializer = self.get_serializer(flota)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path=r'cambiar-prioridad')
    def cambiar_prioridad(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
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

                # Obtener el conteo total de vehículos en la flota (usando el nombre correcto de la relación)
                total_vehiculos = RutVehiculo.objects.filter(flotas_vehiculo_rel__isnull=False).count()

                # Validar que la nueva prioridad esté dentro del rango permitido
                if nueva_prioridad < 1 or nueva_prioridad > total_vehiculos:
                    return Response(
                        {
                            'mensaje': f'La prioridad debe estar entre 1 y {total_vehiculos}', 'codigo':15,
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

            except Exception as e:
                return Response(
                    {'error': f'Error al intercambiar prioridades: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )