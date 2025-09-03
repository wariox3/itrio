from decimal import Decimal
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.viaje import VerViaje
from vertical.models.propuesta import VerPropuesta
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor
from vertical.models.precio_detalle import VerPrecioDetalle
from vertical.serializers.viaje import VerViajeSerializador, VerViajeListaSerializador, VerViajeListaEspecialSerializador
from vertical.serializers.propuesta import VerPropuestaSerializador
from vertical.filters.viaje import VerViajeFilter
from django.db import transaction
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = VerViaje.objects.all()
    serializer_class = VerViajeSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VerViajeFilter 
    serializadores = {
        'lista': VerViajeListaSerializador,
    } 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return VerViajeSerializador
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

    @action(detail=False, methods=["post"], url_path=r'nuevo',)
    def nuevo_action(self, request):        
        raw = request.data
        data = raw
        with transaction.atomic():
            viaje_serializador = VerViajeSerializador(data=data)
            if viaje_serializador.is_valid():
                viaje = viaje_serializador.save()
                precios_detalles = VerPrecioDetalle.objects.filter(ciudad_origen_id=data['ciudad_origen'], ciudad_destino_id=data['ciudad_destino'])
                for precio_detalle in precios_detalles:
                    peso_toneladas = Decimal(viaje.peso) / Decimal(1000)                    
                    data = {
                        'viaje': viaje.id,
                        'usuario': viaje.usuario_id,
                        'precio': round(peso_toneladas * precio_detalle.tonelada),
                        'contenedor_id': precio_detalle.contenedor_id,
                        'schema_name': precio_detalle.schema_name,
                        'empresa': precio_detalle.empresa
                    }
                    propuesta_serializador = VerPropuestaSerializador(data=data)
                    if propuesta_serializador.is_valid():
                        propuesta_serializador.save()
                    else:
                        transaction.set_rollback(True)
                        return Response({'validaciones': propuesta_serializador.errors, 'mensaje': 'No se pudo crear la propuesta'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'mensaje': 'viaje creado', 'viaje': viaje_serializador.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'mensaje': 'Error al crear el viaje', 'validaciones': viaje_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'aceptar',)
    def aceptar_action(self, request):        
        raw = request.data
        viaje_id = raw.get('viaje_id')
        conductor_id = raw.get('conductor_id')
        vehiculo_id = raw.get('vehiculo_id')
        if viaje_id and conductor_id and vehiculo_id:            
            with transaction.atomic():
                try:
                    viaje = VerViaje.objects.get(pk=viaje_id)
                except VerViaje.DoesNotExist:
                    return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                if viaje.estado_aceptado:
                    return Response({'mensaje':'El viaje ya fue aceptado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                               
                try:
                    vehiculo = VerVehiculo.objects.get(pk=vehiculo_id)
                except VerVehiculo.DoesNotExist:
                    return Response({'mensaje':'El vehiculo no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    conductor = VerConductor.objects.get(pk=conductor_id)                                    
                except VerConductor.DoesNotExist:
                    return Response({'mensaje':'El conductor no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                                                                                            
                viaje.conductor = conductor
                viaje.vehiculo = vehiculo
                viaje.estado_aceptado = True
                viaje.save()
                return Response({'mensaje': 'viaje aceptado'}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'cancelar',)
    def cancelar_action(self, request):        
        raw = request.data
        id = raw.get('id')        
        if id:            
            with transaction.atomic():
                try:
                    viaje = VerViaje.objects.get(pk=id)
                except VerViaje.DoesNotExist:
                    return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                if viaje.estado_aceptado:
                    return Response({'mensaje':'El viaje ya fue aceptado y no se puede cancelar', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                                                                                                       
                viaje.estado_cancelado = True
                viaje.save()
                return Response({'mensaje': 'Viaje cancelado aceptado'}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path=r'lista')
    def lista_action(self, request):                
        usuario_id = request.query_params.get('usuario_id')
        estado_aceptado = request.query_params.get('estado_aceptado')
        estado_cancelado = request.query_params.get('estado_cancelado')
        queryset = VerViaje.objects.select_related(
            'ciudad_origen', 
            'ciudad_destino', 
            'servicio', 
            'producto', 
            'empaque',
            'usuario'
        )
        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        if estado_aceptado == True or estado_aceptado == 'true' or estado_aceptado == 'True':
            queryset = queryset.filter(estado_aceptado=True)
        if estado_aceptado == False or estado_aceptado == 'false' or estado_aceptado == 'False':
            queryset = queryset.filter(estado_aceptado=False)    
        if estado_cancelado == True or estado_cancelado == 'true' or estado_cancelado == 'True':
            queryset = queryset.filter(estado_cancelado=True)
        if estado_cancelado == False or estado_cancelado == 'false' or estado_cancelado == 'False':
            queryset = queryset.filter(estado_cancelado=False)                     
        viajes = queryset.prefetch_related(
            Prefetch(
                'propuestas_viaje_rel',
                queryset=VerPropuesta.objects.order_by('-id'),
                to_attr='propuestas_ordenadas'
            )
        ).order_by('-id')

        resultado = []
        for viaje in viajes:
            viaje_serializador = VerViajeListaEspecialSerializador(viaje)
            propuestas_serializador = VerPropuestaSerializador(viaje.propuestas_ordenadas, many=True)
            
            resultado.append({
                'datos': viaje_serializador.data,
                'propuestas': propuestas_serializador.data
            })
        
        return Response({'viajes': resultado}, status=status.HTTP_200_OK)            