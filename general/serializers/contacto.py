from general.models.contacto import GenContacto, GenCiudad, GenIdentificacion, GenRegimen, GenTipoPersona, GenAsesor, GenPrecio, GenPlazoPago, GenBanco, GenCuentaBancoClase
from transporte.models.categoria_licencia import TteCategoriaLicencia
from rest_framework import serializers

class GenContactoSerializador(serializers.HyperlinkedModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=GenIdentificacion.objects.all())
    ciudad = serializers.PrimaryKeyRelatedField(queryset=GenCiudad.objects.all())    
    tipo_persona = serializers.PrimaryKeyRelatedField(queryset=GenTipoPersona.objects.all())
    regimen = serializers.PrimaryKeyRelatedField(queryset=GenRegimen.objects.all())
    asesor = serializers.PrimaryKeyRelatedField(queryset=GenAsesor.objects.all(), allow_null=True, required=False)
    precio = serializers.PrimaryKeyRelatedField(queryset=GenPrecio.objects.all(), allow_null=True, required=False)
    plazo_pago = serializers.PrimaryKeyRelatedField(queryset=GenPlazoPago.objects.all(), allow_null=True, required=False)
    plazo_pago_proveedor = serializers.PrimaryKeyRelatedField(queryset=GenPlazoPago.objects.all(), allow_null=True, required=False)
    banco = serializers.PrimaryKeyRelatedField(queryset=GenBanco.objects.all(), allow_null=True, required=False)
    cuenta_banco_clase = serializers.PrimaryKeyRelatedField(queryset=GenCuentaBancoClase.objects.all(), allow_null=True, required=False)
    cuenta_banco_clase = serializers.PrimaryKeyRelatedField(queryset=GenCuentaBancoClase.objects.all(), allow_null=True, required=False)
    categoria_licencia = serializers.PrimaryKeyRelatedField(queryset=TteCategoriaLicencia.objects.all(), allow_null=True, required=False)
    class Meta:
        model = GenContacto
        fields = [
            'id', 'identificacion', 'numero_identificacion', 'digito_verificacion', 'nombre_corto', 'nombre1', 'nombre2', 'apellido1', 'apellido2',
            'direccion', 'ciudad', 'barrio', 'codigo_postal', 'telefono', 'celular', 'correo', 'correo_facturacion_electronica', 'tipo_persona', 'regimen', 'codigo_ciuu',
            'asesor', 'precio', 'plazo_pago', 'plazo_pago_proveedor', 'cliente', 'proveedor', 'empleado', 'conductor' ,'banco', 'numero_cuenta', 'cuenta_banco_clase', 'numero_licencia',
            'categoria_licencia', 'fecha_vence_licencia']  
        
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
        banco_nombre = ""
        if instance.banco:
            banco_nombre = instance.banco.nombre
        cuenta_banco_clase_nombre =""
        if instance.cuenta_banco_clase:
            cuenta_banco_clase_nombre = instance.cuenta_banco_clase.nombre
        categoria_licencia_nombre =""
        if instance.categoria_licencia:
            categoria_licencia_nombre = instance.categoria_licencia.nombre
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
            'correo_facturacion_electronica': instance.correo_facturacion_electronica,
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
            'numero_cuenta': instance.numero_cuenta,
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
            'empleado': instance.empleado,
            'conductor': instance.conductor,
            'banco_id': instance.banco_id,
            'banco_nombre': banco_nombre,
            'cuenta_banco_clase_id': instance.cuenta_banco_clase_id,
            'cuenta_banco_clase_nombre': cuenta_banco_clase_nombre, 
            'numero_licencia': instance.numero_licencia,
            'categoria_licencia_id': instance.categoria_licencia_id,
            'categoria_licencia_nombre': categoria_licencia_nombre, 
            'fecha_vence_licencia': instance.fecha_vence_licencia
        }     

class GenContactoListaSerializador(serializers.ModelSerializer):      
    identificacion__abreviatura = serializers.CharField(source='identificacion.abreviatura', read_only=True)
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True)
    categoria_licencia__nombre = serializers.CharField(source='categoria_licencia.nombre', read_only=True)
    class Meta:
        model = GenContacto
        fields = ['id', 
                  'identificacion__abreviatura',
                  'numero_identificacion', 
                  'nombre_corto',
                  'correo',
                  'telefono',                                     
                  'celular',
                  'direccion',
                  'ciudad__nombre',
                  'cliente',
                  'proveedor',
                  'empleado',
                  'conductor',
                  'numero_licencia',
                  'categoria_licencia',
                  'categoria_licencia__nombre',
                  'fecha_vence_licencia']
        select_related_fields = ['identificacion', 'ciudad', 'categoria_licencia']

class GenContactoDetalleSerializador(serializers.ModelSerializer):      
    identificacion__abreviatura = serializers.CharField(source='identificacion.abreviatura', read_only=True)
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True)
    categoria_licencia__nombre = serializers.CharField(source='categoria_licencia.nombre', read_only=True)
    class Meta:
        model = GenContacto
        fields = ['id', 
                  'identificacion__abreviatura',
                  'numero_identificacion', 
                  'nombre_corto',
                  'correo',
                  'telefono',                                     
                  'celular',
                  'direccion',
                  'ciudad__nombre',
                  'cliente',
                  'proveedor',
                  'empleado',
                  'conductor',
                  'numero_licencia',
                  'categoria_licencia',
                  'categoria_licencia__nombre',
                  'fecha_vence_licencia']
        select_related_fields = ['identificacion', 'ciudad', 'categoria_licencia']

class GenContactoSeleccionarSerializador(serializers.ModelSerializer):
    plazo_pago__dias = serializers.IntegerField(source='plazo_pago.dias', read_only=True)
    plazo_pago_proveedor__dias = serializers.IntegerField(source='plazo_pago_proveedor.dias', read_only=True)
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True)
    class Meta: 
        model = GenContacto
        fields = ['id', 'nombre_corto', 'numero_identificacion', 'direccion', 'correo', 'ciudad', 'celular' ,'plazo_pago_id', 'plazo_pago_proveedor_id' ,'plazo_pago__dias', 'plazo_pago_proveedor__dias', 'ciudad__nombre']
        select_related_fields = ['plazo_pago', 'plazo_pago_proveedor', 'ciudad']