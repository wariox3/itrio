from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.archivo import GenArchivo
from general.serializers.archivo import GenArchivoSerializador

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = GenArchivo.objects.all()
    serializer_class = GenArchivoSerializador
    permission_classes = [permissions.IsAuthenticated]


     
          
      
    

