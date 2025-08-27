from rest_framework import serializers
from vertical.models.conductor import VerConductor

class VerConductorSerializador(serializers.ModelSerializer):
    categoria_licencia__nombre = serializers.CharField(source='categoria_licencia.nombre', read_only=True, allow_null=True, default=None)
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = VerConductor
        fields = ['id', 'identificacion' ,'numero_identificacion', 'nombre_corto', 'nombre1', 'nombre2', 'apellido1', 'apellido2', 'ciudad', 'ciudad__nombre',
                  'direccion', 'barrio', 'telefono', 'celular','correo', 'numero_licencia', 'fecha_vence_licencia', 'categoria_licencia', 'categoria_licencia__nombre']
        select_related_fields = ['categoria_licencia', 'ciudad', 'identificacion']      