from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from general.models.item import Item
from general.models.contacto import Contacto
from general.models.documento import Documento
from general.serializers.item import ItemSerializador, ItemListaAutocompletarSerializador
from general.serializers.contacto import ContactoSerializador
from general.serializers.documento import DocumentoSerializador
from rest_framework.permissions import IsAuthenticated

class ListaView(APIView):
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
            fields_info = []
            model_fields = serializer().get_fields()
            for field_name, field_instance in model_fields.items():
                field_type = field_instance.__class__.__name__
                fields_info.append({"nombre": field_name, "tipo": field_type})       
            return Response({"propiedades":fields_info, "registros": serializador.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
    
class ListaAutocompletarView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        codigoModelo = raw.get('modelo')
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
            items = items[0:10]
            datos = serializador(items, many=True)    
            return Response({"registros": datos.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)