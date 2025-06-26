from rest_framework import viewsets, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from general.models.contacto import GenContacto
from general.models.identificacion import GenIdentificacion
from general.serializers.contacto import GenContactoSerializador, GenContactoListaSerializador, GenContactoSeleccionarSerializador
from general.filters.contacto import ContactoFilter
from utilidades.wolframio import Wolframio
from utilidades.excel_exportar import ExcelExportar
from io import BytesIO
from utilidades.utilidades import Utilidades
import base64
import openpyxl
import gc
from rest_framework.pagination import PageNumberPagination

class ContactoViewSet(viewsets.ModelViewSet):             
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ContactoFilter 
    queryset = GenContacto.objects.all()   
    serializadores = {'lista': GenContactoListaSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenContactoSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        page_size = self.request.query_params.get('page_size')
        if page_size:
            if page_size != '0':
                self.pagination_class = PageNumberPagination
                self.pagination_class.page_size = int(page_size)
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 

    def list(self, request, *args, **kwargs):
        if request.query_params.get('excel') or request.query_params.get('excel_masivo'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            exporter = ExcelExportar(serializer.data, sheet_name="contactos", filename="contactos.xlsx")
            if request.query_params.get('excel'):
                return exporter.exportar_estilo()
            if request.query_params.get('excel_masivo'):
                return exporter.exportar()
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre_corto = request.query_params.get('nombre_corto__icontains', None)
        cliente = request.query_params.get('cliente', None)
        queryset = self.get_queryset()
        if nombre_corto:
            queryset = queryset.filter(nombre_corto__icontains=nombre_corto)
        if cliente:
            queryset = queryset.filter(cliente=cliente)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = GenContactoSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        relaciones = instance.contactos_rel.first()
        if relaciones:
            modelo_asociado = relaciones.__class__.__name__           
            return Response({'mensaje':f"El registro no se puede eliminar porque tiene registros asociados en {modelo_asociado}", 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
                    'ciudad':row[9],
                    'telefono':row[10],
                    'celular':row[11],
                    'correo':row[12],
                    'correo_facturacion_electronica':row[13],
                    'cliente':row[14],
                    'proveedor':row[15],
                    'empleado':row[16],
                    'plazo_pago':row[17],
                    'plazo_pago_proveedor':row[18],
                    'banco':row[19],
                    'numero_cuenta':row[20],
                    'cuenta_banco_clase':row[21],
                    'digito_verificacion': '0'
                }                   
                if data['identificacion'] == 6 or data['identificacion'] == '6':
                    data['regimen'] = 1
                    data['tipo_persona'] = 1
                else:
                    data['regimen'] = 2
                    data['tipo_persona'] = 2
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

    @action(detail=False, methods=["post"], url_path=r'consulta-dian',)
    def consulta_dian_action(self, request):
        raw = request.data        
        nit = raw.get('nit') 
        identificacion_id = raw.get('identificacion_id') 
        if nit and identificacion_id:
            if identificacion_id in [3,6]:
                identificacion = GenIdentificacion.objects.get(pk=identificacion_id)
                datos = {'nit':nit, 'identificacion': identificacion.codigo}
                wolframio = Wolframio()
                respuesta = wolframio.contacto_consulta_nit(datos)
                if respuesta['error'] == False: 
                    return Response(respuesta['datos'], status=status.HTTP_200_OK)                          
                else:               
                    return Response({'mensaje':respuesta['mensaje'], 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Solo se pueden autocompletar NIT o Cedula', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        