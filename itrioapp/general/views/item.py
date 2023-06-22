from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.item import Item
from general.models.item_impuesto import ItemImpuesto
from general.serializers.item import ItemSerializer
from general.serializers.item_impuesto import ItemImpuestoSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        data = request.data
        itemSerializador = ItemSerializer(data=request.data)
        if itemSerializador.is_valid():
            item = itemSerializador.save()            
            impuestos = data.get('impuestos')
            for impuesto in impuestos:                
                datosImpuestoItem = {"item":item.id,"impuesto":impuesto}                                
                itemImpuestoSerializador = ItemImpuestoSerializer(data=datosImpuestoItem)
                if itemImpuestoSerializador.is_valid():
                    itemImpuestoSerializador.save()                
            return Response({'item':itemSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        item = self.get_object()
        data = {"nombre": request.data.get('nombre')}
        itemSerializador = self.serializer_class(instance=item, data=data, partial=True)
        if itemSerializador.is_valid():
            itemSerializador.save()
            itemImpuestos = ItemImpuesto.objects.filter(item_id=pk).values('impuesto')        
            impuestosActuales = set(itemImpuestos.values_list('impuesto', flat=True))            
            impuestos = set(request.data.get('impuestos'))                    
            impuestosEliminar = impuestosActuales.difference(impuestos)  
            impuestosAdicionar = impuestos.difference(impuestosActuales)    
            for impuesto in impuestosAdicionar:                
                datosImpuestoItem = {"item":item.id,"impuesto":impuesto}                                
                itemImpuestoSerializador = ItemImpuestoSerializer(data=datosImpuestoItem)
                if itemImpuestoSerializador.is_valid():
                    itemImpuestoSerializador.save()
            return Response({'item':itemSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)

        if response is None:
            return None

        if response.status_code == 400:
            response.data = {
                'mensaje': 'Mensajes de validacion',
                'codigo': 14,
                'validacion': response.data
            }

        return response