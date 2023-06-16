import boto3
from botocore.config import Config
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from decouple import config 
import base64
import magic

def vistaTamplate(request):
    return render(request, "general/prueba.html")

def vista(request):
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
    return HttpResponse("Hola mundo")

class PruebaView(APIView):
    def get(self, request):
        #documentacion: https://docs.digitalocean.com/products/spaces/reference/s3-sdk-examples/
        session = boto3.session.Session()
        client = session.client('s3',
                        config=Config(s3={'addressing_style': 'virtual'}),
                        region_name=config('DO_REGION'),
                        endpoint_url='https://sfo3.digitaloceanspaces.com',
                        aws_access_key_id=config('DO_CLAVE_ACCESO'),
                        aws_secret_access_key=config('DO_CLAVE_SECRETA'))             
        
        #Listar los buckets
        #response = client.list_buckets()
        #for space in response['Buckets']:
        #    print(space['Name'])
        #Listar archivos del bucket
        #response = client.list_objects(Bucket='semantica')
        #for obj in response['Contents']:
        #    print(obj['Key'])
        pathArchivo = '/home/desarrollo/Escritorio/Captura.JPG';
        with open(pathArchivo, 'rb') as archivo:
            contenido = archivo.read()
            contenido_codificado = base64.b64encode(contenido)
            contenido_codificado_str = contenido_codificado.decode('utf-8')
            metadata = magic.from_file(pathArchivo, mime=True)
            client.put_object(Bucket='semantica',
                    Key='itrio/Captura.JPG',
                    Body=contenido_codificado_str,
                    ACL='private',
                    Metadata={
                        'ContentType': metadata
                    }
                    )      
        prueba = config('KEY_SENDGRID')
        return Response("Hola mundo" + prueba)

