import boto3
import base64
#import magic
from decouple import config 
from botocore.config import Config
from io import BytesIO

class SpaceDo():
    #documentacion: https://docs.digitalocean.com/products/spaces/reference/s3-sdk-examples/
        #Listar los buckets
        #response = client.list_buckets()
        #for space in response['Buckets']:
        #    print(space['Name'])
        #Listar archivos del bucket
        #response = client.list_objects(Bucket='semantica')
        #for obj in response['Contents']:
        #    print(obj['Key'])


    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client('s3',
                            config=Config(s3={'addressing_style': 'virtual'}),
                            region_name=config('DO_REGION'),
                            endpoint_url='https://fra1.digitaloceanspaces.com',                        
                            aws_access_key_id=config('DO_CLAVE_ACCESO'),
                            aws_secret_access_key=config('DO_CLAVE_SECRETA')) 

    def upload(self, pathArchivo):                                
        self.client.upload_file(pathArchivo, config('DO_BUCKET'), 'prueba/Captura.JPG')

    def put(self, pathArchivo, pathDestino):
        with open(pathArchivo, 'rb') as file:
            #metadata = magic.from_file(pathArchivo, mime=True)
            metadata = ''
            self.client.put_object(Bucket=config('DO_BUCKET'),
                    #Key='prueba/logo_ejemplo.jpg',
                    Key=pathDestino,
                    Body=file,
                    ACL='public-read',
                    ContentType=metadata)
            
    def putB64(self, pathDestino, b64, contentType):
        imagen_bytes = base64.b64decode(b64)
        imagen_temporal = BytesIO(imagen_bytes)
        imagen_temporal.seek(0)
        extra_args = {
            'ACL': 'public-read',
            'ContentType': contentType
            }
        self.client.upload_fileobj(imagen_temporal, config('DO_BUCKET'), pathDestino, ExtraArgs=extra_args)    

    def eliminar(self, pathDestino):
        self.client.delete_object(Bucket=config('DO_BUCKET'), Key=pathDestino)
