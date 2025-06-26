from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.activo import ConActivo
from contabilidad.models.cuenta import ConCuenta
from contabilidad.serializers.activo import ConActivoSerializador
from django.db.models import ProtectedError
from datetime import datetime
from io import BytesIO
import base64
import openpyxl
import gc
import os
from decimal import Decimal
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from contabilidad.filters.activo import ActivoFilter
from utilidades.excel_exportar import ExcelExportar

class ActivoViewSet(viewsets.ModelViewSet):
    queryset = ConActivo.objects.all()
    serializer_class = ConActivoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ActivoFilter 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return ConActivoSerializador
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
            exporter = ExcelExportar(serializer.data, sheet_name="activos", filename="activos.xlsx")
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   

    def calcular_depreciacion_periodo(self, valor_compra, duracion):
        if duracion > 0:
            return valor_compra / duracion
        return 0

    def perform_create(self, serializer):
        raw = self.request.data
        valor_compra = Decimal(raw.get('valor_compra'))
        duracion = int(raw.get('duracion'))
        depreciacion_inicial = Decimal(raw.get('depreciacion_inicial'))
        depreciacion_periodo = self.calcular_depreciacion_periodo(valor_compra, duracion)
        depreciacion_saldo = valor_compra - depreciacion_inicial
        serializer.save(depreciacion_periodo=depreciacion_periodo, depreciacion_saldo=depreciacion_saldo)

    def perform_update(self, serializer):
        raw = self.request.data
        valor_compra = Decimal(raw.get('valor_compra'))
        duracion = int(raw.get('duracion'))
        depreciacion_periodo = self.calcular_depreciacion_periodo(valor_compra, duracion)
        serializer.save(depreciacion_periodo=depreciacion_periodo, depreciacion_saldo=valor_compra)
        
    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            cuentas_map = {c.codigo: c.id for c in ConCuenta.objects.all()}
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'codigo': row[0],
                    'nombre':row[1],
                    'marca': row[2],
                    'serie': row[3],
                    'modelo': row[4],                                        
                    'duracion': row[8],
                    'valor_compra': row[9],
                    'depreciacion_inicial': row[10],
                    'activo_grupo': row[11],
                    'cuenta_depreciacion': str(row[12]),
                    'cuenta_gasto': str(row[13]),
                    'grupo': row[14],
                    'metodo_depreciacion': row[15],
                }  

                data['cuenta_gasto'] = cuentas_map.get(data['cuenta_gasto'])
                data['cuenta_depreciacion'] = cuentas_map.get(data['cuenta_depreciacion'])

                if row[5]:                        
                    fecha_valida = datetime.strptime(str(row[5]), "%Y%m%d").date()
                    data['fecha_compra'] = fecha_valida
                if row[6]:                        
                    fecha_valida = datetime.strptime(str(row[6]), "%Y%m%d").date()
                    data['fecha_activacion'] = fecha_valida 
                if row[7]:                        
                    fecha_valida = datetime.strptime(str(row[7]), "%Y%m%d").date()
                    data['fecha_baja'] = fecha_valida                     

                valor_compra = Decimal(data['valor_compra'])
                depreciacion_inicial = Decimal(data['depreciacion_inicial'])
                duracion = int(data['duracion'])
                if duracion > 0:                    
                    data['depreciacion_periodo'] = round(valor_compra / duracion, 6)
                data['depreciacion_saldo'] = valor_compra - depreciacion_inicial
                
                serializer = ConActivoSerializador(data=data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
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
                    ConActivo.objects.create(**detalle)
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        