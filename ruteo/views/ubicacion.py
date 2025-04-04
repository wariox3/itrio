from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.ubicacion import RutUbicacion
from ruteo.models.despacho import RutDespacho
from ruteo.serializers.ubicacion import RutUbicacionSerializador
from django.db.models import F
from shapely.geometry import Point

class RutUbicacionViewSet(viewsets.ModelViewSet):
    queryset = RutUbicacion.objects.all()
    serializer_class = RutUbicacionSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        latitud = serializer.validated_data.get('latitud')
        longitud = serializer.validated_data.get('longitud')
        despacho = serializer.validated_data.get('despacho')
        
        if despacho:           
            ultima_ubicacion = RutUbicacion.objects.filter(despacho=despacho).order_by('-fecha').first()            
            if ultima_ubicacion:            
                
                punto_nuevo = Point(longitud, latitud)  # Nota: Shapely usa (x,y) = (long,lat)
                punto_anterior = Point(ultima_ubicacion.longitud, ultima_ubicacion.latitud)                                
                distancia = punto_nuevo.distance(punto_anterior) * 111319.9
                
                if distancia <= 2:                    
                    ultima_ubicacion.detenido = F('detenido') + 1
                    ultima_ubicacion.save()
                                        
                    despacho.fecha_ubicacion = serializer.validated_data.get('fecha')
                    despacho.latitud = latitud
                    despacho.longitud = longitud
                    despacho.save()                    
                    return Response({'creado':True}, status=status.HTTP_200_OK)                
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)       

    def perform_create(self, serializer):
        ubicacion = serializer.save()        
        if ubicacion.despacho:
            ubicacion.despacho.fecha_ubicacion = ubicacion.fecha
            ubicacion.despacho.latitud = ubicacion.latitud
            ubicacion.despacho.longitud = ubicacion.longitud
            ubicacion.despacho.save()        