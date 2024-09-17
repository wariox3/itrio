from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from general.models.documento import GenDocumento
from rest_framework.permissions import IsAuthenticated
from general.views.documento import DocumentoViewSet

class PendienteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = [{'propiedad':'cobrar_pendiente__gt', 'valor_1':0}] 
        #raw.get('filtros')
        ordenamientos = raw.get('ordenamientos')                                     
        return Response("reractorizar", status=status.HTTP_200_OK)
