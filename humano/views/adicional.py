from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.adicional import HumAdicional
from humano.models.programacion import HumProgramacion
from humano.models.contrato import HumContrato
from humano.serializers.adicional import HumAdicionalSerializador
from io import BytesIO
import base64
import openpyxl
import gc
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from humano.filters.adicional import AdicionalFilter
from utilidades.excel_exportar import ExcelExportar

class HumAdicionalViewSet(viewsets.ModelViewSet):
    queryset = HumAdicional.objects.all()
    serializer_class = HumAdicionalSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdicionalFilter 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumAdicionalSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('excel'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            exporter = ExcelExportar(serializer.data, nombre_hoja="adicionales", nombre_archivo="adicionales.xlsx", titulo="Adicionales")            
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        permanente = raw.get('permanente')
        if archivo_base64:
            if permanente == True:
                programacion_id = None
            else:
                programacion_id = raw.get('programacion_id', None)
                if programacion_id:
                    programacion = HumProgramacion.objects.filter(id=programacion_id).first()
                    if not programacion:
                        return Response({'mensaje':'La programacion no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
                else:
                   return Response({'mensaje':'Si el adicional no es permanente debe tener el id de la programacion', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'programacion': programacion_id,
                    'identificacion': row[0],
                    'contrato':row[1],
                    'concepto':row[2],
                    'valor':row[3],
                    'detalle':row[4],
                    'aplica_dia_laborado':row[5],
                    'permanente': permanente
                }  
                if data['contrato'] is None:
                    if data['identificacion'] is not None:
                        contrato = HumContrato.objects.filter(contacto__numero_identificacion=data['identificacion']).order_by('-fecha_desde').first()
                        if contrato:
                            data['contrato'] = contrato.id

                serializer = HumAdicionalSerializador(data=data)
                if serializer.is_valid():
                    data_modelo.append(serializer.validated_data)
                    registros_importados += 1
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }
                    errores_datos.append(error_dato)                                
            if not errores:
                for detalle in data_modelo:
                    HumAdicional.objects.create(**detalle)
                gc.collect()
                return Response({'mensaje': f"Se importaron {registros_importados} con éxito"}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)                                 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     