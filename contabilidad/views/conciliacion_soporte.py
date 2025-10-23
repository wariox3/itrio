from rest_framework import viewsets, permissions, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.conciliacion import ConConciliacion
from contabilidad.models.conciliacion_soporte import ConConciliacionSoporte
from contabilidad.serializers.conciliacion_soporte import ConConciliacionSoporteSerializador
from contabilidad.filters.conciliacion_soporte import ConciliacionSoporteFilter
from utilidades.excel_exportar import ExcelExportar
import base64
from io import BytesIO
import openpyxl
import gc
from datetime import datetime


class ConciliacionSoporteViewSet(viewsets.ModelViewSet):
    queryset = ConConciliacionSoporte.objects.all()
    serializer_class = ConConciliacionSoporteSerializador
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConciliacionSoporteFilter 
    permission_classes = [permissions.IsAuthenticated]
    serializadores = {'lista': ConConciliacionSoporteSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return ConConciliacionSoporteSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="conciliaciones_soportes", nombre_archivo="conciliacionesSoportes.xlsx", titulo="ConciliacionesSoportes")            
            return exporter.exportar()
        return super().list(request, *args, **kwargs)    
           
    @action(detail=False, methods=["post"], url_path=r'cargar-soporte',)
    def cargar_soporte(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        id = raw.get('id')
        if archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 

            conciliacion = ConConciliacion.objects.filter(pk=id).first()
            if not conciliacion:
                return Response({'mensaje': 'Conciliación no encontrada.', 'codigo': 2}, status=status.HTTP_404_NOT_FOUND)             
            
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                errores_fila = {}
                fecha_raw = row[0]
                valor_raw = row[1]
                descripcion_raw = row[2] if len(row) > 2 else ''

                fecha = None
                if not fecha_raw:
                    errores_fila["fecha"] = ["Este campo no puede ser nulo."]
                else:
                    try:
                        if isinstance(fecha_raw, datetime):
                            fecha = fecha_raw.date()
                        else:
                            fecha = datetime.strptime(str(fecha_raw).strip(), "%Y%m%d").date()
                    except Exception:
                        errores_fila["fecha"] = ["La fecha no es válida (formato esperado YYYYMMDD)."]

                if valor_raw is None or valor_raw == '':
                    errores_fila["valor"] = ["Este campo no puede ser nulo."]
                elif not isinstance(valor_raw, (int, float)):
                    errores_fila["valor"] = ["El valor debe ser numérico."]

                if errores_fila:
                    errores = True
                    errores_datos.append({'fila': i, 'errores': errores_fila})
                    continue

                debito = valor_raw if valor_raw >= 0 else 0
                credito = abs(valor_raw) if valor_raw < 0 else 0
                descripcion = str(descripcion_raw or '')[:300]

                data = {
                    'fecha': fecha,
                    'detalle': descripcion,
                    'debito': debito,
                    'credito': credito,
                    'conciliacion': conciliacion.id,
                }
                  

                serializer = ConConciliacionSoporteSerializador(data=data)
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
                    ConConciliacionSoporte.objects.create(**detalle)
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
    