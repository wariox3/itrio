from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.contrato import HumContrato
from humano.serializers.contrato import HumContratoSerializador
from django.db.models.deletion import ProtectedError
from datetime import datetime
import base64
from io import BytesIO
import openpyxl
import gc

class HumMovimientoViewSet(viewsets.ModelViewSet):
    queryset = HumContrato.objects.all()
    serializer_class = HumContratoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raw = request.data        
        contacto_id = raw.get('contacto')
        contrato_activo = HumContrato.objects.filter(contacto_id=contacto_id, estado_terminado=False).exists()    
        if contrato_activo:
            return Response({'mensaje':'El contacto ya tiene un contrato activo', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'mensaje':'Contrato eliminado'}, status=status.HTTP_200_OK)
        except ProtectedError as e:
            return Response({'mensaje':'El contrato tiene relaciones', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)   

    def perform_destroy(self, instance):
        instance.delete()    

    @action(detail=False, methods=["post"], url_path=r'terminar',)
    def terminar(self, request):
        raw = request.data
        id = raw.get('id')
        fecha_terminacion = raw.get('fecha_terminacion')
        if id and fecha_terminacion:
            try:
                contrato = HumContrato.objects.get(pk=id)
                if contrato.estado_terminado == False:
                    fecha_terminacion = datetime.strptime(fecha_terminacion, '%Y-%m-%d').date()
                    if fecha_terminacion > contrato.fecha_desde:
                        contrato.fecha_hasta = fecha_terminacion
                        contrato.estado_terminado = True
                        contrato.save()
                        return Response({'mensaje': 'Contrato finalizado'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje':'No puede terminar el contrato antes de su inicio', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'El contrato ya esta terminado', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except HumContrato.DoesNotExist:
                return Response({'mensaje':'El contrato no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)         
        

    # @action(detail=False, methods=["post"], url_path=r'importar',)
    # def importar(self, request):
    #     raw = request.data        
    #     archivo_base64 = raw.get('archivo_base64')        
    #     if archivo_base64:
    #         try:
    #             archivo_data = base64.b64decode(archivo_base64)
    #             archivo = BytesIO(archivo_data)
    #             wb = openpyxl.load_workbook(archivo)
    #             sheet = wb.active    
    #         except Exception as e:     
    #             return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
    #         data_modelo = []
    #         errores = False
    #         errores_datos = []
    #         registros_importados = 0
    #         for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
    #             data = {
    #                 'contacto_id': row[0],                    
    #                 'contrato_tipo_id':row[1],
    #                 'fecha_desde':row[2],
    #                 'fecha_hasta':row[3],
    #                 'grupo_id':row[4],
    #                 'vr_salario':row[5],
    #                 'auxilio_transporte':row[6],
    #                 'direccion':row[7],
    #                 'barrio':row[8],
    #                 'codigo_postal':row[9],
    #                 'ciudad':row[10],
    #                 'telefono':row[11],
    #                 'celular':row[12],
    #                 'correo':row[13],
    #                 'correo_facturacion_electronica':row[14],
    #                 'cliente':row[15],
    #                 'proveedor':row[16],
    #                 'empleado':row[17],
    #                 'plazo_pago':row[18],
    #                 'plazo_pago_proveedor':row[19],
    #                 'digito_verificacion': '0'
    #             }                   
    #             if data['identificacion'] == 6 or data['identificacion'] == '6':
    #                 data['regimen'] = 1
    #                 data['tipo_persona'] = 1
    #             else:
    #                 data['regimen'] = 2
    #                 data['tipo_persona'] = 2
    #             data['digito_verificacion'] = str(Utilidades.digito_verificacion(data['numero_identificacion']))
    #             serializer = GenContactoSerializador(data=data)
    #             if serializer.is_valid():
    #                 data_modelo.append(serializer.validated_data)
    #                 registros_importados += 1
    #             else:
    #                 errores = True
    #                 error_dato = {
    #                     'fila': i,
    #                     'errores': serializer.errors
    #                 }                                    
    #                 errores_datos.append(error_dato)                    
    #         if not errores:
    #             # for detalle in data_modelo:
    #             #     GenContacto.objects.create(**detalle)
    #             # gc.collect()
    #             return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
    #         else:
    #             gc.collect()                    
    #             return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
    #     else:
    #         return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)