from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from contenedor.models import CtnMovimiento, CtnEventoPago, CtnConsumo, CtnSocio
from contenedor.filters.movimiento import MovimientoFilter
from seguridad.models import User
from contenedor.serializers.movimiento import CtnMovimientoSerializador
from servicios.contenedor.movimiento import MovimientoServicio
from decouple import config
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Sum, Q, F
from django.db import transaction
from django.db import connection
from django.http import HttpResponse
from decimal import Decimal
from utilidades.space_do import SpaceDo
import hashlib
from decouple import config


class MovimientoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]     
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
            lote = datetime.now().strftime("%Y%m%d%H%M%S")
            pedidos = []
            for consumo in consumos:
                total = round(consumo['vr_total'])
                usuario = User.objects.get(pk=consumo['usuario_id'])
                if usuario.cortesia == False:
                    movimiento = CtnMovimiento(
                        tipo = "PEDIDO",                           
                        descripcion = 'SERVICIOS NUBE',
                        vr_total = total,
                        vr_total_operado = total,
                        vr_saldo = total,
                        usuario_id = consumo['usuario_id'],
                        socio_id=usuario.socio_id,
                        lote = lote,
                    )
                    pedidos.append(movimiento)                
                    usuario.vr_saldo += total
                    usuario.fecha_limite_pago = datetime.now().date() + timedelta(days=3)
                    usuario.save()
            CtnMovimiento.objects.bulk_create(pedidos)
            
            # Aplicar abonos si existen
            movimientos = CtnMovimiento.objects.filter(lote=lote)            
            for movimiento in movimientos:
                if movimiento.usuario_id:
                    usuario = User.objects.get(pk=movimiento.usuario_id)
                    if usuario:
                        if usuario.vr_abono > 0:
                            abono = usuario.vr_abono
                            if abono > movimiento.vr_saldo:
                                abono = movimiento.vr_saldo
                            saldo = movimiento.vr_saldo - abono
                            recibo = CtnMovimiento(
                                tipo = "RECIBO_ABONO",
                                descripcion = 'APLICACION DE ABONO',                                
                                movimiento_referencia_id=movimiento.id,
                                vr_total = abono,
                                vr_total_operado = abono*-1,
                                usuario_id = movimiento.usuario_id
                            )
                            recibo.save()
                            saldo = movimiento.vr_saldo - abono
                            movimiento.vr_afectado = movimiento.vr_afectado + abono
                            movimiento.vr_saldo = saldo                            
                            movimiento.save()
                            usuario.vr_abono -= abono
                            usuario.vr_saldo -= abono
                            usuario.save()
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
        evento = raw.get('event', None)
        entorno = raw.get('environment', None)
        data = raw.get('data', None)
        fecha_transaccion_parametro=raw.get('sent_at', None)
        fecha_transaccion_parametro = fecha_transaccion_parametro[:16]
        fecha_transaccion_parametro = fecha_transaccion_parametro.replace('T', ' ')
        fecha_transaccion = datetime.strptime(fecha_transaccion_parametro, '%Y-%m-%d %H:%M')
        transaccion=data.get('transaction', None)
        estado=transaccion.get('status', None)
        valor_original=transaccion.get('amount_in_cents', 0)
        valor=valor_original/100
        referencia_cruda=transaccion.get('reference', None)
        evento_pago = CtnEventoPago(            
            evento = evento,
            entorno = entorno,
            transaccion = transaccion.get('id'),
            metodo_pago = transaccion.get('payment_method_type'),
            referencia = referencia_cruda,
            estado = estado,
            correo = transaccion.get('customer_email'),
            fecha_transaccion = fecha_transaccion,
            vr_original = valor_original,
            vr_aplicar = valor,
            datos = raw
        )
        evento_pago.save()        
        if estado == 'APPROVED':       
            try:
                if referencia_cruda:  
                    with transaction.atomic():                                      
                        referencias = referencia_cruda.split('_')
                        for referencia in referencias:
                            tipo = referencia[0]                         
                            if tipo == 'P':
                                referencia_pedido_cruda = referencia[1:]
                                referencia_pedido = referencia_pedido_cruda.split('-')
                                movimiento_id = referencia_pedido[0]   
                                informacion_facturacion_id = referencia_pedido[1]                                                           
                                comentario = f'PED{movimiento_id} INF_FAC{informacion_facturacion_id}'
                                factura_id = MovimientoServicio.crear_factura(informacion_facturacion_id, valor, comentario)
                                pedido = CtnMovimiento.objects.get(id=movimiento_id) 
                                if pedido:                                                                     
                                    recibo = CtnMovimiento(
                                        tipo = "RECIBO",
                                        descripcion = 'PAGO SERVICIOS NUBE',
                                        movimiento_referencia_id=movimiento_id,
                                        vr_total = pedido.vr_saldo,
                                        vr_total_operado = pedido.vr_saldo*-1,
                                        vr_saldo = 0,
                                        socio_id = pedido.socio_id,
                                        usuario_id = pedido.usuario_id,
                                        factura_id = factura_id,
                                        genera_factura = True,
                                        informacion_facturacion_id = informacion_facturacion_id
                                    )
                                    recibo.save()
                                    total_pedido = Decimal(pedido.vr_saldo)
                                    # Aplicar creditos al socio por el pago
                                    if pedido.socio_id:
                                        socio = CtnSocio.objects.get(id=pedido.socio_id)                                        
                                        if socio:
                                            valor_credito = round(total_pedido * socio.porcentaje_comision / 100)
                                            if valor_credito > 0:
                                                credito = CtnMovimiento(
                                                    tipo = "CREDITO",
                                                    descripcion = f'COMISION PEDIDO ID {movimiento_id} RECIBO ID {recibo.id}',                                                     
                                                    movimiento_referencia_id=recibo.id,                                          
                                                    vr_total = valor_credito,
                                                    vr_total_operado = valor_credito,
                                                    vr_saldo = 0,
                                                    socio_id = pedido.socio_id,
                                                    usuario_id = socio.usuario_id
                                                )
                                                credito.save()  
                                                User.objects.filter(id=socio.usuario_id).update(vr_credito=F('vr_credito') + valor_credito)

                                    # Afectar saldo del pedido                                            
                                    pedido.vr_afectado = total_pedido
                                    pedido.vr_saldo =  0
                                    pedido.save()                                

                                    # Actualiza saldo del usuario
                                    User.objects.filter(id=pedido.usuario_id).update(vr_saldo=F('vr_saldo') - total_pedido)                                         
                            
                            if tipo == 'A': 
                                referencia_abono_cruda = referencia[1:]
                                referencia_abono = referencia_abono_cruda.split('-')
                                usuario_id = referencia_abono[0]   
                                informacion_facturacion_id = referencia_abono[1]
                                fecha = referencia_abono[2]
                                comentario = f'ABONO USUARIO{usuario_id} INF_FAC{informacion_facturacion_id}'   
                                # Crea factura en semantica
                                factura_id = MovimientoServicio.crear_factura(informacion_facturacion_id, valor, comentario)                    
                                abono = CtnMovimiento(
                                    tipo = "ABONO",
                                    descripcion = 'ABONO',
                                    vr_total = valor,
                                    vr_total_operado = valor,
                                    usuario_id = usuario_id,
                                    factura_id = factura_id,
                                    genera_factura = True,
                                    informacion_facturacion_id = informacion_facturacion_id
                                )
                                abono.save()
                                # Actualiza usuario
                                User.objects.filter(pk=usuario_id).update(vr_abono=F('vr_abono') + valor)         

                        evento_pago.estado_aplicado = True
                        evento_pago.save()
            except Exception as e:
                pass
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'aplicar-credito',)
    def aplicar_credito_action(self, request):
        raw = request.data
        movimiento_id = raw.get('movimiento_id')
        valor = raw.get('valor')        
        if movimiento_id and valor:
            try:
                movimiento = CtnMovimiento.objects.get(id=movimiento_id)
            except CtnMovimiento.DoesNotExist:
                return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                
            try:
                usuario = User.objects.get(id=movimiento.usuario_id)
            except User.DoesNotExist:
                return Response({'mensaje':'El usuario no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)      
                                                                                  
            if movimiento.vr_saldo >= valor:
                if usuario.vr_credito >= valor:
                    recibo = CtnMovimiento(
                        tipo = "RECIBO_CREDITO",
                        descripcion = f'APLICACION DE CREDITOS PEDIDO ID {movimiento_id}',
                        
                        movimiento_referencia_id=movimiento_id,
                        usuario_id=movimiento.usuario_id,
                        socio_id=usuario.socio_id,
                        vr_total = valor,
                        vr_total_operado = valor*-1,
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

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'regenerar-saldos',)
    def regenerar_saldos_action(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id', None)
        if usuario_id:
            User.objects.filter(id=usuario_id).update(vr_abono=0, vr_saldo=0, vr_credito=0)
        else:
            User.objects.all().update(vr_abono=0, vr_saldo=0, vr_credito=0)
    

        movimientos_abono = CtnMovimiento.objects.filter(tipo__in=['ABONO', 'RECIBO_ABONO']).values('usuario_id').annotate(total_abono=Sum('vr_total_operado'))
        for movimiento_abono in movimientos_abono:
            User.objects.filter(id=movimiento_abono['usuario_id']).update(vr_abono=movimiento_abono['total_abono'])

        movimientos_pedido = CtnMovimiento.objects.filter(tipo__in=['PEDIDO', 'RECIBO', 'RECIBO_CREDITO', 'RECIBO_ABONO']).values('usuario_id').annotate(total=Sum('vr_total_operado'))
        for movimiento_pedido in movimientos_pedido:
            User.objects.filter(id=movimiento_pedido['usuario_id']).update(vr_saldo=movimiento_pedido['total'])

        movimientos_credito = CtnMovimiento.objects.filter(tipo__in=['CREDITO', 'RECIBO_CREDITO']).values('usuario_id').annotate(total=Sum('vr_total_operado'))
        for movimiento_credito in movimientos_credito:
            User.objects.filter(id=movimiento_credito['usuario_id']).update(vr_credito=movimiento_credito['total'])

        with connection.cursor() as cursor:        
            query = f'''
                UPDATE cnt_movimiento AS pedido
                SET 
                    vr_afectado = COALESCE((SELECT SUM(mr.vr_total) FROM cnt_movimiento mr WHERE mr.movimiento_referencia_id = pedido.id), 0),
                    vr_saldo = pedido.vr_total - COALESCE((SELECT SUM(mr.vr_total) FROM cnt_movimiento mr WHERE mr.movimiento_referencia_id = pedido.id),0)
                WHERE pedido.tipo = 'PEDIDO';
            '''                    
            cursor.execute(query)
        return Response(status=status.HTTP_200_OK)
      
    @action(detail=False, methods=["post"], url_path=r'descargar',)
    def descargar(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                movimiento = CtnMovimiento.objects.get(pk=id)  
                if movimiento.factura_id:
                    respuesta = MovimientoServicio.descargar_factura(movimiento)
                    response = HttpResponse(
                        content=respuesta.content,
                        content_type=respuesta.headers.get('Content-Type', 'application/pdf')
                    )                        
                    #response = HttpResponse(respuesta['data'], content_type='application/pdf')
                    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                    response['Content-Disposition'] = f'attachment; filename="factura_{id}.pdf"'
                    return response                                            
                else:
                    return Response({'mensaje':'El archivo aun no se encuentra disponible', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except CtnMovimiento.DoesNotExist:
                return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                 
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

    # Deprecated        
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

    @action(detail=False, methods=["post"], url_path=r'crear-factura',)
    def crear_factura(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                movimiento = CtnMovimiento.objects.get(pk=id)  
                if movimiento.factura_id == None:
                    if movimiento.genera_factura:
                        if movimiento.informacion_facturacion_id:
                            comentario = f'PED/ABO{id} INF_FAC{movimiento.informacion_facturacion_id}'
                            factura_id = MovimientoServicio.crear_factura(movimiento.informacion_facturacion_id, float(movimiento.vr_total), comentario)
                            if factura_id:
                                movimiento.factura_id = factura_id
                                movimiento.save()
                                return Response({'mensaje': 'Factura generada'}, status=status.HTTP_200_OK)
                            else:
                                return Response({'mensaje':'No se genero la factura', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)    
                        else:
                            return Response({'mensaje':'El movimiento no tiene informacion facturacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje':'El movimiento no genera factura', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'El movimiento ya tiene factura', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except CtnMovimiento.DoesNotExist:
                return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                 
        else:
            return Response({'mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)              