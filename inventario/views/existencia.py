from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from inventario.models.existencia import InvExistencia
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
                existencia = InvExistencia.objects.filter(almacen_id=detalle['almacen'], item_id=detalle['item']).first()
                if existencia:
                    saldo = existencia.disponible - detalle['cantidad']
                    if saldo < 0:
                        return Response({'mensaje':f'El disponible {existencia.disponible} del item {detalle["item"]} es insuficiente para descontar {detalle["cantidad"]}', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':f'El disponible 0 del item {detalle["item"]} es insuficiente', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'validar': True}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    