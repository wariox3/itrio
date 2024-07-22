from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from contenedor.models import InformacionFacturacion
from contenedor.serializers.informacion_facturacion import InformacionFacturacionSerializador

class InformacionFacturacionViewSet(viewsets.ModelViewSet):
    queryset = InformacionFacturacion.objects.all()
    serializer_class = InformacionFacturacionSerializador    
    permission_classes = [permissions.IsAuthenticated]   

    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:  
            informacionFacturacion = InformacionFacturacion.objects.filter(usuario_id=usuario_id)                       
            informacionFacturacionSerializer = InformacionFacturacionSerializador(informacionFacturacion, many=True)
            return Response({'informaciones_facturacion': informacionFacturacionSerializer.data}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)       