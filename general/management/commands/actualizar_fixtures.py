from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection
from django.db import models
import json
import os


class Command(BaseCommand):
    help = 'Comando para actualizar los fixtures'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta del archivo/directorio JSON')

    def handle(self, *args, **options):        
        schema = connection.schema_name
        json = options['json_file']
        if os.path.isfile(json):
            self.process_json_file(schema, json)
        elif os.path.isdir(json):
            json_files = [os.path.join(json, f) for f in os.listdir(json) if f.endswith('.json')]
            json_files = sorted(json_files)
            for json_file in json_files:                
                self.process_json_file(schema, json_file)
        else:
            self.stdout.write(self.style.ERROR('La ruta especificada no es un archivo ni un directorio'))    

    def process_json_file(self, schema, json_file):
        if schema != 'public':
            try:
                with open(json_file, 'r') as file:
                    actualizados = 0
                    creados = 0
                    nombre_archivo = os.path.basename(json_file)
                    data = json.load(file)                    
                    for item in data:
                        model_name = item.get('model')                    
                        pk = item.get('pk')                
                        fields = item.get('fields', {})                    
                        app_label, model_name = model_name.split('.')
                        Model = apps.get_model(app_label, model_name)
                        model_fields = [field.name for field in Model._meta.get_fields()]
                        filtered_fields = {}
                        for key, value in fields.items():
                            if key in model_fields:
                                field = Model._meta.get_field(key)
                                if isinstance(field, models.ForeignKey):
                                    related_model = field.related_model
                                    try:
                                        related_instance = related_model.objects.get(pk=value)
                                        filtered_fields[key] = related_instance
                                    except related_model.DoesNotExist:
                                        self.stdout.write(self.style.ERROR(f'El objeto relacionado {related_model} con pk={value} no existe.'))
                                        continue
                                else:
                                    filtered_fields[key] = value
                        instance, created = Model.objects.update_or_create(pk=pk, defaults=filtered_fields)                    
                        if created:
                            creados += 1
                        else:
                            actualizados += 1
                    self.stdout.write(self.style.SUCCESS(f'Registros creados {creados} actualizados {actualizados} modelo {nombre_archivo}'))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR('El archivo JSON no existe'))