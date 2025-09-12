from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transporte.models.negocio import TteNegocio
from general.models.contacto import GenContacto
from vertical.models.viaje import VerViaje
from vertical.models.propuesta import VerPropuesta
from transporte.serializers.negocio import TteNegocioSerializador, TteNegocioSeleccionarSerializador
from transporte.filters.negocio import NegocioFilter
from transporte.servicios.negocio import TteNegocioServicio
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar
from django.db import transaction
from django.utils import timezone

class NegocioViewSet(viewsets.ModelViewSet):
    queryset = TteNegocio.objects.all()
    serializer_class = TteNegocioSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NegocioFilter 
    serializadores = {
        'lista': TteNegocioSerializador,
    } 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteNegocioSerializador
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
        if request.query_params.get('excel'):   
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)         
            exporter = ExcelExportar(serializer.data, 'negocio', 'negocios.xlsx')
            return exporter.exportar_estilo()
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre__icontains', None)
        contacto_id = request.query_params.get('contacto_id', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if contacto_id:
            queryset = queryset.filter(contacto_id=contacto_id)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = TteNegocioSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)   

    @action(detail=False, methods=["post"], url_path=r'nuevo-viaje',)
    def nuevo_viaje_action(self, request):        
        raw = request.data
        viaje_id = raw.get('viaje_id', None)
        propuesta_id = raw.get('propuesta_id', None)
        if viaje_id and propuesta_id:
            try:
                viaje = VerViaje.objects.get(pk=viaje_id)
            except VerViaje.DoesNotExist:
                return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)      
            try:
                propuesta = VerPropuesta.objects.get(pk=propuesta_id)
            except VerPropuesta.DoesNotExist:
                return Response({'mensaje':'La propuesta no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)      
            with transaction.atomic():
                contacto_id = None
                if viaje.numero_identificacion:
                    contacto = GenContacto.objects.filter(numero_identificacion=viaje.numero_identificacion).first()
                    contacto_id = contacto.id if contacto else None
                data = {
                    'fecha': timezone.now().date(),
                    'nombre': viaje.cliente,
                    'servicio': viaje.servicio_id,
                    'producto': viaje.producto_id,
                    'empaque': viaje.empaque_id,
                    'unidades': viaje.unidades,
                    'peso': viaje.peso,
                    'volumen': viaje.volumen,
                    'flete': viaje.flete,
                    'pago': viaje.pago,
                    'comentario': viaje.comentario,
                    'ciudad_origen': viaje.ciudad_origen_id,
                    'ciudad_destino': viaje.ciudad_destino_id,    
                    'puntos_entrega': viaje.puntos_entrega, 
                    'operacion': 1,   
                    'contacto': contacto_id,
                    'publicar': True       
                }     
                serializador_negocio = TteNegocioSerializador(data=data)
                if serializador_negocio.is_valid():
                    negocio = serializador_negocio.save()                    
                    viaje.negocio_id = negocio.id
                    viaje.save()
                    respuesta = TteNegocioServicio.aprobar(negocio, propuesta.contenedor_id, propuesta.schema_name)
                    return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)                                           
                else:
                    return Response({'validaciones': serializador_negocio.errors, 'mensaje': 'No se pudo crear el negocio'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar_action(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                negocio = TteNegocio.objects.get(pk=id)
            except TteNegocio.DoesNotExist:
                return Response({'mensaje':'El negocio no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                respuesta = TteNegocioServicio.aprobar(negocio, request.tenant.id, request.tenant.schema_name)   
                if respuesta['error'] == False:
                    return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':respuesta['mensaje'], 'codigo':16}, status=status.HTTP_400_BAD_REQUEST)                                             
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)