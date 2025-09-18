from decimal import Decimal
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.parametro import VerParametro
from vertical.serializers.parametro import VerParametroSerializador

class ParametroViewSet(viewsets.ModelViewSet):
    queryset = VerParametro.objects.all()
    serializer_class = VerParametroSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path=r'version-ruteo',)
    def version_ruteo_action(self, request):        
        parametro = VerParametro.objects.filter(pk=1).values('version_ruteo').first()
        if not parametro:
            return Response({'mensaje': 'No se han establecido parametros'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'version': parametro['version_ruteo']}, status=status.HTTP_200_OK)
           