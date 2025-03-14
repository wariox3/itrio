from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from inventario.models.existencia import InvExistencia
from general.models.item import GenItem
from inventario.serializers.existencia import InvExistenciaSerializador

class InvExistenciaViewSet(viewsets.ModelViewSet):
    queryset = InvExistencia.objects.all()
    serializer_class = InvExistenciaSerializador
    permission_classes = [permissions.IsAuthenticated]

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
                        if existencia:
                            saldo = existencia.disponible - detalle['cantidad']
                            if saldo < 0:
                                return Response({'mensaje':f'El item {detalle["item"]} tiene {existencia.disponible} cantidades disponibles, es insuficiente para descontar {detalle["cantidad"]}', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje':f'El item {detalle["item"]} tiene 0 cantidades disponibles', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                        
                else:
                    return Response({'mensaje':'El item no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
            return Response({'validar': True}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    