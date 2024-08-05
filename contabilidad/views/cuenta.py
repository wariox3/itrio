from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.cuenta import ConCuenta
from contabilidad.serializers.cuenta import ConCuentaSerializador
from io import BytesIO
import base64
import openpyxl

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuenta.objects.all()
    serializer_class = ConCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar-detalle',)
    def importar_detalle(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active         
            except Exception as e:     
                return Response({'mensaje':'Error procesando el archivo', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
            data_documento_detalle = []
            errores = False
            errores_datos = []
            registros_importados = 0

            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'cuenta': row[0],
                    'numero_identificacion':row[1],
                    'debito': row[2] if row[2] is not None else 0,
                    'credito': row[3] if row[3] is not None else 0,
                    'base': row[4] if row[4] is not None else 0,
                    'descripcion': row[5]                    
                }                                    

            if errores == False:
                for detalle in data_documento_detalle:
                    '''GenDocumentoDetalle.objects.create(
                        documento=documento,
                        cuenta_id=detalle['cuenta_id'],
                        contacto_id=detalle['contacto_id'],
                        total=detalle['total'],
                        base_impuesto=detalle['base'],
                        naturaleza=detalle['naturaleza'],
                        detalle=detalle['descripcion']
                    )'''
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    