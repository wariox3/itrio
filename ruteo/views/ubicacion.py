from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.ubicacion import RutUbicacion
from ruteo.models.despacho import RutDespacho
from ruteo.serializers.ubicacion import RutUbicacionSerializador

class RutUbicacionViewSet(viewsets.ModelViewSet):
    queryset = RutUbicacion.objects.all()
    serializer_class = RutUbicacionSerializador
    permission_classes = [permissions.IsAuthenticated]
            
    def perform_create(self, serializer):
        ubicacion = serializer.save()        
        if ubicacion.despacho:
            ubicacion.despacho.fecha_ubicacion = ubicacion.fecha
            ubicacion.despacho.latitud = ubicacion.latitud
            ubicacion.despacho.longitud = ubicacion.longitud
            ubicacion.despacho.save()
            
            '''RutDespacho.objects.filter(id=ubicacion.despacho.id).update(
                latitud=ubicacion.latitud,
                longitud=ubicacion.longitud,
                fecha_ubicacion=ubicacion.fecha
            )'''      