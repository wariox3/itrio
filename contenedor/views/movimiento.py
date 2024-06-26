from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contenedor.models import ContenedorMovimiento, EventoPago
from seguridad.models import User
from contenedor.serializers.movimiento import ContenedorMovimientoSerializador
from decouple import config
from datetime import timedelta, datetime
from django.utils import timezone
import hashlib
from decimal import Decimal

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
            movimientos = ContenedorMovimiento.objects.filter(usuario_id=usuario_id, tipo='FACTURA', vr_saldo__gt=0)
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
        estado=transaccion.get('status')
        valor=transaccion.get('amount_in_cents')
        valor=valor/100
        referencia=transaccion.get('reference')
        evento_pago = EventoPago(
            fecha=timezone.now().date(),
            evento=evento,
            entorno=entorno,
            transaccion=transaccion.get('id'),
            metodo_pago=transaccion.get('payment_method_type'),
            referencia=referencia,
            estado=estado,
            correo=transaccion.get('customer_email'),
            fecha_transaccion=fecha_transaccion
        )
        evento_pago.save()
        if estado == 'APPROVED':
                recibo = ContenedorMovimiento(
                    tipo = "RECIBO",
                    fecha = timezone.now().date(),
                    fecha_vence = timezone.now().date(),
                    contenedor_movimiento_id=referencia,
                    vr_total = valor,
                    vr_saldo = 0,                    
                )
                recibo.save()
                valor = Decimal(valor)                
                factura = ContenedorMovimiento.objects.get(id=referencia)
                if factura:
                    factura.vr_afectado = factura.vr_afectado + valor
                    factura.vr_saldo =  factura.vr_saldo - valor
                    factura.save()
                    usuario = User.objects.get(pk=factura.usuario_id)
                    if usuario:
                        usuario.vr_saldo -= valor
                        usuario.save()
        return Response(status=status.HTTP_200_OK)     