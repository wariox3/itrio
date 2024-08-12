from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transporte.models.guia import TteGuia
from transporte.serializers.guia import GuiaSerializador


class GuiaViewSet(viewsets.ModelViewSet):
    queryset = TteGuia.objects.all()
    serializer_class = GuiaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar_ruteo',)
    def lista(self, request):
        raw = request.data
        return Response({'mensaje':'hola mundo'}, status=status.HTTP_200_OK)   