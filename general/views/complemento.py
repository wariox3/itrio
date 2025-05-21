from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.complemento import GenComplemento
from general.serializers.complemento import GenComplementoSerializador
from utilidades.holmio import Holmio

class ComplementoViewSet(viewsets.ModelViewSet):
    queryset = GenComplemento.objects.all()
    serializer_class = GenComplementoSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar_action(self, request):             
        raw = request.data
        id = raw.get('id')            
        if id:
            complemento = GenComplemento.objects.get(pk=id)
            validado = False   
            if id == 1:
                holmio = Holmio()
                respuesta = holmio.estado()
                if respuesta['error'] == False:
                    validado = True
            if validado:
                return Response({'mensaje': 'complemento validado'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':f'Fallo la validacion', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                              
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     