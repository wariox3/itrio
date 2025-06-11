from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.item import GenItem
from general.models.item_impuesto import GenItemImpuesto
from contabilidad.models.cuenta import ConCuenta
from general.serializers.item import GenItemSerializador, GenItemListaSerializador
from general.serializers.item_impuesto import GenItemImpuestoSerializador, GenItemImpuestoDetalleSerializador
from general.filters.item import ItemFilter
from utilidades.utilidades import Utilidades
from utilidades.space_do import SpaceDo
from io import BytesIO
import base64
import openpyxl
import gc

class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter 
    queryset = GenItem.objects.all()   
    serializadores = {'lista': GenItemListaSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenItemSerializador
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
            exporter = ExportarExcel(serializer.data, sheet_name="itemes", filename="itemes.xlsx")
            return exporter.export()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, venta=False):
        raw = request.data
        venta = raw.get('venta')
        queryset = GenItem.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        itemSerializador = GenItemSerializador(item)
        itemImpuestos = GenItemImpuesto.objects.filter(item=pk)
        if venta:
            itemImpuestos = itemImpuestos.filter(impuesto__venta=True)
        itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
        itemRespuesta = itemSerializador.data
        itemRespuesta['impuestos'] = itemImpuestosSerializador.data
        return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        itemSerializador = GenItemSerializador(data=request.data)
        if itemSerializador.is_valid():
            item = itemSerializador.save()            
            impuestos = data.get('impuestos')
            if impuestos is not None:
                for impuesto in impuestos:                
                    datosImpuestoItem = {"item":item.id,"impuesto":impuesto['impuesto']}
                    itemImpuestoSerializador = GenItemImpuestoSerializador(data=datosImpuestoItem)
                    if itemImpuestoSerializador.is_valid():
                        itemImpuestoSerializador.save()                
            itemImpuestos = GenItemImpuesto.objects.filter(item=item.id)
            itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
            itemRespuesta = itemSerializador.data
            itemRespuesta['impuestos'] = itemImpuestosSerializador.data
            return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        raw = request.data
        item = self.get_object()    
        itemSerializador = self.serializer_class(instance=item, data=raw, partial=True)
        if itemSerializador.is_valid():
            itemSerializador.save()
            impuestosNuevos = raw.get('impuestos')
            if impuestosNuevos is not None:
                for impuesto in impuestosNuevos:                
                    impuesto['item'] = item.id
                    itemImpuestoSerializador = GenItemImpuestoSerializador(data=impuesto)
                    if itemImpuestoSerializador.is_valid():
                        itemImpuestoSerializador.save() 
            impuestosEliminados = raw.get('impuestos_eliminados')
            if impuestosEliminados is not None:
                for itemImpuestoEliminado in impuestosEliminados:                                
                    itemImpuesto = GenItemImpuesto.objects.get(pk=itemImpuestoEliminado)
                    itemImpuesto.delete()
            itemImpuestos = GenItemImpuesto.objects.filter(item=item.id)
            itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
            itemRespuesta = itemSerializador.data
            itemRespuesta['impuestos'] = itemImpuestosSerializador.data                    
            return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Obtén todos los campos relacionados del modelo
        related_objects = []
        for related_object in instance._meta.related_objects:
            related_manager = getattr(instance, related_object.get_accessor_name())
            if related_manager.exists():
                related_objects.append(related_object.related_model.__name__)

        if related_objects:
            # Si hay relaciones, devuelve un mensaje indicando dónde se usa
            relaciones_texto = ', '.join(related_objects)
            return Response(
                {
                    'mensaje': f"El registro no se puede eliminar porque tiene registros asociados en: {relaciones_texto}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Si no hay relaciones, elimina el objeto
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path=r'detalle',)
    def detalle(self, request):
        raw = request.data
        id = raw.get('id')
        venta = raw.get('venta')
        compra = raw.get('compra')
        if(id):
            queryset = GenItem.objects.all()
            item = get_object_or_404(queryset, pk=id)
            itemSerializador = GenItemSerializador(item)
            itemImpuestos = GenItemImpuesto.objects.filter(item=id)
            if venta:
                itemImpuestos = itemImpuestos.filter(impuesto__venta=True)
            if compra:
                itemImpuestos = itemImpuestos.filter(impuesto__compra=True)
            itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
            itemRespuesta = itemSerializador.data
            itemRespuesta['impuestos'] = itemImpuestosSerializador.data
            return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'validar-uso',)
    def validar_uso(self, request):
        raw = request.data
        id = raw.get('id')        
        if id:            
            movimientos = GenDocumentoDetalle.objects.filter(item_id=id).first()
            if movimientos:
                return Response({'uso': True}, status=status.HTTP_200_OK)
            else:
                return Response({'uso': False}, status=status.HTTP_200_OK)            
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)        
        
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
                return Response({'mensaje': 'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)  
            
            cuentas_map = {c.codigo: c.id for c in ConCuenta.objects.all()}
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'nombre': row[0],
                    'codigo': row[1],
                    'referencia': row[2],
                    'costo': row[3],
                    'precio': row[4],
                    'inventario': row[5],
                    'producto': row[6],
                    'servicio': row[7],
                    'cuenta_venta': str(row[8]),
                    'cuenta_compra': str(row[9]),
                    'negativo': row[10],
                    'venta': row[11],
                    'impuesto_venta': row[12],
                    'impuesto_compra': row[13],
                }

                data['cuenta_venta'] = cuentas_map.get(data['cuenta_venta'])
                data['cuenta_compra'] = cuentas_map.get(data['cuenta_compra'])  
                    
                serializer = GenItemSerializador(data=data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    data_modelo.append((validated_data, data['impuesto_venta'], data['impuesto_compra']))
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }                                    
                    errores_datos.append(error_dato)    

            if not errores:
                for detalle, impuesto_venta, impuesto_compra in data_modelo:
                    item = GenItem.objects.create(**detalle)
                    
                    # Procesar impuesto_venta
                    if impuesto_venta:
                        datos_impuesto_venta = {"item": item.id, "impuesto": impuesto_venta}
                        item_impuesto_venta_serializer = GenItemImpuestoSerializador(data=datos_impuesto_venta)
                        if item_impuesto_venta_serializer.is_valid():
                            item_impuesto_venta_serializer.save()

                    # Procesar impuesto_compra
                    if impuesto_compra:
                        datos_impuesto_compra = {"item": item.id, "impuesto": impuesto_compra}
                        item_impuesto_compra_serializer = GenItemImpuestoSerializador(data=datos_impuesto_compra)
                        if item_impuesto_compra_serializer.is_valid():
                            item_impuesto_compra_serializer.save()

                    registros_importados += 1

                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje': 'Errores de validacion', 'codigo': 1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje': 'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'cargar-imagen',)
    def cargar_imagen(self, request):
        raw = request.data
        id = raw.get('id')
        base64 = raw.get('base64')        
        if id and base64:
            try:                            
                item = GenItem.objects.get(pk=id)
            except GenItem.DoesNotExist:
                return Response({'mensaje':'El item no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
            
            try:                                        
                objeto_base64 = Utilidades.separar_base64(base64)
                ruta_destino = f"itrio/imagen/{request.tenant.id}/item/{id}.{objeto_base64['extension']}"
                spaceDo = SpaceDo()
                spaceDo.putB64(ruta_destino, objeto_base64['base64_raw'], objeto_base64['content_type']) 
                item.imagen = ruta_destino
                item.save()
                return Response({'mensaje': 'Imagen cargada'}, status=status.HTTP_200_OK)                      
            except ValueError as e:
                return Response({'mensaje': str(e), 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)             
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)        
    