from general.models.archivo import GenArchivo
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
import requests
import json


class ArchivoServicio():

    @staticmethod
    def cargar_modelo(archivo_base64, nombre_archivo, codigo, modelo, tenant):        
        if archivo_base64 and nombre_archivo and codigo and modelo:                                            
            try:                        
                objeto_base64 = Utilidades.separar_base64(archivo_base64)
                backblaze = Backblaze()
                id, tamano, tipo, uuid = backblaze.subir(objeto_base64['base64_raw'], tenant, nombre_archivo)
                archivo = GenArchivo()
                archivo.archivo_tipo_id = 2
                archivo.almacenamiento_id = id
                archivo.nombre = nombre_archivo
                archivo.tipo = tipo
                archivo.tamano = tamano
                archivo.uuid = uuid
                archivo.codigo = codigo
                archivo.modelo = modelo
                archivo.save()
                return {'error':False, 'id':str(archivo.id)}                                         
            except ValueError as e:
                return {'error':True, 'mensaje':str(e)}                
        else:
            return {'error':True, 'mensaje': 'Faltan parametros'}