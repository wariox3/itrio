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
import base64
import openpyxl

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
        solo_nuevos = raw.get('solo_nuevos', False)
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
                if solo_nuevos:
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
                    'cliente':row[14],
                    'proveedor':row[15],
                    'empleado':row[16],
                    'plazo_pago':row[17],
                    'plazo_pago_proveedor':row[18],
                }  
                if not data['numero_identificacion']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un numero_identificacion'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    contacto = GenContacto.objects.filter(numero_identificacion=data['numero_identificacion']).first()
                    if contacto:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El contacto con numero de identificacion {data["numero_identificacion"]} ya existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True

                if not data['nombre_corto']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un nombre o razon social'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['direccion']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar una direccion'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['telefono']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un telefono'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['correo']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un correo'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['identificacion']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el tipo de identificacion'
                    }
                    errores_datos.append(error_dato)
                    errores = True  
                else:
                    identificacion = GenIdentificacion.objects.filter(codigo=data['identificacion']).first()
                    if identificacion is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'La identificacion con codigo {data["identificacion"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['identificacion_id'] = identificacion.id 
                        if data['identificacion_id'] == 6:
                            data['regimen_id'] = 1
                            data['tipo_persona_id'] = 1
                        else:
                            data['regimen_id'] = 2
                            data['tipo_persona_id'] = 2

                if not data['ciudad']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar la ciudad'
                    }
                    errores_datos.append(error_dato)
                    errores = True  
                else:
                    ciudad = GenCiudad.objects.filter(id=data['ciudad']).first()
                    if ciudad is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'La ciudad con codigo {data["ciudad"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['ciudad_id'] = ciudad.id

                if not data['cliente']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si el contacto es cliente'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['cliente'] in ['SI', 'NO']:
                        data['cliente'] = data['cliente'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True

                if not data['proveedor']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si el contacto es proveedor'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['proveedor'] in ['SI', 'NO']:
                        data['proveedor'] = data['proveedor'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True

                if not data['empleado']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si el contacto es empleado'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['empleado'] in ['SI', 'NO']:
                        data['empleado'] = data['empleado'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True

                if not data['plazo_pago']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el plazo de pago cliente'
                    }
                    errores_datos.append(error_dato)
                    errores = True  
                else:
                    plazo_pago = GenPlazoPago.objects.filter(id=data['plazo_pago']).first()
                    if plazo_pago is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El plazo de pago cliente con codigo {data["plazo_pago"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['plazo_pago_id'] = plazo_pago.id

                if not data['plazo_pago_proveedor']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el plazo de pago proveedor'
                    }
                    errores_datos.append(error_dato)
                    errores = True  
                else:
                    plazo_pago_proveedor = GenPlazoPago.objects.filter(id=data['plazo_pago_proveedor']).first()
                    if plazo_pago_proveedor is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El plazo de pago proveedor con codigo {data["plazo_pago_proveedor"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['plazo_pago_proveedor_id'] = plazo_pago_proveedor.id

                data_modelo.append(data)
            if errores == False:
                for detalle in data_modelo:
                    GenContacto.objects.create(
                        numero_identificacion=detalle['numero_identificacion'],                        
                        identificacion_id=detalle['identificacion_id'],
                        nombre_corto=detalle['nombre_corto'],
                        nombre1=detalle['nombre1'],
                        nombre2=detalle['nombre2'],
                        apellido1=detalle['apellido1'],
                        apellido2=detalle['apellido2'],
                        direccion=detalle['direccion'],
                        barrio=detalle['barrio'],
                        codigo_postal=detalle['codigo_postal'],
                        ciudad_id=detalle['ciudad_id'],
                        telefono=detalle['telefono'],
                        celular=detalle['celular'],
                        correo=detalle['correo'],
                        cliente=detalle['cliente'],
                        proveedor=detalle['proveedor'],
                        empleado=detalle['empleado'],
                        plazo_pago_id=detalle['plazo_pago_id'],
                        plazo_pago_proveedor_id=detalle['plazo_pago_proveedor_id'],
                        regimen_id=detalle['regimen_id'],
                        tipo_persona_id=detalle['tipo_persona_id'],
                    )
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
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
        