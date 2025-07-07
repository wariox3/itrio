from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from contenedor.models import CtnMovimiento, CtnEventoPago, CtnConsumo, CtnSocio
from contenedor.filters.movimiento import MovimientoFilter
from seguridad.models import User
from contenedor.serializers.movimiento import CtnMovimientoSerializador
from decouple import config
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Sum, Q, F
from django.http import HttpResponse
from decimal import Decimal
from utilidades.space_do import SpaceDo
import hashlib


class MovimientoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]     
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    queryset = CtnMovimiento.objects.all()
    serializer_class = CtnMovimientoSerializador  
    filterset_class = MovimientoFilter  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'generar-pedido',)
    def generar_pedido(self, request):
        raw = request.data
        fecha_desde = raw.get('fechaDesde')
        fecha_hasta = raw.get('fechaHasta')
        usuario_id = raw.get('usuario_id')
        if fecha_desde and fecha_hasta:                        
            consumos = CtnConsumo.objects.values('usuario_id'
                ).filter(
                    fecha__gte=fecha_desde,
                    fecha__lte=fecha_hasta,
                    cortesia=False
                ).annotate(
                    vr_total=Sum('vr_total'))
            if usuario_id:
                consumos.filter(usuario_id=usuario_id)
            facturas = []
            for consumo in consumos:
                total = round(consumo['vr_total'])
                usuario = User.objects.get(pk=consumo['usuario_id'])
                if usuario.vr_saldo <= 0:
                    if usuario.cortesia == False:
                        movimiento = CtnMovimiento(
                            tipo = "PEDIDO",
                            fecha = timezone.now(),
                            fecha_vence = datetime.now().date() + timedelta(days=3),
                            descripcion = 'SERVICIOS NUBE',
                            vr_total = total,
                            vr_saldo = total,
                            usuario_id = consumo['usuario_id'],
                            socio_id=usuario.socio_id
                        )
                        facturas.append(movimiento)                
                        usuario.vr_saldo += total
                        usuario.fecha_limite_pago = datetime.now().date() + timedelta(days=3)
                        usuario.save()
            CtnMovimiento.objects.bulk_create(facturas)
            return Response({'proceso':True}, status=status.HTTP_200_OK)  
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:
            movimientos = CtnMovimiento.objects.filter(usuario_id=usuario_id)
            movimientosSerializador = CtnMovimientoSerializador(movimientos, many=True)
            return Response({'movimientos':movimientosSerializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   

    @action(detail=False, methods=["post"], url_path=r'consulta-socio',)
    def consulta_socio(self, request):
        raw = request.data
        socio_id = raw.get('socio_id')
        if socio_id:
            movimientos = CtnMovimiento.objects.filter(socio_id=socio_id)
            movimientosSerializador = CtnMovimientoSerializador(movimientos, many=True)
            return Response({'movimientos':movimientosSerializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'consulta_credito',)
    def consulta_credito_action(self, request):
        raw = request.data
        socio_id = raw.get('socio_id')
        if socio_id:
            movimientos = CtnMovimiento.objects.filter(socio_id=socio_id).filter(
                Q(tipo='CREDITO') | Q(tipo='RECIBO_CREDITO')
            )
            movimientosSerializador = CtnMovimientoSerializador(movimientos, many=True)
            return Response({'movimientos':movimientosSerializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'pendiente',)
    def pendiente(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:
            movimientos = CtnMovimiento.objects.filter(usuario_id=usuario_id, tipo='PEDIDO', vr_saldo__gt=0)
            movimientosSerializador = CtnMovimientoSerializador(movimientos, many=True)
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
        valor_original=transaccion.get('amount_in_cents')
        valor=valor_original/100
        referencia=transaccion.get('reference')
        evento_pago = CtnEventoPago(
            fecha = timezone.now(),
            evento = evento,
            entorno = entorno,
            transaccion = transaccion.get('id'),
            metodo_pago = transaccion.get('payment_method_type'),
            referencia = referencia,
            estado = estado,
            correo = transaccion.get('customer_email'),
            fecha_transaccion = fecha_transaccion,
            vr_original = valor_original,
            vr_aplicar = valor
        )
        evento_pago.save()
        if estado == 'APPROVED':       
            if referencia:
                try:
                    pedido = CtnMovimiento.objects.get(id=referencia) 
                    if pedido:         
                        if valor <= pedido.vr_saldo:                            
                            recibo = CtnMovimiento(
                                tipo = "RECIBO",
                                fecha = timezone.now(),
                                fecha_vence = timezone.now().date(),
                                descripcion = 'PAGO SERVICIOS NUBE',
                                contenedor_movimiento_id=referencia,
                                movimiento_referencia_id=referencia,
                                vr_total = valor,
                                vr_saldo = 0,
                                socio_id = pedido.socio_id,
                                usuario_id = pedido.usuario_id
                            )
                            recibo.save()
                            valor = Decimal(valor)
                            # Aplicar creditos al socio por el pago
                            if pedido.socio_id:
                                socio = CtnSocio.objects.get(id=pedido.socio_id)
                                socio_usuario = User.objects.filter(es_socio=True, socio_id=pedido.socio_id).first()
                                if socio_usuario and socio:
                                    valor_credito = round(valor * socio.porcentaje_comision / 100)
                                    if valor_credito > 0:
                                        credito = CtnMovimiento(
                                            tipo = "CREDITO",
                                            fecha = timezone.now(),
                                            fecha_vence = timezone.now().date(),
                                            descripcion = f'COMISION PEDIDO ID {referencia} RECIBO ID {recibo.id}',
                                            contenedor_movimiento_id=recibo.id,  
                                            movimiento_referencia_id=recibo.id,                                          
                                            vr_total = valor_credito,
                                            vr_saldo = 0,
                                            socio_id = pedido.socio_id,
                                            usuario_id = socio_usuario.id
                                        )
                                        credito.save()  
                                        socio_usuario.vr_credito += valor_credito
                                        socio_usuario.save()

                            # Afectar saldo del pedido                                            
                            pedido.vr_afectado = pedido.vr_afectado + valor
                            pedido.vr_saldo =  pedido.vr_saldo - valor
                            pedido.save()
                            
                            # Actualizar la aplicacion del evento "pago"
                            evento_pago.estado_aplicado = True
                            evento_pago.save()

                            # Actualiza saldo del usuario
                            usuario = User.objects.get(pk=pedido.usuario_id)
                            if usuario:
                                usuario.vr_saldo -= valor
                                usuario.save()                                
                except Exception as e:
                    pass
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'aplicar-credito',)
    def aplicar_credito_action(self, request):
        raw = request.data
        movimiento_id = raw.get('movimiento_id')
        valor = raw.get('valor')
        usuario_id = raw.get('usuario_id')
        if movimiento_id and valor and usuario_id:
            try:
                movimiento = CtnMovimiento.objects.get(id=movimiento_id)
            except CtnMovimiento.DoesNotExist:
                return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                
            try:
                usuario = User.objects.get(id=usuario_id)
            except User.DoesNotExist:
                return Response({'mensaje':'El usuario no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                                                            
            if movimiento.vr_saldo >= valor:
                if usuario.vr_credito >= valor:
                    recibo = CtnMovimiento(
                        tipo = "RECIBO_CREDITO",
                        fecha = timezone.now(),
                        fecha_vence = timezone.now().date(),
                        descripcion = f'APLICACION DE CREDITOS PEDIDO ID {movimiento_id}',
                        contenedor_movimiento_id=movimiento_id,
                        movimiento_referencia_id=movimiento_id,
                        usuario_id=usuario_id,
                        socio_id=usuario.socio_id,
                        vr_total = valor,
                        vr_saldo = 0
                    )
                    recibo.save()                    
                    movimiento.vr_saldo -= valor
                    movimiento.vr_afectado += valor
                    movimiento.save()
                    usuario.vr_credito -= valor
                    usuario.vr_saldo -= valor
                    usuario.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({'Mensaje': 'El usuario no tiene creditos suficientes para afectar', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                     
            else:
                return Response({'Mensaje': f'El movimiento tiene un saldo de {movimiento.vr_saldo} y esta intentado aplicar un valor mayor {valor}', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                 
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)             
        
    @action(detail=False, methods=["post"], url_path=r'descargar',)
    def descargar(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                movimiento = CtnMovimiento.objects.get(pk=id)  
                if movimiento.documento_fisico:
                    archivo = f"itrio/prod/movimiento/factura_{id}.pdf" 
                    spaceDo = SpaceDo()
                    respuesta = spaceDo.descargar(archivo)         
                    if respuesta['error'] == False:
                        response = HttpResponse(respuesta['data'], content_type='application/pdf')
                        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                        response['Content-Disposition'] = f'attachment; filename="factura_{id}.pdf"'
                        return response
                        #return Response({'mensaje': 'Hola'}, status=status.HTTP_200_OK)
                    else:                    
                        return Response({'mensaje':respuesta['mensaje'], 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'El archivo aun no se encuentra disponible', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except CtnMovimiento.DoesNotExist:
                return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                 
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'marcar-adjunto',)
    def marcar_adjunto(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                movimiento = CtnMovimiento.objects.get(pk=id)  
                movimiento.documento_fisico = True
                movimiento.save()   
                return Response({'mensaje': 'Se marco correctamente'}, status=status.HTTP_200_OK)
            except CtnMovimiento.DoesNotExist:
                return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                 
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)         