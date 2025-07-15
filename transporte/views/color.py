from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from transporte.models.color import TteColor
from transporte.serializers.color import TteColorSeleccionarSerializador, TteColorSerializador


class ColorViewSet(viewsets.ModelViewSet):
    queryset = TteColor.objects.all()
    serializer_class = TteColorSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre__icontains', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = TteColorSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)        