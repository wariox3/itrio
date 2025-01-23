from b2sdk.v2 import InMemoryAccountInfo, B2Api, UploadSourceBytes
from decouple import config
import base64
import io

class Backblaze():

    def __init__(self):   
        app_key_id = config('B2_APP_KEY_ID')
        app_key = config('B2_APP_KEY')     
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        self.b2_api.authorize_account("production", app_key_id, app_key)


    def subir_archivo(self, base64_data, nombre_archivo):
        bucket_nombre = config('B2_BUCKET_NAME')
        bucket = self.b2_api.get_bucket_by_name(bucket_nombre)
        if bucket is None:
            raise ValueError(f"El bucket '{bucket_nombre}' no existe.")         
        file_data = base64.b64decode(base64_data)                
        response = bucket.upload_bytes(
            file_data,
            nombre_archivo
        )                
        return response.id_, response.size, response.content_type   

    def descargar(self, archivo_id):
        bucket_nombre = config('B2_BUCKET_NAME')
        bucket = self.b2_api.get_bucket_by_name(bucket_nombre)
        if bucket is None:
            raise ValueError(f"El bucket '{bucket_nombre}' no existe.")         
                        
        downloaded_file = bucket.download_file_by_id(archivo_id)
        #downloaded_file.save_to("/home/desarrollo/Escritorio/prueba.png")    
        return downloaded_file.response


