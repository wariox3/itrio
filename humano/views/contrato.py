from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.contrato import HumContrato
from humano.models.grupo import HumGrupo
from humano.models.cargo import HumCargo
from humano.models.sucursal import HumSucursal
from humano.models.riesgo import HumRiesgo
from humano.models.salud import HumSalud
from humano.models.pension import HumPension
from humano.models.tipo_cotizante import HumTipoCotizante
from humano.models.subtipo_cotizante import HumSubtipoCotizante
from humano.models.entidad import HumEntidad
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from humano.models.contrato_tipo import HumContratoTipo
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
                    'contacto': row[0],
                    'contrato_tipo': row[1],
                    'fecha_desde': row[2],
                    'fecha_hasta': row[3],
                    'salario': row[4],
                    'auxilio_transporte': row[5],
                    'salario_integral': row[6],
                    'grupo': row[7],
                    'cargo': row[8],
                    'ciudad_contrato': row[9],
                    'ciudad_labora': row[10],
                    'sucursal': row[11],
                    'riesgo': row[12],
                    'tipo_cotizante': row[13],
                    'subtipo_cotizante': row[14],
                    'salud': row[15],
                    'pension': row[16],
                    'entidad_salud': row[17],
                    'entidad_pension': row[18],
                    'entidad_cesantias': row[19],
                    'entidad_caja': row[20],
                    'comentario': row[21],
                    'estado_terminado' : False
                }

                if row[2]:
                    fechaDesde = str(row[2])   
                    fecha_valida = datetime.strptime(fechaDesde, "%Y%m%d").date()
                    data['fecha_desde'] = fecha_valida

                if row[3]:
                    fechaHasta = str(row[3])
                    fecha_valida = datetime.strptime(fechaHasta, "%Y%m%d").date()
                    data['fecha_hasta'] = fecha_valida

                # Validación 1: Fecha hasta no puede ser inferior a fecha desde
                if data['fecha_hasta'] and data['fecha_desde'] and data['fecha_hasta'] < data['fecha_desde']:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'fecha_hasta': ['La fecha hasta no puede ser inferior a la fecha desde.']
                        }
                    }
                    errores_datos.append(error_dato)
                    continue

                # Validación 2: Si contrato_tipo es 1, las fechas deben ser iguales
                if data['contrato_tipo'] == 1 and data['fecha_desde'] != data['fecha_hasta']:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'fecha_desde': ['Para el tipo de contrato 1 indefinido, las fechas desde y hasta deben ser iguales.']
                        }
                    }
                    errores_datos.append(error_dato)
                    continue

                if data['contacto']:
                    contacto = GenContacto.objects.filter(id=data['contacto']).first()
                    if contacto:
                        data['contacto'] = contacto.id

                        contrato_activo = HumContrato.objects.filter(contacto_id=contacto.id, estado_terminado=False).exists()
                        if contrato_activo:
                            errores = True
                            error_dato = {
                                'fila': i,
                                'errores': {
                                    'contacto': ['El contacto ya tiene un contrato activo.']
                                }
                            }
                            errores_datos.append(error_dato)
                            continue


                if data['contrato_tipo']:
                    contratoTipo = HumContratoTipo.objects.filter(id=data['contrato_tipo']).first()
                    if contratoTipo:
                        data['contrato_tipo'] = contratoTipo.id

                if data['grupo']:
                    grupo = HumGrupo.objects.filter(id=data['grupo']).first()
                    if grupo:
                        data['grupo'] = grupo.id

                if data['cargo']:
                    cargo = HumCargo.objects.filter(id=data['cargo']).first()
                    if cargo:
                        data['cargo'] = cargo.id

                if data['ciudad_contrato']:
                    ciudadContrato = GenCiudad.objects.filter(id=data['ciudad_contrato']).first()
                    if cargo:
                        data['ciudad_contrato'] = ciudadContrato.id

                if data['ciudad_labora']:
                    ciudadLabora = GenCiudad.objects.filter(id=data['ciudad_labora']).first()
                    if ciudadLabora:
                        data['ciudad_labora'] = ciudadLabora.id

                if data['sucursal']:
                    sucursal = HumSucursal.objects.filter(id=data['sucursal']).first()
                    if sucursal:
                        data['sucursal'] = sucursal.id

                if data['riesgo']:
                    riesgos = HumRiesgo.objects.filter(id=data['riesgo']).first()
                    if riesgos:
                        data['riesgo'] = riesgos.id

                if data['tipo_cotizante']:
                    tipoCotizante = HumTipoCotizante.objects.filter(id=data['tipo_cotizante']).first()
                    if tipoCotizante:
                        data['tipo_cotizante'] = tipoCotizante.id

                if data['subtipo_cotizante']:
                    subtipoCotizante = HumSubtipoCotizante.objects.filter(id=data['subtipo_cotizante']).first()
                    if subtipoCotizante:
                        data['subtipo_cotizante'] = subtipoCotizante.id

                if data['salud']:
                    salud = HumSalud.objects.filter(id=data['salud']).first()
                    if salud:
                        data['salud'] = salud.id

                if data['pension']:
                    pension = HumPension.objects.filter(id=data['pension']).first()
                    if pension:
                        data['pension'] = pension.id

                if data['entidad_salud']:
                    entidadSalud = HumEntidad.objects.filter(id=data['entidad_salud']).first()
                    if entidadSalud:
                        data['entidad_salud'] = entidadSalud.id

                        if not entidadSalud.salud:
                            errores = True
                            error_dato = {
                                'fila': i,
                                'errores': {
                                    'entidad_salud': ['La entidad no está marcada como salud.']
                                }
                            }
                            errores_datos.append(error_dato)
                            continue


                if data['entidad_salud']:
                    entidadPension = HumEntidad.objects.filter(id=data['entidad_pension']).first()
                    if entidadPension:
                        data['entidad_pension'] = entidadPension.id

                        if not entidadPension.pension:
                            errores = True
                            error_dato = {
                                'fila': i,
                                'errores': {
                                    'entidad_pension': ['La entidad no está marcada como pension.']
                                }
                            }
                            errores_datos.append(error_dato)
                            continue


                if data['entidad_cesantias']:
                    entidadeCesantia = HumEntidad.objects.filter(id=data['entidad_cesantias']).first()
                    if entidadeCesantia:
                        data['entidad_cesantias'] = entidadeCesantia.id

                        if not entidadeCesantia.cesantias:
                            errores = True
                            error_dato = {
                                'fila': i,
                                'errores': {
                                    'entidad_cesantias': ['La entidad no está marcada como cesantias.']
                                }
                            }
                            errores_datos.append(error_dato)
                            continue
                        

                if data['entidad_caja']:
                    entidadCaja = HumEntidad.objects.filter(id=data['entidad_caja']).first()
                    if entidadCaja:
                        data['entidad_caja'] = entidadCaja.id

                        if not entidadCaja.caja:
                            errores = True
                            error_dato = {
                                'fila': i,
                                'errores': {
                                    'entidad_caja': ['La entidad no está marcada como caja.']
                                }
                            }
                            errores_datos.append(error_dato)
                            continue


                serializer = HumContratoSerializador(data=data)
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
                    HumContrato.objects.create(**detalle)
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)