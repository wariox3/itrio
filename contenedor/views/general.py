from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from contenedor.models import CtnIdentificacion
from contenedor.models import CtnCiudad
from contenedor.models import CtnRegimen
from contenedor.models import CtnTipoPersona
from rest_framework.permissions import IsAuthenticated

class ListaAutocompletarView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        codigoModelo = raw.get('modelo')
        limite = raw.get('limite')
        if codigoModelo and (limite or limite == 0):      
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