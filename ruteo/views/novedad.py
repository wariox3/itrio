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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        imagenes = data.pop('imagenes', None)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            visita_id = serializer.validated_data['visita'].id
            try:
                visita = RutVisita.objects.get(pk=visita_id)
            except RutVisita.DoesNotExist:
                return Response({'mensaje': 'La visita no existe', 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
            if visita.estado_novedad:
                return Response({'mensaje': 'La visita ya tiene una novedad activa', 'codigo': 3}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                instance = serializer.save()
                visita.estado_novedad = True
                visita.save(update_fields=['estado_novedad'])
                if visita.despacho:
                    despacho = visita.despacho
                    despacho.visitas_novedad = despacho.visitas_novedad + 1
                    despacho.save(update_fields=['visitas_novedad'])

                if imagenes:
                    tenant = request.tenant.schema_name
                    for imagen in imagenes:
                        objeto_base64 = Utilidades.separar_base64(imagen['base64'])
                        nombre_archivo = f'{instance.id}.{objeto_base64["extension"]}'
                        ArchivoServicio.cargar_modelo(objeto_base64['base64_raw'],nombre_archivo,instance.id,"RutNovedad",tenant)
            return Response({'mensaje': 'Se crea la nueva novedad'}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'Errores de validación', 'errores_validador': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

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
                    visita = RutVisita.objects.get(pk=novedad.visita_id)
                    visita.estado_novedad = False
                    visita.save(update_fields=['estado_novedad'])                        
                    if visita.despacho:
                        despacho = visita.despacho
                        despacho.visitas_novedad = despacho.visitas_novedad - 1
                        despacho.save(update_fields=['visitas_novedad'])
                    return Response({'mensaje': f'Se soluciono la novedad'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La novedad ya esta solucionada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
        

