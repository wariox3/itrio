from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.categoria_licencia import VerCategoriaLicencia
from vertical.serializers.categoria_licencia import VerCategoriaLicenciaSerializador, VerCategoriaLicenciaSeleccionarSerializador

class CategoriaLicenciaViewSet(viewsets.ModelViewSet):
    queryset = VerCategoriaLicencia.objects.all()
    serializer_class = VerCategoriaLicenciaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = VerCategoriaLicenciaSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)       