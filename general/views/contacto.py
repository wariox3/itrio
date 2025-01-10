from rest_framework import viewsets, permissions, status
from general.models.contacto import GenContacto
from general.models.identificacion import GenIdentificacion
from general.models.ciudad import GenCiudad
from general.models.plazo_pago import GenPlazoPago
from general.models.regimen import GenRegimen
from general.models.tipo_persona import GenTipoPersona
from general.serializers.contacto import GenContactoSerializador, GenContactoExcelSerializador
from rest_framework.response import Response
from rest_framework.decorators import action
from openpyxl import Workbook
from django.http import HttpResponse
from io import BytesIO
from utilidades.utilidades import Utilidades
import base64
import openpyxl
import gc

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = GenContacto.objects.all()
    serializer_class = GenContactoSerializador    
    permission_classes = [permissions.IsAuthenticated]               

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        relaciones = instance.contactos_rel.first()
        if relaciones:
            modelo_asociado = relaciones.__class__.__name__           
            return Response({'mensaje':f"El registro no se puede eliminar porque tiene registros asociados en {modelo_asociado}", 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["post"], url_path=r'excel',)
    def excel(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 5000)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = raw.get('filtros', [])        
        ordenamientos = raw.get('ordenamientos', [])    
        ordenamientos.append('-id')                 
        respuesta = ContactoViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)
        serializador = GenContactoExcelSerializador(respuesta['contactos'], many=True)
        contactos = serializador.data
        if contactos:
            field_names = list(contactos[0].keys())
        else:
            field_names = []

        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for row in contactos:
            row_data = [row[field] for field in field_names]
            ws.append(row_data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = 'attachment; filename=contactos.xlsx'
        wb.save(response)
        return response

    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):        
        raw = request.data
        identificacion_id = raw.get('identificacion_id')
        numero_identificacion = raw.get('numero_identificacion')
        if identificacion_id and numero_identificacion:
            try:
                contacto = GenContacto.objects.filter(identificacion_id=identificacion_id, numero_identificacion=numero_identificacion).first()
                if contacto:
                    return Response({'validacion': True, 'id': contacto.id}, status=status.HTTP_200_OK)
                else:
                    return Response({'validacion':False, 'codigo':15}, status=status.HTTP_200_OK)    
            except GenContacto.DoesNotExist:
                return Response({'validacion':False, 'codigo':15}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
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
                if row[0]:
                    contacto = GenContacto.objects.filter(numero_identificacion=row[0]).first()
                    if contacto:
                        continue
                data = {
                    'numero_identificacion': row[0],                    
                    'identificacion':row[1],
                    'nombre_corto':row[2],
                    'nombre1':row[3],
                    'nombre2':row[4],
                    'apellido1':row[5],
                    'apellido2':row[6],
                    'direccion':row[7],
                    'barrio':row[8],
                    'codigo_postal':row[9],
                    'ciudad':row[10],
                    'telefono':row[11],
                    'celular':row[12],
                    'correo':row[13],
                    'correo_facturacion_electronica':row[14],
                    'cliente':row[15],
                    'proveedor':row[16],
                    'empleado':row[17],
                    'plazo_pago':row[18],
                    'plazo_pago_proveedor':row[19],
                    'digito_verificacion': '0'
                }                   
                if data['identificacion'] == 6:
                    data['regimen'] = 2
                    data['tipo_persona'] = 2
                else:
                    data['regimen'] = 1
                    data['tipo_persona'] = 1  
                data['digito_verificacion'] = str(Utilidades.digito_verificacion(data['numero_identificacion']))
                serializer = GenContactoSerializador(data=data)
                if serializer.is_valid():
                    data_modelo.append(serializer.validated_data)
                    registros_importados += 1
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }                                    
                    errores_datos.append(error_dato)                    
            if not errores:
                for detalle in data_modelo:
                    GenContacto.objects.create(**detalle)
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        contactos = GenContacto.objects.all()
        if filtros:
            for filtro in filtros:
                contactos = contactos.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            contactos = contactos.order_by(*ordenamientos)              
        contactos = contactos[desplazar:limite+desplazar]
        itemsCantidad = GenContacto.objects.all()[:limiteTotal].count()                   
        respuesta = {'contactos': contactos, "cantidad_registros": itemsCantidad}
        return respuesta     
        