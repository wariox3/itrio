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
from general.serializers.item import ItemSerializador, ItemListaAutocompletarSerializador
from general.serializers.contacto import ContactoSerializador, ContactoListaAutocompletarSerializador
from general.serializers.forma_pago import FormaPagoSerializador, FormaPagoListaAutocompletarSerializador
from general.serializers.metodo_pago import MetodoPagoSerializador, MetodoPagoListaAutocompletarSerializador
from general.serializers.tipo_persona import TipoPersonaSerializador, TipoPersonaListaAutocompletarSerializador
from general.serializers.documento import DocumentoSerializador
from general.serializers.impuesto import ImpuestoSerializador, ImpuestoListaAutocompletarSerializador
from general.serializers.identificacion import IdentificacionSerializador, IdentificacionListaAutocompletarSerializador
from general.serializers.ciudad import CiudadSerializador, CiudadListaAutocompletarSerializador
from general.serializers.regimen import RegimenSerializador, RegimenListaAutocompletarSerializador
from general.serializers.resolucion import ResolucionSerializador
from rest_framework.permissions import IsAuthenticated

class PendienteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({"mensaje": "Hola mundo"}, status=status.HTTP_200_OK)
