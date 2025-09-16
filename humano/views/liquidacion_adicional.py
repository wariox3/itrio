from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.liquidacion_adicional import HumLiquidacionAdicional
from humano.serializers.liquidacion_adicional import HumLiquidacionAdicionalSerializador
from humano.filters.liquidacion_adicional import LiquidacionAdicionalFilter
from utilidades.excel_exportar import ExcelExportar
from humano.servicios.liquidacion import LiquidacionServicio
from django.db import transaction

class HumLiquidacionAdicionalViewSet(viewsets.ModelViewSet):
    queryset = HumLiquidacionAdicional.objects.all()
    serializer_class = HumLiquidacionAdicionalSerializador
    permission_classes = [permissions.IsAuthenticated]   
    filterset_class = LiquidacionAdicionalFilter 
    serializadores = {
        'lista': HumLiquidacionAdicionalSerializador,
        }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumLiquidacionAdicionalSerializador
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
            titulo = 'Informe programacion detalles'
            nombre_hoja = "programacion_detalles"
            nombre_archivo = "programacion_detalles.xlsx"
            if request.query_params.get('excel_masivo'):
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar() 
            elif request.query_params.get('excel_informe'): 
                serializador_parametro = self.request.query_params.get('serializador', None)                
                if serializador_parametro == 'informe_programacion_detalle':
                    titulo = 'Programación detalles' 
                    nombre_archivo = "programación_detalles.xlsx"  
                    nombre_hoja = 'programación_detalles'    
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo, titulo)
                return exporter.exportar_informe()                    
            else:
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar_estilo()            
        return super().list(request, *args, **kwargs)     
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        liquidacion_adicional = serializer.save()        
        liquidacion = liquidacion_adicional.liquidacion        
        LiquidacionServicio.liquidar(liquidacion)
    
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)    

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()    
        liquidacion = instance.liquidacion    
        self.perform_destroy(instance)
        LiquidacionServicio.liquidar(liquidacion)        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()