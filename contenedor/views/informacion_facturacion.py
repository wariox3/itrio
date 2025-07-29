from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from contenedor.models import CtnInformacionFacturacion
from contenedor.serializers.informacion_facturacion import CtnInformacionFacturacionSerializador

class InformacionFacturacionViewSet(viewsets.ModelViewSet):
    queryset = CtnInformacionFacturacion.objects.all()
    serializer_class = CtnInformacionFacturacionSerializador    
    permission_classes = [permissions.AllowAny]   

    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:  
            informacionFacturacion = CtnInformacionFacturacion.objects.filter(usuario_id=usuario_id)                       
            informacionFacturacionSerializer = CtnInformacionFacturacionSerializador(informacionFacturacion, many=True)
            return Response({'informaciones_facturacion': informacionFacturacionSerializer.data}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)       