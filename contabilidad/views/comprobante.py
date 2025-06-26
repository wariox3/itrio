from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from contabilidad.models.comprobante import ConComprobante
from contabilidad.serializers.comprobante import ConComprobanteSerializador, ConComprobanteSeleccionarSerializar
from io import BytesIO
import base64
import openpyxl

class ComprobanteViewSet(viewsets.ModelViewSet):
    queryset = ConComprobante.objects.all()
    serializer_class = ConComprobanteSerializador
    permission_classes = [permissions.IsAuthenticated]
  
    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre__icontains', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre=nombre)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = ConComprobanteSeleccionarSerializar(queryset, many=True)        
        return Response(serializer.data)    

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
                    'permite_asiento': row[2]
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

                if not data['permite_asiento']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si la cuenta permite movimiento'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['permite_asiento'] in ['SI', 'NO']:
                        data['permite_asiento'] = data['permite_asiento'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                data_modelo.append(data)
            if errores == False:
                for detalle in data_modelo:
                    ConComprobante.objects.create(
                        codigo=detalle['codigo'],
                        nombre=detalle['nombre'],
                        permite_asiento=detalle['permite_asiento']
                    )
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     