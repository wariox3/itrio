from general.models.contacto import Contacto, Ciudad, Identificacion, Regimen, TipoPersona, GenAsesor, Precio, PlazoPago
from rest_framework import serializers

class ContactoSerializador(serializers.HyperlinkedModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    ciudad = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())    
    tipo_persona = serializers.PrimaryKeyRelatedField(queryset=TipoPersona.objects.all())
    regimen = serializers.PrimaryKeyRelatedField(queryset=Regimen.objects.all())
    asesor = serializers.PrimaryKeyRelatedField(queryset=GenAsesor.objects.all(), allow_null=True, required=False)
    precio = serializers.PrimaryKeyRelatedField(queryset=Precio.objects.all(), allow_null=True, required=False)
    plazo_pago = serializers.PrimaryKeyRelatedField(queryset=PlazoPago.objects.all(), allow_null=True, required=False)
    plazo_pago_proveedor = serializers.PrimaryKeyRelatedField(queryset=PlazoPago.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Contacto
        fields = [
            'id', 'identificacion', 'numero_identificacion', 'digito_verificacion', 'nombre_corto', 'nombre1', 'nombre2', 'apellido1', 'apellido2',
            'direccion', 'ciudad', 'barrio', 'codigo_postal', 'telefono', 'celular', 'correo', 'tipo_persona', 'regimen', 'codigo_ciuu',
            'asesor', 'precio', 'plazo_pago', 'plazo_pago_proveedor', 'cliente', 'proveedor', 'empleado']  
        
    def to_representation(self, instance):
        asesor = instance.asesor
        asesor_nombre_corto = None
        if asesor:
            asesor_nombre_corto = asesor.nombre_corto
        precio = instance.precio
        precio_nombre = None
        if precio:
            precio_nombre = precio.nombre
        plazo_pago = instance.plazo_pago
        plazo_pago_nombre = None
        plazo_pago_dias = 0
        if plazo_pago:
            plazo_pago_nombre = plazo_pago.nombre
            plazo_pago_dias = plazo_pago.dias
        plazo_pago_proveedor = instance.plazo_pago_proveedor
        plazo_pago_proveedor_nombre = None
        plazo_pago_proveedor_dias = 0
        if plazo_pago_proveedor:
            plazo_pago_proveedor_nombre = plazo_pago_proveedor.nombre
            plazo_pago_proveedor_dias = plazo_pago_proveedor.dias            
        return {
            'id': instance.id,
            'identificacion_id': instance.identificacion_id, 
            'identificacion_abreviatura': instance.identificacion.abreviatura, 
            'numero_identificacion': instance.numero_identificacion,
            'digito_verificacion': instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'nombre1': instance.nombre1,
            'nombre2': instance.nombre2,
            'apellido1': instance.apellido1,
            'apellido2': instance.apellido2,
            'correo': instance.correo,
            'telefono': instance.telefono,
            'celular': instance.celular,
            'direccion': instance.direccion,  
            'ciudad_id': instance.ciudad_id,
            'ciudad_nombre': instance.ciudad.nombre,
            'departamento_nombre': instance.ciudad.estado.nombre,
            'barrio': instance.barrio,
            'codigo_postal': instance.codigo_postal,
            'tipo_persona_id': instance.tipo_persona_id,
            'tipo_persona': instance.tipo_persona.nombre,
            'regimen_id': instance.regimen_id,
            'regimen_nombre': instance.regimen.nombre,  
            'codigo_ciuu': instance.codigo_ciuu,
            'asesor_id': instance.asesor_id,
            'asesor_nombre_corto': asesor_nombre_corto,
            'precio_id': instance.precio_id,
            'precio_nombre': precio_nombre,
            'plazo_pago_id': instance.plazo_pago_id,
            'plazo_pago_nombre': plazo_pago_nombre,
            'plazo_pago_dias': plazo_pago_dias,
            'plazo_pago_proveedor_id': instance.plazo_pago_proveedor_id,
            'plazo_pago_proveedor_nombre': plazo_pago_proveedor_nombre,
            'plazo_pago_proveedor_dias': plazo_pago_proveedor_dias,
            'cliente': instance.cliente,
            'proveedor': instance.proveedor,
            'empleado': instance.empleado
        }     

class ContactoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    ciudad = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())    
    tipo_persona = serializers.PrimaryKeyRelatedField(queryset=TipoPersona.objects.all())
    regimen = serializers.PrimaryKeyRelatedField(queryset=Regimen.objects.all())
    class Meta:
        model = Contacto 
        
    def to_representation(self, instance):
        plazo_pago = instance.plazo_pago
        plazo_pago_dias = 0
        if plazo_pago:
            plazo_pago_dias = plazo_pago.dias
        plazo_pago_proveedor = instance.plazo_pago_proveedor
        plazo_pago_proveedor_dias = 0
        if plazo_pago_proveedor:
            plazo_pago_proveedor_dias = plazo_pago_proveedor.dias
        return {
            'contacto_id': instance.id,            
            'contacto_nombre_corto': instance.nombre_corto,
            'plazo_pago_id': instance.plazo_pago_id,
            'plazo_pago_dias': plazo_pago_dias,
            'plazo_pago_proveedor_id': instance.plazo_pago_proveedor_id,
            'plazo_pago_proveedor_dias': plazo_pago_proveedor_dias
        }       

class ContactoListaBuscarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contacto 
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'numero_identificacion': instance.numero_identificacion,
            'nombre_corto': instance.nombre_corto            
        }
    
class ContactoExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contacto
        fields = [
            'id',
            'identificacion', 
            'numero_identificacion',
            'digito_verificacion',
            'nombre_corto',
            'nombre1',
            'nombre2',
            'apellido1',
            'apellido2',
            'direccion',
            'ciudad',
            'barrio',
            'codigo_postal',
            'telefono',
            'celular',
            'correo',
            'tipo_persona',
            'regimen',            
            'codigo_ciuu',
            'asesor',
            'precio',
            'plazo_pago']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'numero_identificacion': instance.numero_identificacion,
            'digito_verificacion': instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'nombre1': instance.nombre1,
            'nombre2': instance.nombre2,
            'apellido1': instance.apellido1,
            'apellido2': instance.apellido2,
            'direccion': instance.direccion,  
            'ciudad_nombre': instance.ciudad.nombre if instance.ciudad else None,
            'barrio': instance.barrio,
            'codigo_postal': instance.codigo_postal,
            'telefono': instance.telefono,
            'celular': instance.celular,
            'correo': instance.correo,
            'tipo_persona__nombre': instance.tipo_persona.nombre if instance.tipo_persona else None,
            'regimen_nombre': instance.regimen.nombre if instance.regimen else None,
            'codigo_ciuu': instance.codigo_ciuu,
            'asesor__nombre': instance.asesor.nombre_corto if instance.asesor else None,
            'precio': instance.precio.nombre if instance.precio else None,
            'plazo_pago': instance.plazo_pago.nombre if instance.plazo_pago else None,
            'cliente': instance.cliente,
            'proveedor': instance.proveedor
        } 