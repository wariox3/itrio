from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.ubicacion import RutUbicacion
from ruteo.models.despacho import RutDespacho
from ruteo.serializers.ubicacion import RutUbicacionSerializador
from django.db.models import F
from shapely.geometry import Point
from decouple import config
import requests

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
        
        '''if despacho:           
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
                    return Response({'creado':True}, status=status.HTTP_200_OK)'''                
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

    @action(detail=False, methods=["post"], url_path=r'autocompletar')
    def autocompletar(self, request):
        try:
            input_text = request.data.get('input', {}).get('input', '')
            if not input_text:
                return Response(
                    {'mensaje': 'El parámetro "input" es requerido', 'error': True},
                    status=status.HTTP_400_BAD_REQUEST
                )

            country = request.GET.get('country', 'co')
            api_key = config('GOOGLE_MAPS_API_KEY')
            
            url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
            params = {
                'input': input_text,
                'key': api_key,
                'components': f'country:{country}',
                'types': 'address'
            }
            
            response = requests.get(url, params=params)
            google_data = response.json()

            if google_data.get('status') != 'OK':
                return Response(
                    {'mensaje': 'No se encontraron resultados', 'error': False, 'predictions': []},
                    status=status.HTTP_200_OK
                )

            return Response({
                'mensaje': 'Proceso exitoso',
                'predictions': google_data.get('predictions', [])
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'mensaje': f'Error en el servidor: {str(e)}', 'error': True},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"], url_path=r'detalle')
    def place_details(self, request):
        try:
            place_id = request.data.get('place_id', '')
            if not place_id:
                return Response(
                    {'mensaje': 'El parámetro "place_id" es requerido', 'error': True},
                    status=status.HTTP_400_BAD_REQUEST
                )

            api_key = config('GOOGLE_MAPS_API_KEY')
            
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'key': api_key,
                'fields': 'formatted_address,geometry'
            }
            
            response = requests.get(url, params=params)
            google_data = response.json()

            if google_data.get('status') != 'OK':
                return Response(
                    {'mensaje': 'No se encontraron detalles para el lugar', 'error': True},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extraemos los datos relevantes
            result = google_data.get('result', {})
            geometry = result.get('geometry', {}).get('location', {})
            
            return Response({
                'mensaje': 'Proceso exitoso',
                'error': False,
                'data': {
                    'address': result.get('formatted_address', ''),
                    'latitude': geometry.get('lat'),
                    'longitude': geometry.get('lng')
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'mensaje': f'Error en el servidor: {str(e)}', 'error': True},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )