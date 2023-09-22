from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from inquilino.models import InquilinoMovimiento, Consumo
from inquilino.serializers.movimiento import InquilinoMovimientoSerializador
from seguridad.models import User
from django.db.models import Sum, Max, Q
from datetime import datetime, timedelta
from django.utils import timezone

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = InquilinoMovimiento.objects.all()
    serializer_class = InquilinoMovimientoSerializador    
    permission_classes = [permissions.IsAuthenticated]    

    @action(detail=False, methods=["post"], url_path=r'generar-factura',)
    def generar_factura(self, request):
        raw = request.data
        fechaDesde = raw.get('fechaDesde')
        fechaHasta = raw.get('fechaHasta')
        if fechaDesde and fechaHasta:
            consumosUsuarios = Consumo.objects.values('usuario_id').filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta)).annotate(
                vr_total=Sum('vr_total'))
            facturas = []
            for consumoUsuario in consumosUsuarios:
                movimiento = InquilinoMovimiento(
                    tipo = "FACTURA",
                    fecha = timezone.now().date(),
                    vr_total = consumoUsuario['vr_total'],
                    vr_saldo = consumoUsuario['vr_total'],
                    usuario_id = consumoUsuario['usuario_id']
                )
                facturas.append(movimiento)
                usuario = User.objects.get(pk=consumoUsuario['usuario_id'])
                usuario.vr_saldo += consumoUsuario['vr_total']
                usuario.fecha_limite_pago = datetime.now().date() + timedelta(days=3)
                usuario.save()
            InquilinoMovimiento.objects.bulk_create(facturas)
            return Response({'proceso':True}, status=status.HTTP_200_OK)  
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)  
        
    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:
            movimientos = InquilinoMovimiento.objects.filter(usuario_id=usuario_id)
            movimientosSerializador = InquilinoMovimientoSerializador(movimientos, many=True)
            return Response({'movimientos':movimientosSerializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)      