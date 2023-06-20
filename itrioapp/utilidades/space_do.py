import boto3
import magic
from decouple import config 
from botocore.config import Config

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
        self.client.upload_file(pathArchivo, 'itrio', 'prueba/Captura.JPG')

    def put(self, pathArchivo):                      
        with open(pathArchivo, 'rb') as file:
            metadata = magic.from_file(pathArchivo, mime=True)
            self.client.put_object(Bucket='itrio',
                    Key='prueba/Captura.JPG',
                    Body=file,
                    ACL='private',
                    ContentType=metadata)    
