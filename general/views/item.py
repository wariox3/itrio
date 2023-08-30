from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from general.models.item import Item
from general.models.item_impuesto import ItemImpuesto
from general.serializers.item import ItemSerializador
from general.serializers.item_impuesto import ItemImpuestoSerializador
from rest_framework.decorators import action
from django.db.models import Count, Q, F

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializador
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        itemSerializador = ItemSerializador(item)
        itemImpuestos = ItemImpuesto.objects.filter(item=pk)
        itemImpuestosSerializador = ItemImpuestoSerializador(itemImpuestos, many=True)
        itemRespuesta = itemSerializador.data
        itemRespuesta['impuestos'] = itemImpuestosSerializador.data
        return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        itemSerializador = ItemSerializador(data=request.data)
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
            for impuesto in impuestosEliminar:                
                impuestoEliminar = ItemImpuesto.objects.get(item_id=pk, impuesto_id=impuesto)
                impuestoEliminar.delete()            
            return Response({'item':itemSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        cantidadLimite = raw.get('cantidad_limite', 5000)    
        filtros = raw.get('filtros')
        ordenamientos = raw.get('ordenamientos')
        items = Item.objects.all()
        if filtros:
            for filtro in filtros:
                items = items.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            items = items.order_by(*ordenamientos)              
        items = items[desplazar:limite+desplazar]
        itemsCantidad = Item.objects.all()[:cantidadLimite].count()
        #consumos = Item.objects.aggregate(cantidad=Count('id'))
        #consulta_sql = str(items.query)
        #print(consulta_sql)
        ItemSerializador = ItemSerializador(items, many=True)
        return Response({"registros": ItemSerializador.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
