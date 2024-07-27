from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from general.models.item import Item
from general.models.contacto import Contacto
from general.models.forma_pago import FormaPago
from general.models.metodo_pago import MetodoPago
from general.models.documento import Documento
from general.models.impuesto import Impuesto
from general.models.identificacion import Identificacion
from general.models.ciudad import Ciudad
from general.models.tipo_persona import TipoPersona
from general.models.regimen import Regimen
from general.models.resolucion import Resolucion
from general.models.asesor import Asesor
from general.models.precio import Precio
from general.models.plazo_pago import PlazoPago
from general.models.sede import Sede
from general.models.cuenta_banco import CuentaBanco
from general.models.cuenta_banco_tipo import CuentaBancoTipo
from contabilidad.models.cuenta import Cuenta
from humano.models.hum_contrato import HumContrato
from humano.models.hum_programacion import HumProgramacion
from humano.models.hum_grupo import HumGrupo
from humano.models.hum_pago_tipo import HumPagoTipo
from ruteo.models.rut_vehiculo import RutVehiculo
from ruteo.models.rut_franja import RutFranja
from general.serializers.item import ItemSerializador, ItemListaAutocompletarSerializador, ItemListaBuscarSerializador
from general.serializers.contacto import ContactoSerializador, ContactoListaAutocompletarSerializador, ContactoListaBuscarSerializador
from general.serializers.forma_pago import FormaPagoSerializador, FormaPagoListaAutocompletarSerializador
from general.serializers.metodo_pago import MetodoPagoSerializador, MetodoPagoListaAutocompletarSerializador
from general.serializers.tipo_persona import TipoPersonaSerializador, TipoPersonaListaAutocompletarSerializador
from general.serializers.documento import DocumentoSerializador
from general.serializers.impuesto import ImpuestoSerializador, ImpuestoListaAutocompletarSerializador
from general.serializers.identificacion import IdentificacionSerializador, IdentificacionListaAutocompletarSerializador
from general.serializers.ciudad import CiudadSerializador, CiudadListaAutocompletarSerializador
from general.serializers.regimen import RegimenSerializador, RegimenListaAutocompletarSerializador
from general.serializers.resolucion import ResolucionSerializador, ResolucionListaAutocompletarSerializador
from general.serializers.asesor import AsesorSerializador, AsesorListaAutocompletarSerializador
from general.serializers.precio import PrecioSerializador, PrecioListaAutocompletarSerializador
from general.serializers.plazo_pago import PlazoPagoSerializador, PlazoPagoListaAutocompletarSerializador
from general.serializers.sede import SedeSerializador, SedeListaAutocompletarSerializador
from general.serializers.cuenta_banco import CuentaBancoSerializador, CuentaBancoListaAutocompletarSerializador
from general.serializers.cuenta_banco_tipo import CuentaBancoTipoSerializador, CuentaBancoTipoListaAutocompletarSerializador
from contabilidad.serializers.cuenta import CuentaListaAutocompletarSerializador
from humano.serializers.hum_contrato import HumContratoSerializador
from humano.serializers.hum_programacion import HumProgramacionSerializador
from humano.serializers.hum_grupo import HumGrupoSerializador, HumGrupoListaAutocompletarSerializador
from humano.serializers.hum_pago_tipo import HumPagoTipoSerializador, HumPagoTipoListaAutocompletarSerializador
from ruteo.serializers.rut_vehiculo import RutVehiculoSerializador
from ruteo.serializers.rut_franja import RutFranjaSerializador

from rest_framework.permissions import IsAuthenticated

class ListaAdministradorView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        codigoModelo = raw.get('modelo')
        if codigoModelo:
            desplazar = raw.get('desplazar', 0)
            limite = raw.get('limite', 50)    
            cantidadLimite = raw.get('cantidad_limite', 5000)    
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')
            model = globals()[codigoModelo]
            serializer_name = f"{codigoModelo}Serializador"
            serializer = globals()[serializer_name]
            items = model.objects.all()
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)              
            items = items[desplazar:limite+desplazar]
            itemsCantidad = model.objects.all()[:cantidadLimite].count()
            serializador = serializer(items, many=True) 
            '''fields_info = []
            model_fields = serializer().get_fields()
            for field_name, field_instance in model_fields.items():
                nombre_verbose_name = model._meta.get_field(field_name).verbose_name
                field_type = field_instance.__class__.__name__
                fields_info.append({"nombre": field_name, "tipo": field_type, "titulo":field_name.upper(), "titulo2": nombre_verbose_name})'''
            return Response({"registros": serializador.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

class ListaAutocompletarView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        codigoModelo = raw.get('modelo')
        limite = raw.get('limite', 10)
        if codigoModelo:      
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')
            modelo = globals()[codigoModelo]
            serializadorNombre = f"{codigoModelo}ListaAutocompletarSerializador"
            serializador = globals()[serializadorNombre]            
            items = modelo.objects.all()
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)                          
            if limite > 0:
                items = items[0:limite]
            datos = serializador(items, many=True)    
            return Response({"registros": datos.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
    
class ListaBuscarView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        codigoModelo = raw.get('modelo')
        limite = raw.get('limite', 10)
        if codigoModelo:      
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')
            modelo = globals()[codigoModelo]
            serializadorNombre = f"{codigoModelo}ListaBuscarSerializador"
            serializador = globals()[serializadorNombre]            
            items = modelo.objects.all()
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)                          
            if limite > 0:
                items = items[0:limite]
            datos = serializador(items, many=True)    
            return Response({"registros": datos.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    