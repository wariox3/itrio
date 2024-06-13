from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contenedor.models import ContenedorMovimiento, EventoPago
from contenedor.serializers.movimiento import ContenedorMovimientoSerializador
from decouple import config
from datetime import timedelta, datetime
from django.utils import timezone
import hashlib

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

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'pendiente',)
    def pendiente(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:
            movimientos = ContenedorMovimiento.objects.filter(usuario_id=usuario_id, vr_saldo__gt=0)
            movimientosSerializador = ContenedorMovimientoSerializador(movimientos, many=True)
            return Response({'movimientos':movimientosSerializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
        
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'generar-integridad',)
    def generara_integridad(self, request):
        raw = request.data
        referencia = raw.get('referencia')
        monto = raw.get('monto')
        secreto_integridad = config('WOMPI_SECRETO_INTEGRIDAD')
        if referencia and monto:                                
            now = timezone.localtime(timezone.now())
            now = now + timedelta(minutes=10)
            fecha_vencimiento = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            cadena = referencia+monto+"COP"+secreto_integridad
            cadena_bytes = cadena.encode('utf-8')
            hash_obj = hashlib.sha256(cadena_bytes)
            hash_str = hash_obj.hexdigest()
            return Response({'hash':hash_str}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'evento-wompi',)
    def evento_wompi(self, request):
        raw = request.data
        evento = raw.get('event')
        entorno = raw.get('environment')
        data = raw.get('data')
        fecha_transaccion_parametro=raw.get('sent_at')
        fecha_transaccion_parametro = fecha_transaccion_parametro[:16]
        fecha_transaccion_parametro = fecha_transaccion_parametro.replace('T', ' ')
        fecha_transaccion = datetime.strptime(fecha_transaccion_parametro, '%Y-%m-%d %H:%M')
        transaccion=data.get('transaction')
        evento_pago = EventoPago(
            fecha=timezone.now().date(),
            evento=evento,
            entorno=entorno,
            transaccion=transaccion.get('id'),
            metodo_pago=transaccion.get('payment_method_type'),
            referencia=transaccion.get('reference'),
            estado=transaccion.get('status'),
            correo=transaccion.get('customer_email'),
            fecha_transaccion=fecha_transaccion
        )
        evento_pago.save()
        return Response(status=status.HTTP_200_OK)     