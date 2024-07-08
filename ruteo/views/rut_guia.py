from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.rut_guia import RutGuia
from ruteo.serializers.rut_guia import RutGuiaSerializador
import base64
from io import BytesIO
import openpyxl
from datetime import datetime

class RutGuiaViewSet(viewsets.ModelViewSet):
    queryset = RutGuia.objects.all()
    serializer_class = RutGuiaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            archivo_data = base64.b64decode(archivo_base64)
            archivo = BytesIO(archivo_data)
            wb = openpyxl.load_workbook(archivo)
            sheet = wb.active    
            for row in sheet.iter_rows(min_row=2, values_only=True):
                fecha_texto = str(row[1])
                fecha = datetime.strptime(fecha_texto, '%Y%m%d').date()
                data = {
                    'guia': row[0],
                    'fecha':fecha,
                    'documento': row[2],
                    'destinatario': row[3],
                    'destinatario_direccion': row[4],
                    'destinatario_telefono': row[5],
                    'destinatario_correo': row[6],
                    'peso': row[7],
                    'volumen': row[8],
                }
                guiaSerializador = RutGuiaSerializador(data=data)
                if guiaSerializador.is_valid():
                    guiaSerializador.save()
                else:
                    return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': guiaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'Se importo el archivo con exito'}, status=status.HTTP_200_OK)        
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)