from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.periodo import ConPeriodo
from contabilidad.serializers.periodo import ConPeriodoSerializador

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = ConPeriodo.objects.all()
    serializer_class = ConPeriodoSerializador
    permission_classes = [permissions.IsAuthenticated]  

    @action(detail=False, methods=["post"], url_path=r'generar',)
    def generar(self, request):
        raw = request.data        
        anio = raw.get('anio')
        if anio:
            periodo = ConPeriodo.objects.filter(anio=anio).first()
            if periodo is None:
                for i in range(1, 14):
                    codigo = f"{anio}{str(i).zfill(2)}"
                    ConPeriodo.objects.create(id=codigo, anio=anio, mes=i)
                return Response({'mensaje': 'Se generan los periodos del año'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': 'Ya existen periodos con este año'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    