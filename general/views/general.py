from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from importlib import import_module
import re

class ListaAdministradorView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        modelo_nombre = raw.get('modelo')
        if modelo_nombre:
            aplicacion_prefijo = modelo_nombre[:3].lower()
            modelo_serializado_nombre = modelo_nombre[3:]        
            aplicaciones = {
                'hum': 'humano',
                'con': 'contabilidad',
                'ven': 'venta'
            }
            aplicacion = aplicaciones.get(aplicacion_prefijo, 'general')
            if aplicacion_prefijo not in aplicaciones:
                aplicacion_prefijo = 'gen'
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', modelo_serializado_nombre)            
            # Quitar este if cuando se organicen las entidades de general
            if aplicacion == 'general':
                serializador_nombre = modelo_nombre.lower()
            else:
                serializador_nombre = aplicacion_prefijo + '_' + re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()            
            modulo = import_module(f'{aplicacion}.serializers.{serializador_nombre}')            
            modelo = apps.get_model(aplicacion, modelo_nombre)
            serializador = getattr(modulo, f'{modelo_nombre}Serializador')

            desplazar = raw.get('desplazar', 0)
            limite = raw.get('limite', 50)    
            cantidadLimite = raw.get('cantidad_limite', 5000)    
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')
            items = modelo.objects.all()
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)              
            items = items[desplazar:limite+desplazar]
            itemsCantidad = modelo.objects.all()[:cantidadLimite].count()
            serializadorDatos = serializador(items, many=True) 
            return Response({"registros": serializadorDatos.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

class ListaAutocompletarView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        modelo_nombre = raw.get('modelo')
        limite = raw.get('limite', 10)
        if modelo_nombre:      
            aplicacion_prefijo = modelo_nombre[:3].lower()
            modelo_serializado_nombre = modelo_nombre[3:]        
            aplicaciones = {
                'hum': 'humano',
                'con': 'contabilidad',
                'ven': 'venta'
            }
            aplicacion = aplicaciones.get(aplicacion_prefijo, 'general')
            if aplicacion_prefijo not in aplicaciones:
                aplicacion_prefijo = 'gen'
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', modelo_serializado_nombre)            
            # Quitar este if cuando se organicen las entidades de general
            if aplicacion == 'general':
                serializador_nombre = modelo_nombre.lower()
            else:
                serializador_nombre = aplicacion_prefijo + '_' + re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()            
            modulo = import_module(f'{aplicacion}.serializers.{serializador_nombre}')            
            modelo = apps.get_model(aplicacion, modelo_nombre)
            serializador = getattr(modulo, f'{modelo_nombre}Serializador')
            
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')                     
            items = modelo.objects.all()
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)                          
            if limite > 0:
                items = items[0:limite]
            datos = serializador(items, many=True)    
            return Response({"registros": datos.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
    
class ListaBuscarView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        codigoModelo = raw.get('modelo')
        limite = raw.get('limite', 10)
        if codigoModelo:      
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')
            modelo = globals()[codigoModelo]
            serializadorNombre = f"{codigoModelo}ListaBuscarSerializador"
            serializador = globals()[serializadorNombre]            
            items = modelo.objects.all()
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)                          
            if limite > 0:
                items = items[0:limite]
            datos = serializador(items, many=True)    
            return Response({"registros": datos.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    