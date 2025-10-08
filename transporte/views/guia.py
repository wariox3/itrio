from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.configuracion import GenConfiguracion
from general.serializers.configuracion import GenConfiguracionRndcSerializador
from transporte.models.guia import TteGuia
from transporte.serializers.guia import TteGuiaSerializador, TteGuiaDetalleSerializador, TteGuiaRndcSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar
from transporte.filters.guia import GuiaFilter
from django.db import models
from django.db import transaction
from datetime import datetime
from utilidades.rndc import Rndc


class GuiaViewSet(viewsets.ModelViewSet):
    queryset = TteGuia.objects.all()
    serializer_class = TteGuiaSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GuiaFilter 
    serializadores = {
        'detalle': TteGuiaDetalleSerializador,
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteGuiaSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="guias", nombre_archivo="guias.xlsx", titulo="Guias")
            if request.query_params.get('excel'):
                return exporter.exportar_estilo()
            if request.query_params.get('excel_masivo'):
                return exporter.exportar()
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        related_objects = []
        for related_object in instance._meta.related_objects:
            if not hasattr(related_object, 'field') or related_object.field.remote_field.on_delete == models.CASCADE:
                continue
            related_manager = getattr(instance, related_object.get_accessor_name())
            if related_manager.exists():
                related_objects.append(related_object.related_model.__name__)
        if related_objects:
            relaciones_texto = ', '.join(related_objects)
            return Response({'mensaje': f"El registro no se puede eliminar porque tiene registros asociados en: {relaciones_texto}"},status=status.HTTP_400_BAD_REQUEST) 
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["post"], url_path=r'entregar',)
    def entregar(self, request):                     
        raw = request.data
        id = raw.get('id')
        fecha = raw.get('fecha')
        hora = raw.get('hora')
        soporte = raw.get('soporte', False)                           
        if id and fecha and hora:
            try:
                fecha_hora_str = f"{fecha} {hora}"
                fecha_entrega = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
                guia = TteGuia.objects.get(pk=id)
                if guia.estado_entregado == False:  
                    with transaction.atomic():
                        guia.estado_entregado = True
                        guia.fecha_entrega = fecha_entrega 
                        if soporte:
                            guia.estado_soporte = True
                            guia.fecha_soporte = fecha_entrega
                        guia.save()
                        return Response({'mensaje': f'Guia entregada con éxito'}, status=status.HTTP_200_OK)                  
                else:
                    return Response({'mensaje':'La guia ya esta despachada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
            except TteGuia.DoesNotExist:
                return Response({'mensaje':'La guia no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                     
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        

    @action(detail=False, methods=["post"], url_path=r'enviar-rndc',)
    def enviar_rndc_action(self, request):        
        rndc = Rndc()             
        raw = request.data
        id = raw.get('id')                             
        if id:
            try:
                guia = TteGuia.objects.get(pk=id)
                credenciales = GenConfiguracionRndcSerializador(GenConfiguracion.objects.get(pk=1)).data
                if guia.estado_rndc == False:
                    serializador_rndc = TteGuiaRndcSerializador(guia)
                    datos_guia = serializador_rndc.data
                    if datos_guia['estado_rndc'] == False:
                        if datos_guia['servicio'] == 1:
                            respuesta_remitente = self.enviar_remitente_rndc(datos_guia, credenciales)
                            if not respuesta_remitente.get('error'):
                                respuesta_destinatario = self.enviar_destinatario_rndc(datos_guia, credenciales)
                                if not respuesta_destinatario.get('error'):
                                    numero_identificacion = datos_guia['cliente__numero_identificacion']
                                    if datos_guia['cliente__identificacion__codigo'] == '31':
                                        numero_identificacion += datos_guia['cliente__digito']

                                    arr_propiedades = {
                                        "CONSECUTIVOREMESA": datos_guia['id'],
                                        "CODOPERACIONTRANSPORTE": "G",
                                        "CODNATURALEZACARGA": "1",
                                        "CODNATURALEZACARGA": datos_guia['peso'],
                                        "UNIDADMEDIDACAPACIDAD": "1",
                                        "CODTIPOEMPAQUE": datos_guia['empaque__codigo'],
                                        "MERCANCIAREMESA": datos_guia['producto__codigo'],
                                        "DESCRIPCIONCORTAPRODUCTO": self.convertir_encoding_rndc(datos_guia['producto__nombre']),
                                        "CODTIPOIDREMITENTE": datos_guia['cliente__identificacion__codigo'],
                                        "NUMIDREMITENTE": numero_identificacion,
                                        "CODSEDEREMITENTE": datos_guia['ciudad_origen'],
                                        "CODTIPOIDDESTINATARIO": "C",
                                        "NUMIDDESTINATARIO": "333333333",
                                        "CODSEDEDESTINATARIO" : datos_guia['ciudad_destino'],
                                        "CODTIPOIDPROPIETARIO" : datos_guia['cliente__identificacion__codigo'],
                                        "NUMIDPROPIETARIO" : numero_identificacion,
                                        "CODSEDEPROPIETARIO": datos_guia['ciudad_origen']
                                    }
                                    proceso = "83"
                                    if datos_guia['servicio'] == 1:
                                        proceso = "3"
                                        arr_propiedades.update({
                                            "DUENOPOLIZA": "E",
                                            "NUMPOLIZATRANSPORTE": "",
                                            "FECHAVENCIMIENTOPOLIZACARGA": "",
                                            "COMPANIASEGURO": "",
                                            "HORASPACTOCARGA": "1",
                                            "MINUTOSPACTOCARGA": "1",
                                            "FECHACITAPACTADACARGUE": datos_guia['fecha_ingreso'],
                                            "HORACITAPACTADACARGUE": "08:00",
                                            "HORASPACTODESCARGUE": "1",
                                            "MINUTOSPACTODESCARGUE": "1",
                                            "FECHACITAPACTADADESCARGUE": datos_guia['fecha_ingreso'],
                                            "HORACITAPACTADADESCARGUEREMESA": "10:00"
                                        })
                                    xml = rndc.crear_xml(credenciales, "1", proceso, arr_propiedades)
                                    respuesta = rndc.enviar(xml)
                                    if not respuesta.get('error'):
                                        if respuesta.get('ingresoid'):
                                            guia.estado_rndc = True
                                            guia.numero_rndc = respuesta.get('numero_rndc')
                                            guia.save()
                                            return Response({'mensaje': 'Guia enviada'}, status=status.HTTP_200_OK)
                                    else:
                                        return Response({'mensaje': f"Ocurrió un error enviando la guia {id}: {respuesta.get('errorMensaje', 'Error desconocido')}"}, status=status.HTTP_400_BAD_REQUEST) 
                                else:
                                    return Response({'mensaje': f"Error al enviar destinatario: {respuesta_destinatario.get('errorMensaje')}", 'codigo': 3}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({'mensaje': f"Error al enviar remitente: {respuesta_remitente.get('errorMensaje')}", 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje': f"La guia: {id} tiene un tipo de servicio que no esta configurado para enviar el RNDC debe ser MUN o NAC", 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje': f"La guia: {id} ya fue enviada al rndc", 'codigo': 2}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje': 'La guia fue enviada al rndc', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST) 
            except TteGuia.DoesNotExist:
                return Response({'mensaje': 'La guia no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)                     
        else:
            return Response({'mensaje': 'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)

    def enviar_remitente_rndc(self, datos_guia, credenciales):
        rndc = Rndc()
        
        identificacion = datos_guia['cliente__numero_identificacion'] or ""
        nombre = datos_guia['cliente__nombre1'] or ""

        if datos_guia['cliente__identificacion__codigo'] == '31':
            identificacion += datos_guia['cliente__digito']
            nombre = datos_guia['cliente__nombre_corto']
        
        arr_propiedades = {
            "CODTIPOIDTERCERO": datos_guia['cliente__identificacion__codigo'],
            "NUMIDTERCERO": identificacion,
            "NOMIDTERCERO": self.convertir_encoding_rndc(nombre),
            "PRIMERAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_guia['cliente__apellido1']),
            "SEGUNDOAPELLIDOIDTERCERO": self.convertir_encoding_rndc(datos_guia['cliente__apellido2']),
            "CODSEDETERCERO": datos_guia['ciudad_origen'],
            "NOMSEDETERCERO": "PRINCIPAL",
            "NUMTELEFONOCONTACTO": datos_guia['cliente__telefono'],
            "NOMENCLATURADIRECCION": self.convertir_encoding_rndc(datos_guia['cliente__direccion']), 
            "CODMUNICIPIORNDC": datos_guia['ciudad_origen__codigo']
        }
        
        xml = rndc.crear_xml(credenciales, "1", "11", arr_propiedades)
        return rndc.enviar(xml)
    
    def enviar_destinatario_rndc(self, datos_guia, credenciales):
        rndc = Rndc()
                
        arr_propiedades = {
            "CODTIPOIDTERCERO": "C",
            "NUMIDTERCERO": "333333333",
            "NOMIDTERCERO": "VARIOS DESTINATARIO",
            "PRIMERAPELLIDOIDTERCERO": "PRIMERAPELLIDOIDTERCERO",
            "SEGUNDOAPELLIDOIDTERCERO": "VARIOS",
            "CODSEDETERCERO": datos_guia['ciudad_destino'],
            "NOMSEDETERCERO": f"{datos_guia['ciudad_destino']} CALLE PRINCIPAL",
            "NUMTELEFONOCONTACTO": "",
            "NOMENCLATURADIRECCION": f"CALLE PRINCIPAL {datos_guia['ciudad_destino__codigo']}", 
            "CODMUNICIPIORNDC": datos_guia['ciudad_destino__codigo']
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