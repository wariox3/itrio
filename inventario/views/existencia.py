from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from inventario.models.existencia import InvExistencia
from general.models.item import GenItem
from inventario.serializers.existencia import InvExistenciaSerializador
from inventario.filters.existencia import InvExistenciaFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class InvExistenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = InvExistencia.objects.all()    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = InvExistenciaFilter 

    serializadores = {
        'informe_inventario_valorizado': InvExistenciaSerializador,
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return InvExistenciaSerializador
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

            if request.query_params.get('excel_masivo'):
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar() 
            elif request.query_params.get('excel_informe'): 
                serializador_parametro = self.request.query_params.get('serializador', None)                
                if serializador_parametro == 'informe_inventario_valorizado':
                    titulo = 'Inventario valorizado' 
                    nombre_archivo = "inventario_valorizado.xlsx"  
                    nombre_hoja = 'valorizado'      
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo, titulo)
                return exporter.exportar_informe()                    
            else:
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar_estilo()
        return super().list(request, *args, **kwargs) 


    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):        
        raw = request.data
        detalles = raw.get('detalles')
        if detalles: 
            for detalle in detalles:
                item = GenItem.objects.get(id=detalle['item'])
                if item:
                    if item.inventario:
                        existencia = InvExistencia.objects.filter(almacen_id=detalle['almacen'], item_id=detalle['item']).first()                
                        if existencia or item.negativo == False:
                            saldo = existencia.disponible - detalle['cantidad']
                            if saldo < 0:
                                if item.negativo == False:
                                    return Response({'mensaje':f'El item {detalle["item"]} tiene {existencia.disponible} cantidades disponibles, es insuficiente para descontar {detalle["cantidad"]}', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje':f'El item {detalle["item"]} tiene 0 cantidades disponibles', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                        
                else:
                    return Response({'mensaje':'El item no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
            return Response({'validar': True}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    