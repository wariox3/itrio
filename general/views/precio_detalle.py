from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from general.models.precio_detalle import GenPrecioDetalle
from general.models.item import GenItem
from general.serializers.precio_detalle import GenPrecioDetalleSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.filters.precio_detalle import PrecioDetalleFilter
from rest_framework.response import Response
import base64
import openpyxl
from io import BytesIO
import gc

class PrecioDetalleViewSet(viewsets.ModelViewSet):
    queryset = GenPrecioDetalle.objects.all()
    serializer_class = GenPrecioDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]    
    filterset_class = PrecioDetalleFilter 
    serializadores = {
        'lista': GenPrecioDetalleSerializador
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenPrecioDetalleSerializador
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
        if request.query_params.get('lista', '').lower() == 'true':
            self.pagination_class = None
        return super().list(request, *args, **kwargs)    
    
    @action(detail=False, methods=["get"], url_path=r'consultar_precio')
    def consultar_precio(self, request):
        precio_id = request.query_params.get('precio_id', None)
        item_id = request.query_params.get('item_id', None)
        
        if precio_id and item_id:        
            try:
                precio_detalle = GenPrecioDetalle.objects.filter(precio_id=precio_id,item_id=item_id).order_by('id').first()
                if precio_detalle:
                    return Response({'vr_precio': precio_detalle.vr_precio}, status=status.HTTP_200_OK)
                else:
                    return Response({'vr_precio': None}, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({'mensaje': 'Error procesando la api', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)              
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                
    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data        
        precio_id = raw.get('precio_id')
        archivo_base64 = raw.get('archivo_base64')
        if precio_id and archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({'mensaje': 'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)  
                        
            #itemes_map = {int(i.id): i for i in GenItem.objects.all()}
            itemes_map = set(GenItem.objects.values_list('id', flat=True))
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'precio': precio_id,
                    'item': row[0],                    
                    'vr_precio': row[1]                    
                }

                if data['vr_precio'] is not None:
                    try:
                        precio_str = str(data['vr_precio'])
                        if '.' in precio_str:
                            decimal_part = precio_str.split('.')[1]
                            if len(decimal_part) > 2:
                                errores = True
                                error_dato = {
                                    'fila': i,
                                    'errores': {'precio': ['No puede tener más de 2 decimales']}
                                }                                    
                                errores_datos.append(error_dato)
                                continue
                    except (ValueError, TypeError):
                        errores = True
                        error_dato = {
                            'fila': i,
                            'errores': {'precio': ['Formato inválido']}
                        }                                    
                        errores_datos.append(error_dato)
                        continue                
   
                if data['item'] not in itemes_map:
                    data['item'] = None                               
                serializer = GenPrecioDetalleSerializador(data=data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    data_modelo.append((validated_data))
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }                                    
                    errores_datos.append(error_dato)   

            if not errores:
                for detalle in data_modelo:
                    GenPrecioDetalle.objects.create(**detalle)
                    registros_importados += 1

                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje': 'Errores de validacion', 'codigo': 1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje': 'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                