from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.models.cuenta_clase import ConCuentaClase
from contabilidad.models.cuenta_grupo import ConCuentaGrupo
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta
from contabilidad.models.cuenta_subcuenta import ConCuentaSubcuenta
from general.models.documento_detalle import GenDocumentoDetalle
from contabilidad.serializers.cuenta import ConCuentaSerializador
from django.db.models import ProtectedError
from io import BytesIO
import base64
import openpyxl
import gc

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuenta.objects.all()
    serializer_class = ConCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        try:            
            self.perform_destroy(instance)
        except ProtectedError:            
            return Response({'mensaje': 'No se puede eliminar porque está relacionado con otros registros.'}, status=status.HTTP_400_BAD_REQUEST)        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        raw = request.data        
        codigo = raw.get('codigo')
        validar_cuenta = ConCuenta.objects.filter(codigo=codigo).exists()    
        if validar_cuenta:
            return Response({'mensaje':'Ya existe una cuenta con este codigo', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            archivo_data = base64.b64decode(archivo_base64)
            archivo = BytesIO(archivo_data)
            wb = openpyxl.load_workbook(archivo)
            sheet = wb.active    
            data_modelo = []
            errores = False
            errores_datos = []                
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):                
                if len(row) < 6:
                    return Response({'mensaje':'El archivo no tiene la estructura requerida', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                
                data = {
                    'codigo': row[0],
                    'nombre':row[1],            
                    'exige_tercero': row[2],
                    'exige_base': row[3],
                    'exige_grupo': row[4],
                    'permite_movimiento': row[5],
                    'cuenta_clase': None,
                    'cuenta_grupo': None,
                    'cuenta_cuenta': None,
                    'cuenta_subcuenta': None,
                    'nivel': None                    
                } 


                if data['codigo']:
                    codigo_str = str(data['codigo'])
                    longitud_codigo = len(codigo_str)                    
                    if longitud_codigo >= 1:
                        data['cuenta_clase'] = codigo_str[0]
                    if longitud_codigo >= 2:
                        data['cuenta_grupo'] = codigo_str[:2]
                    if longitud_codigo >= 4:                            
                        data['cuenta_cuenta'] = codigo_str[:4]
                    #if longitud_codigo >= 6:                            
                    #    data['cuenta_subcuenta'] = codigo_str[:6]

                    if longitud_codigo <= 1:
                        data['nivel'] = 1
                    if longitud_codigo > 1 and longitud_codigo <= 2:
                        data['nivel'] = 2
                    if longitud_codigo > 2 and longitud_codigo <= 4:
                        data['nivel'] = 3  
                    if longitud_codigo > 4 and longitud_codigo <= 6:
                        data['nivel'] = 4
                    if longitud_codigo > 6 and longitud_codigo <= 8:
                        data['nivel'] = 5

                serializer = ConCuentaSerializador(data=data)
                if serializer.is_valid():
                    data_modelo.append(serializer.validated_data)
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }
                    errores_datos.append(error_dato)
            if not errores:
                for detalle in data_modelo:
                    ConCuenta.objects.create(**detalle)
                gc.collect()
                return Response({'mensaje': 'Se importó el archivo con éxito'}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)                                    
            
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
  
    @action(detail=False, methods=["post"], url_path=r'trasladar',)
    def trasladar(self, request):
        raw = request.data
        cuenta_origen_id = raw.get('cuenta_origen_id')
        cuenta_destino_id = raw.get('cuenta_destino_id')
        if cuenta_origen_id and cuenta_destino_id:
            if cuenta_origen_id != cuenta_destino_id:
                try:
                    cuenta_origen = ConCuenta.objects.get(pk=cuenta_origen_id)  
                    cuenta_destino = ConCuenta.objects.get(pk=cuenta_destino_id)  
                    
                    ConMovimiento.objects.filter(cuenta_id=cuenta_origen_id).update(cuenta_id=cuenta_destino_id)
                    GenDocumentoDetalle.objects.filter(cuenta_id=cuenta_origen_id).update(cuenta_id=cuenta_destino_id)
                    return Response({'mensaje': 'Se trasladaron los movimientos con éxito'}, status=status.HTTP_200_OK)

                except ConCuenta.DoesNotExist:
                    return Response({'mensaje':'La cuenta no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje': 'Las cuentas no pueden ser iguales', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    