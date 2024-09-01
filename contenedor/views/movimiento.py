from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contenedor.models import CtnMovimiento, CtnEventoPago, CtnConsumo
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


def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
    documentos = CtnMovimiento.objects.all()
    if filtros:
        for filtro in filtros:
            documentos = documentos.filter(**{filtro['propiedad']: filtro['valor1']})
    if ordenamientos:
        documentos = documentos.order_by(*ordenamientos)              
    documentos = documentos[desplazar:limite+desplazar]
    itemsCantidad = CtnMovimiento.objects.all()[:limiteTotal].count()                   
    respuesta = {'movimientos': documentos, "cantidad_registros": itemsCantidad}
    return respuesta  

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = CtnMovimiento.objects.all()
    serializer_class = CtnMovimientoSerializador    
    permission_classes = [permissions.IsAuthenticated]     
        
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        limiteTotal = raw.get('limite_total', 5000)                
        ordenamientos = raw.get('ordenamientos', [])            
        ordenamientos.insert(0, '-fecha')
        #ordenamientos.append('-numero')        
        filtros = raw.get('filtros', [])            
        #filtros.append({'propiedad': 'documento_tipo__documento_clase_id', 'valor1': documento_clase_id})        
        respuesta = listar(desplazar, limite, limiteTotal, filtros, ordenamientos)     
        serializador = CtnMovimientoSerializador(respuesta['movimientos'], many=True)
        documentos = serializador.data
        return Response(documentos, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'generar-pedido',)
    def generar_pedido(self, request):
        raw = request.data
        fechaDesde = raw.get('fechaDesde')
        fechaHasta = raw.get('fechaHasta')
        if fechaDesde and fechaHasta:
            consumosUsuarios = CtnConsumo.objects.values('usuario_id').filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta) & Q(usuario__cortesia=False)
                                                                              ).annotate(vr_total=Sum('vr_total'))
            facturas = []
            for consumoUsuario in consumosUsuarios:
                total = round(consumoUsuario['vr_total'])
                usuario = User.objects.get(pk=consumoUsuario['usuario_id'])
                if usuario.vr_saldo <= 0:
                    movimiento = CtnMovimiento(
                        tipo = "PEDIDO",
                        fecha = timezone.now(),
                        fecha_vence = datetime.now().date() + timedelta(days=3),
                        vr_total = total,
                        vr_saldo = total,
                        usuario_id = consumoUsuario['usuario_id'],
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
                    factura = CtnMovimiento.objects.get(id=referencia)          
                    if valor <= factura.vr_saldo:
                        recibo = CtnMovimiento(
                            tipo = "RECIBO",
                            fecha = timezone.now(),
                            fecha_vence = timezone.now().date(),
                            contenedor_movimiento_id=referencia,
                            vr_total = valor,
                            vr_saldo = 0                                         
                        )
                        recibo.save()
                        valor = Decimal(valor)                

                        factura.vr_afectado = factura.vr_afectado + valor
                        factura.vr_saldo =  factura.vr_saldo - valor
                        factura.save()
                        evento_pago.estado_aplicado = True
                        evento_pago.save()
                        usuario = User.objects.get(pk=factura.usuario_id)
                        if usuario:
                            usuario.vr_saldo -= valor
                            usuario.save()
                except Exception as e:
                    pass
        return Response(status=status.HTTP_200_OK)
    
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