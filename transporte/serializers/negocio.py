from rest_framework import serializers
from transporte.models.negocio import TteNegocio


class TteNegocioSerializador(serializers.ModelSerializer):   

    class Meta:
        model = TteNegocio
        fields = ['id', 'fecha', 'fecha_registro', 'unidades' , 'peso', 'volumen', 'declara' ,'pago', 
                  'flete' , 'manejo', 'comentario', 'contacto', 'ciudad_origen' , 'ciudad_destino']
        select_related_fields = ['contacto', 'ciudad_origen', 'ciudad_destino']  
    
 