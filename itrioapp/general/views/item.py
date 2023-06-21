from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.item import Item
from general.serializers.item import ItemSerializer
from general.serializers.item_impuesto import ItemImpuestoSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        data = request.data
        nombreSolo = data.get('nombre')
        impuestos = data.get('impuestos')
        serializador = ItemSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()
            print(request)
            for impuesto in impuestos:
                prueba = 1
                print(impuesto['impuesto_id'])
            return Response({'mensaje':'Es valido'}, status=status.HTTP_200_OK)
        return Response({'mensaje':'No es valido'}, status=status.HTTP_200_OK)

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