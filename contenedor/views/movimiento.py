from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contenedor.models import ContenedorMovimiento, Consumo
from contenedor.serializers.movimiento import ContenedorMovimientoSerializador
from seguridad.models import User
from django.db.models import Sum, Max, Q
from datetime import datetime, timedelta
from django.utils import timezone

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = ContenedorMovimiento.objects.all()
    serializer_class = ContenedorMovimientoSerializador    
    permission_classes = [permissions.IsAuthenticated]     
        
    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:
            movimientos = ContenedorMovimiento.objects.filter(usuario_id=usuario_id)
            movimientosSerializador = ContenedorMovimientoSerializador(movimientos, many=True)
            return Response({'movimientos':movimientosSerializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)      