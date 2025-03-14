from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.item import GenItem
from general.models.item_impuesto import GenItemImpuesto
from general.serializers.item import GenItemSerializador, GenItemExcelSerializador
from general.serializers.item_impuesto import GenItemImpuestoSerializador, GenItemImpuestoDetalleSerializador
from rest_framework.decorators import action
from openpyxl import Workbook
from django.http import HttpResponse

class ItemViewSet(viewsets.ModelViewSet):
    queryset = GenItem.objects.all()
    serializer_class = GenItemSerializador
    permission_classes = [permissions.IsAuthenticated]

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
                return Response({'validacion': False}, status=status.HTTP_200_OK)
            else:
                return Response({'validacion': True}, status=status.HTTP_200_OK)            
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)        
        