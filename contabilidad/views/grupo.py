from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.grupo import ConGrupo
from contabilidad.serializers.grupo import ConGrupoSerializador
from io import BytesIO
import base64
import openpyxl

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = ConGrupo.objects.all()
    serializer_class = ConGrupoSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'codigo': row[0],
                    'nombre':row[1],
                }  
                if not data['codigo']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un codigo'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['nombre']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar nombre'
                    }
                    errores_datos.append(error_dato)
                    errores = True 

                data_modelo.append(data)
            if errores == False:
                for detalle in data_modelo:
                    ConGrupo.objects.create(
                        codigo=detalle['codigo'],
                        nombre=detalle['nombre']                    
                    )
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    