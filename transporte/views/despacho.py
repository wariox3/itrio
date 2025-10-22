from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.configuracion import GenConfiguracion
from general.serializers.configuracion import GenConfiguracionRndcSerializador
from transporte.models.despacho import TteDespacho
from transporte.models.despacho_detalle import TteDespachoDetalle
from transporte.models.negocio import TteNegocio
from transporte.models.guia import TteGuia
from transporte.models.vehiculo import TteVehiculo
from general.models.contacto import GenContacto
from vertical.models.viaje import VerViaje
from transporte.serializers.despacho import TteDespachoSerializador, TteDespachoListaSerializador, TteDespachoDetalleVerSerializador, TteDespachoRndcSerializador
from transporte.serializers.despacho_detalle import TteDespachoDetalleSerializador
from transporte.serializers.guia import TteGuiaSerializador
from transporte.filters.despacho import DespachoFilter
from transporte.servicios.despacho import TteDespachoServicio
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Sum, Count, F
from utilidades.excel_exportar import ExcelExportar
from datetime import datetime
from transporte.formatos.orden_cargue import FormatoOrdenCargue
from transporte.formatos.manifiesto import FormatoManifiesto
from django.http import HttpResponse
from django.utils import timezone
from utilidades.rndc import Rndc

class DespachoViewSet(viewsets.ModelViewSet):
    queryset = TteDespacho.objects.all()
    serializer_class = TteDespachoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DespachoFilter 
    serializadores = {
        'lista': TteDespachoListaSerializador,
        'detalle': TteDespachoDetalleVerSerializador,
    } 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteDespachoSerializador
        return self.serializadores[serializador_parametro]

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
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('lista_completa', '').lower() == 'true':
            self.pagination_class = None
        if request.query_params.get('excel') or request.query_params.get('excel_masivo'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            exporter = ExcelExportar(serializer.data, nombre_hoja="despachos", nombre_archivo="despachos.xlsx", titulo="Despachos")
            if request.query_params.get('excel'):
                return exporter.exportar_estilo()
            if request.query_params.get('excel_masivo'):
                return exporter.exportar()
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar_action(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                despacho = TteDespacho.objects.get(pk=id)
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            with transaction.atomic():                                
                respuesta = TteDespachoServicio.aprobar(despacho)
                if respuesta['error'] == False:
                    return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':respuesta['mensaje'], 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'adicionar-guia',)
    def adicionar_guia_action(self, request):                     
        raw = request.data
        id = raw.get('id')           
        guia_id = raw.get('guia_id')           
        if id and guia_id:
            try:
                despacho = TteDespacho.objects.get(pk=id)
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            try:
                guia = TteGuia.objects.get(pk=guia_id)                            
            except TteGuia.DoesNotExist:
                return Response({'mensaje':'La guia no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)           
            if guia.estado_despachado == False and guia.despacho_id == None:  
                with transaction.atomic():   
                    TteDespachoServicio.adicionar_guia(despacho, guia)
                    return Response({'mensaje': f'Guia adicionada al despacho'}, status=status.HTTP_200_OK)                  
            else:
                return Response({'mensaje':'La guia ya esta despachada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    @action(detail=False, methods=["post"], url_path=r'generar-viaje',)
    def generar_viaje_action(self, request):        
        raw = request.data
        viaje_id = raw.get('viaje_id')
        if viaje_id:
            try:
                with transaction.atomic():
                    viaje = VerViaje.objects.get(pk=viaje_id)   
                    try:
                        negocio = TteNegocio.objects.get(pk=viaje.negocio_id)
                    except TteNegocio.DoesNotExist:
                        return Response({'mensaje':'El negocio no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                    try:
                        vehiculo = TteDespachoServicio.validar_vehiculo_vertical(viaje)
                    except ValueError as e:
                        return Response({'mensaje': str(e), 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                                                                
                    try:
                        conductor = TteDespachoServicio.validar_conductor_vertical(viaje)
                    except ValueError as e:
                        return Response({'mensaje': str(e), 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                         

                    data = {
                        'fecha':datetime.now(),
                        'despacho_tipo':1,
                        'ciudad_origen':negocio.ciudad_origen_id,
                        'ciudad_destino':negocio.ciudad_destino_id,
                        'operacion':negocio.operacion_id,
                        'contacto':vehiculo.propietario_id,
                        'vehiculo':vehiculo.id,                        
                        'conductor':conductor.id,
                        'servicio': negocio.servicio_id,
                        'guias': 1,
                        'unidades': negocio.unidades,
                        'peso': negocio.peso,
                        'volumen': negocio.volumen,
                        'pago': negocio.pago
                    }    
                    despacho_serializador = TteDespachoSerializador(data=data)
                    if despacho_serializador.is_valid(): 
                        despacho = despacho_serializador.save()
                        data = {
                            'fecha': datetime.now(),    
                            'fecha_ingreso': datetime.now(),    
                            'operacion_ingreso': negocio.operacion_id,
                            'operacion_cargo': negocio.operacion_id,
                            'contacto': negocio.contacto_id,
                            'cliente': negocio.contacto_id,
                            'unidades': negocio.unidades,
                            'peso': negocio.peso,
                            'volumen': negocio.volumen,
                            'peso_facturado': negocio.peso,
                            'flete': negocio.flete,                                
                            'ciudad_origen': negocio.ciudad_origen_id,
                            'ciudad_destino': negocio.ciudad_destino_id,
                            'remitente': negocio.contacto.nombre_corto,
                            'destinatario_nombre': negocio.destinatario_nombre if negocio.destinatario_nombre else "Destinatario conocido",
                            'destinatario_direccion': negocio.destinatario_direccion,
                            'destinatario_telefono': negocio.destinatario_telefono,
                            'destinatario_correo': negocio.destinatario_correo,
                            'servicio': negocio.servicio_id,
                            'producto': negocio.producto_id,
                            'empaque': negocio.empaque_id,
                            'liquidacion': 'M',
                            'despacho': despacho.id,
                            'estado_despachado': True,
                            'estado_recodigo': True,
                            'estado_ingreso': True
                        }
                        guia_serializador = TteGuiaSerializador(data=data)
                        if guia_serializador.is_valid():
                            guia = guia_serializador.save()
                            data = {
                                'despacho':despacho.id,
                                'guia':guia.id,
                                'unidades': guia.unidades, 
                                'peso': guia.peso, 
                                'volumen': guia.volumen, 
                                'peso_facturado': guia.peso_facturado, 
                                'costo': guia.costo, 
                                'declara': guia.declara,                         
                                'flete':guia.flete, 
                                'manejo':guia.manejo, 
                                'recaudo':guia.recaudo, 
                                'cobro_entrega':guia.cobro_entrega                        
                            }
                            despacho_detalle_serializador = TteDespachoDetalleSerializador(data=data)
                            if despacho_detalle_serializador.is_valid():    
                                despacho_detalle_serializador.save()                        
                            else:
                                return Response({'validaciones': despacho_detalle_serializador.errors, 'mensaje': 'Cuenta por pagar'}, status=status.HTTP_400_BAD_REQUEST)                            
                        else:
                            return Response({'mensaje': 'Se presentaron errores creado la guia', 'validaciones': guia_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                        
                    else:
                        return Response({'mensaje': 'Se presentaron errores creando el despacho', 'validariovalidacionesnes': despacho_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                             

                    return Response({'mensaje': 'viaje generado'}, status=status.HTTP_200_OK)                 
            except VerViaje.DoesNotExist:
                return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                                        
    @action(detail=False, methods=["post"], url_path=r'imprimir',)
    def imprimir(self, request):
        raw = request.data
        id = raw.get('despacho_id')
        if id:
            try:
                pdf = None                                     
                formato = FormatoOrdenCargue()
                pdf = formato.generar_pdf(id)              
                nombre_archivo = f"orden_cargue_{id}.pdf"       
                
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
                return response
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
        
    @action(detail=False, methods=["post"], url_path=r'imprimir-manifiesto',)
    def imprimirManifiesto(self, request):
        raw = request.data
        id = raw.get('despacho_id')
        if id:
            try:
                pdf = None                                     
                formato = FormatoManifiesto()
                pdf = formato.generar_pdf(id)              
                nombre_archivo = f"manifiesto_{id}.pdf"       
                
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
                return response
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
        
    @action(detail=False, methods=["post"], url_path=r'nuevo-viaje',)
    def nuevo_viaje_action(self, request):        
        raw = request.data
        viaje_id = raw.get('viaje_id')        
        if viaje_id:
            try:
                viaje = VerViaje.objects.get(pk=viaje_id)
            except VerViaje.DoesNotExist:
                return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            try:
                negocio = TteNegocio.objects.get(pk=viaje.negocio_id)
            except TteNegocio.DoesNotExist:
                return Response({'mensaje':'El negocio no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            try:
                vehiculo = TteVehiculo.objects.filter(placa=viaje.vehiculo.placa).first()
                if not vehiculo:
                    raise TteVehiculo.DoesNotExist
            except TteVehiculo.DoesNotExist:
                return Response({'mensaje':'El vehiculo no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
            try:
                conductor = GenContacto.objects.filter(numero_identificacion=viaje.conductor.numero_identificacion).first()
                if not conductor:
                    raise GenContacto.DoesNotExist
            except GenContacto.DoesNotExist:
                return Response({'mensaje':'El conductor no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)             

            with transaction.atomic():                
                data = {
                    'fecha': timezone.now().date(),                        
                    'operacion_ingreso': negocio.operacion_id,
                    'operacion_cargo': negocio.operacion_id,
                    'negocio': negocio.id,
                    'contacto': negocio.contacto_id,
                    'cliente': negocio.contacto_id,
                    'unidades': negocio.unidades,
                    'peso': negocio.peso,
                    'volumen': negocio.volumen,
                    'peso_facturado': negocio.peso,
                    'flete': negocio.flete,        
                    'destinatario_nombre' : 'PEDRO PEREZ',
                    'destinatario_direccion' : 'CALLE 25 NRO 25 80',
                    'ciudad_origen': negocio.ciudad_origen_id,
                    'ciudad_destino': negocio.ciudad_destino_id,
                    'remitente_nombre': negocio.contacto.nombre_corto,
                    'servicio': negocio.servicio_id,
                    'producto': negocio.producto_id,
                    'empaque': negocio.empaque_id,
                    'estado_recogido': True,
                    'estado_ingreso': True,
                    'liquidacion': 'M'
                }     
                guia_serializador = TteGuiaSerializador(data=data)
                if guia_serializador.is_valid():
                    guia = guia_serializador.save()   
                    data = {
                        "fecha": timezone.now().date(),
                        "despacho_tipo":1,
                        "servicio":negocio.servicio_id,
                        "ciudad_origen":negocio.ciudad_origen_id,
                        "ciudad_destino":negocio.ciudad_destino_id,
                        "operacion":negocio.operacion_id,                        
                        "contacto":vehiculo.poseedor_id,
                        "vehiculo":vehiculo.id,
                        "conductor":conductor.id,
                        "pago":negocio.pago,
                        "unidades":negocio.unidades,
                        "peso":negocio.peso,
                        "volumen":negocio.volumen,
                        "guias": 1
                    }      
                    despacho_serializador = TteDespachoSerializador(data=data)
                    if despacho_serializador.is_valid():    
                        despacho = despacho_serializador.save()
                        TteDespachoServicio.adicionar_guia(despacho, guia)
                        TteDespachoServicio.aprobar(despacho)
                        return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)                                           
                    else:
                        return Response({'validaciones': despacho_serializador.errors, 'mensaje': 'No se pudo crear el despacho'}, status=status.HTTP_400_BAD_REQUEST)                               
                else:
                    return Response({'validaciones': guia_serializador.errors, 'mensaje': 'No se pudo crear la guia'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)              
        
    @action(detail=False, methods=["post"], url_path=r'enviar-rndc',)
    def enviar_rndc_action(self, request):         
        rndc = Rndc()                    
        raw = request.data
        id = raw.get('id')                             
        if id:
            try:
                despacho = TteDespacho.objects.get(pk=id)
                credenciales = GenConfiguracionRndcSerializador(GenConfiguracion.objects.get(pk=1)).data
                if despacho.estado_rndc == False:
                    serializador_rndc = TteDespachoRndcSerializador(despacho)
                    datos_despacho = serializador_rndc.data
                    if datos_despacho['servicio'] == 1:
                        respuesta_poseedor = self.enviar_poseedor_rndc(datos_despacho, credenciales)
                        if not respuesta_poseedor.get('error'):
                            respuesta_propietario = self.enviar_propietario_rndc(datos_despacho, credenciales)
                            if not respuesta_propietario.get('error'):
                                respuesta_conductor = self.enviar_conductor_rndc(datos_despacho, credenciales)
                            else:
                                return Response({'mensaje': f"Error al enviar el propietario: {respuesta_propietario.get('errorMensaje')}", 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje': f"Error al enviar el poseedor: {respuesta_poseedor.get('errorMensaje')}", 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje': f"El despacho: {id} tiene un tipo de servicio que no esta configurado para enviar el RNDC debe ser MUN o NAC", 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje': 'El despachado ya fue enviado al rndc', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST) 
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                     
            return Response({'mensaje': f'Despacho enviado'}, status=status.HTTP_200_OK)                  
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    def enviar_poseedor_rndc(self, datos_despacho, credenciales):
        rndc = Rndc()
        
        identificacion = datos_despacho['cliente__numero_identificacion'] or ""
        nombre = datos_despacho['cliente__nombre1'] or ""

        if datos_despacho['cliente__identificacion__codigo'] == '31':
            identificacion += datos_despacho['cliente__digito']
            nombre = datos_despacho['cliente__nombre_corto']
        # Definir de donde salen los datos correctamente poseedor.
        arr_propiedades = {
            "CODTIPOIDTERCERO": datos_despacho['cliente__identificacion__codigo'],
            "NUMIDTERCERO": identificacion,
            "NOMIDTERCERO": self.convertir_encoding_rndc(nombre),
            "PRIMERAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_despacho['cliente__apellido1']),
            "SEGUNDOAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_despacho['cliente__apellido2']),
            "CODSEDETERCERO": "1",
            "NOMSEDETERCERO": "PRINCIPAL",
            "NUMTELEFONOCONTACTO": datos_despacho['cliente__telefono'],
            "NOMENCLATURADIRECCION": self.convertir_encoding_rndc(datos_despacho['cliente__direccion']), 
            "CODMUNICIPIORNDC": datos_despacho['ciudad_origen__codigo']
        }
        
        xml = rndc.crear_xml(credenciales, "1", "11", arr_propiedades)
        return rndc.enviar(xml)
    
    def enviar_propietario_rndc(self, datos_despacho, credenciales):
        rndc = Rndc()
        
        identificacion = datos_despacho['cliente__numero_identificacion'] or ""
        nombre = datos_despacho['cliente__nombre1'] or ""

        if datos_despacho['cliente__identificacion__codigo'] == '31':
            identificacion += datos_despacho['cliente__digito']
            nombre = datos_despacho['cliente__nombre_corto']
        # Definir de donde salen los datos correctamente propietario.
        arr_propiedades = {
            "CODTIPOIDTERCERO": datos_despacho['cliente__identificacion__codigo'],
            "NUMIDTERCERO": identificacion,
            "NOMIDTERCERO": self.convertir_encoding_rndc(nombre),
            "PRIMERAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_despacho['cliente__apellido1']),
            "SEGUNDOAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_despacho['cliente__apellido2']),
            "CODSEDETERCERO": "1",
            "NOMSEDETERCERO": "PRINCIPAL",
            "NUMTELEFONOCONTACTO": datos_despacho['cliente__telefono'],
            "NOMENCLATURADIRECCION": self.convertir_encoding_rndc(datos_despacho['cliente__direccion']), 
            "CODMUNICIPIORNDC": datos_despacho['ciudad_origen__codigo']
        }
        
        xml = rndc.crear_xml(credenciales, "1", "11", arr_propiedades)
        return rndc.enviar(xml)    
    
    def enviar_conductor_rndc(self, datos_despacho, credenciales):
        rndc = Rndc()

        tipoIdentificacion = 'C'
        if datos_despacho['cliente__identificacion__codigo'] == '31':
            tipoIdentificacion = 'N'
        
        arr_propiedades = {
            "CODTIPOIDTERCERO": datos_despacho['cliente__identificacion__codigo'],
            "NUMIDTERCERO": datos_despacho['conductor__numero_identificacion'],
            "NOMIDTERCERO": self.convertir_encoding_rndc(datos_despacho['conductor__nombre1']),
            "PRIMERAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_despacho['conductor__apellido1']),
            "SEGUNDOAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_despacho['conductor__apellido2']),
            "CODSEDETERCERO": "1",
            "NOMSEDETERCERO": "PRINCIPAL",
            "NUMTELEFONOCONTACTO": datos_despacho['conductor__telefono'],
            "NOMENCLATURADIRECCION": self.convertir_encoding_rndc(datos_despacho['conductor__direccion']), 
            "CODMUNICIPIORNDC": datos_despacho['conductor__ciudad__codigo'],
            "CODCATEGORIALICENCIACONDUCCION": datos_despacho['conductor__ciudad__codigo'],
            "NUMLICENCIACONDUCCION": datos_despacho['conductor__ciudad__codigo'],
            "FECHAVENCIMIENTOLICENCIA": datos_despacho['conductor__ciudad__codigo'],
        }
        
        xml = rndc.crear_xml(credenciales, "1", "11", arr_propiedades)
        return rndc.enviar(xml)        

    @staticmethod
    def convertir_encoding_rndc(texto):
        if texto is None:
            return ""
        try:
            return str(texto).encode('iso-8859-1').decode('utf-8')
        except:
            return str(texto)  