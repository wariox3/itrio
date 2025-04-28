from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.novedad import RutNovedad
from ruteo.models.visita import RutVisita
from ruteo.serializers.novedad import RutNovedadSerializador
from django.db import transaction
from django.utils import timezone
from utilidades.utilidades import Utilidades
from servicios.archivo_servicio import ArchivoServicio

class RutNovedadViewSet(viewsets.ModelViewSet):
    queryset = RutNovedad.objects.all()
    serializer_class = RutNovedadSerializador
    permission_classes = [permissions.IsAuthenticated]  

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            novedad = serializer.save()
            visita = novedad.visita
            visita.estado_novedad = True
            visita.save(update_fields=['estado_novedad'])
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
      
    @action(detail=False, methods=["post"], url_path=r'solucionar',)
    def solucionar(self, request):             
        raw = request.data
        id = raw.get('id')  
        solucion = raw.get('solucion')  
        if id:
            try:
                novedad = RutNovedad.objects.get(pk=id)                            
            except RutNovedad.DoesNotExist:
                return Response({'mensaje':'La novedad no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            
            if novedad.estado_solucion == False:                
                with transaction.atomic():
                    novedad.estado_solucion = True
                    novedad.fecha_solucion = timezone.now() 
                    novedad.solucion = solucion
                    novedad.save()                
                    pendientes = RutNovedad.objects.filter(visita_id=novedad.visita_id, estado_solucion=False).exclude(pk=novedad.pk).exists()                
                    if not pendientes:
                        visita = RutVisita.objects.get(pk=novedad.visita_id)
                        visita.estado_novedad = False
                        visita.save(update_fields=['estado_novedad'])                        
                    return Response({'mensaje': f'Se soluciono la novedad'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La novedad ya esta solucionada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
        
    @action(detail=False, methods=["post"], url_path=r'nuevo',)
    def nuevo(self, request):             
        raw = request.data
        imagenes = raw.get('imagenes')
        
        if imagenes:
            tenant = request.tenant.schema_name
            for imagen in imagenes:                                                
                objeto_base64 = Utilidades.separar_base64(imagen['base64'])
                nombre_archivo = f'{id}.{objeto_base64["extension"]}'
                respuesta = ArchivoServicio.cargar_modelo(objeto_base64['base64_raw'], nombre_archivo, id, "RutNovedad", tenant)     