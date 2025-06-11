from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.archivo import GenArchivo
from general.models.documento import GenDocumento
from general.models.item import GenItem
from general.serializers.archivo import GenArchivoSerializador
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from utilidades.exportar_excel import ExportarExcel
from django.http import HttpResponse
from io import BytesIO

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = GenArchivo.objects.all()
    serializer_class = GenArchivoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        backblaze = Backblaze()
        backblaze.eliminar(instance.almacenamiento_id)    
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Refactorizar este método para usar archivo_servicio.py
    @action(detail=False, methods=["post"], url_path=r'cargar',)
    def cargar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        nombre_archivo = raw.get('nombre_archivo')
        documento_id = raw.get('documento_id')     
        codigo = raw.get('codigo', None)
        modelo = raw.get('modelo', None)
        if archivo_base64 and nombre_archivo and (documento_id or (codigo and modelo)):            
            try:
                documento = None
                if documento_id:
                    documento = GenDocumento.objects.get(pk=documento_id)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                 
                
            try:                        
                tenant = request.tenant.schema_name
                objeto_base64 = Utilidades.separar_base64(archivo_base64)
                backblaze = Backblaze()
                id, tamano, tipo, uuid = backblaze.subir(objeto_base64['base64_raw'], tenant, nombre_archivo)
                archivo = GenArchivo()
                archivo.archivo_tipo_id = 1
                archivo.almacenamiento_id = id
                archivo.documento = documento
                archivo.nombre = nombre_archivo
                archivo.tipo = tipo
                archivo.tamano = tamano
                archivo.uuid = uuid
                archivo.codigo = codigo
                archivo.modelo = modelo
                archivo.save()
                return Response({'id': str(archivo.id)}, status=status.HTTP_200_OK)                                         
            except ValueError as e:
                return Response({'mensaje': str(e), 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                                          
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

      
    @action(detail=False, methods=["post"], url_path=r'descargar',)
    def descargar(self, request):
        raw = request.data        
        id = raw.get('id')
        if id:
            try:
                archivo = GenArchivo.objects.get(pk=id)
                try:                                                                
                    backblaze = Backblaze()
                    contenido = backblaze.descargar(archivo.almacenamiento_id)          
                    response = HttpResponse(contenido, content_type=archivo.tipo)
                    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                    response['Content-Disposition'] = f'attachment; filename="{archivo.nombre}"'                    
                    return response                                                                                   
                except ValueError as e:
                    return Response({'mensaje': str(e), 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                   
            except GenArchivo.DoesNotExist:
                return Response({'mensaje':'El archivo no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                        
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        

     
          
      
    

