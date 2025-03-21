from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.documento import GenDocumento
from rest_framework.permissions import IsAuthenticated

class InformeView(APIView):
    permission_classes = (IsAuthenticated,)

    def obtener_pendiente_corte(self, fecha_hasta):            
        query = f'''
            SELECT
                d.id,
                d.numero,
                d.fecha,
                d.fecha_vence,
                d.documento_tipo_id,
                d.subtotal,
                d.impuesto,
                d.total,
                dt.nombre as documento_tipo_nombre,
                c.numero_identificacion as contacto_numero_identificacion,
                c.nombre_corto as contacto_numero_nombre_corto,
                COALESCE(
                	(SELECT SUM(dd.precio) 
                		FROM gen_documento_detalle dd 
                		left join gen_documento ddd on dd.documento_id=ddd.id
                		WHERE dd.documento_afectado_id = d.id AND ddd.fecha <= '{fecha_hasta}')
                ,0) AS abono
            FROM
                gen_documento d
            left join
            	gen_documento_tipo dt on d.documento_tipo_id = dt.id 
           	left join 
           		gen_contacto c on d.contacto_id = c.id 
           	where dt.cobrar = true and d.fecha <= '{fecha_hasta}';
        '''
        documentos = GenDocumento.objects.raw(query)        
        resultados_json = []
        for documento in documentos:
            resultados_json.append({
                'id': documento.id,
                'numero': documento.numero,
                'fecha': documento.fecha,
                'fecha_vence': documento.fecha_vence,
                'documento_tipo_id': documento.documento_tipo_id,
                'subtotal': documento.subtotal,
                'impuesto': documento.impuesto,
                'total': documento.total,
                'documento_tipo_nombre': documento.documento_tipo_nombre,
                'contacto_numero_identificacion': documento.contacto_numero_identificacion,
                'contacto_numero_nombre_corto': documento.contacto_numero_nombre_corto,
                'abono': documento.abono,                
            })            
        resultados_json.sort(key=lambda x: str(x['codigo']))
        return resultados_json

    def post(self, request):    
        raw = request.data
        filtros = raw.get("filtros", [])
        excel = raw.get('excel', False)
        pdf = raw.get('pdf', False)        
        fecha_hasta = None
        for filtro in filtros:
            if filtro["propiedad"] == "fecha_hasta":
                fecha_hasta = filtro["valor1"]              
        
        if not fecha_hasta:
            return Response(
                {"error": "Los filtros 'fecha_desde' y 'fecha_hasta' son obligatorios."},status=status.HTTP_400_BAD_REQUEST)               
        resultados_movimiento = self.obtener_pendiente_corte(fecha_hasta)
        resultados_json = resultados_movimiento
        resultados_json.sort(key=lambda x: str(x['cuenta_codigo']))
        return Response({'registros': resultados_json}, status=status.HTTP_200_OK)
    
    def get(self, request):
        numero = 123  
        return Response("Esta es la respuesta" + numero)

