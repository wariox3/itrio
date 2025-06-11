from rest_framework import serializers
from django.db import models
from general.models.documento import GenDocumento
from general.models.documento_tipo import GenDocumentoTipo
from general.models.contacto import GenContacto
from general.models.metodo_pago import GenMetodoPago
from general.models.empresa import GenEmpresa
from general.models.plazo_pago import GenPlazoPago
from general.models.forma_pago import GenFormaPago
from general.models.gen_asesor import GenAsesor
from general.models.resolucion import GenResolucion
from general.models.sede import GenSede
from general.models.cuenta_banco import GenCuentaBanco
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.contrato import HumContrato
from humano.models.grupo import HumGrupo
from humano.models.periodo import HumPeriodo
from humano.models.aporte import HumAporte
from contabilidad.models.comprobante import ConComprobante
from contabilidad.models.grupo import ConGrupo
from contabilidad.models.cuenta import ConCuenta
from inventario.models.almacen import InvAlmacen
from seguridad.models import User

class GenDocumentoSerializador(serializers.HyperlinkedModelSerializer):        
    numero = serializers.IntegerField(allow_null=True, default=None)
    fecha = serializers.DateField()
    fecha_vence = serializers.DateField(allow_null=True, default=None)
    fecha_contable = serializers.DateField(allow_null=True, default=None)
    fecha_hasta = serializers.DateField(allow_null=True, default=None)
    estado_aprobado = serializers.BooleanField(default = False, label='APR')    
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), default=None, allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=GenDocumentoTipo.objects.all())    
    metodo_pago = serializers.PrimaryKeyRelatedField(queryset=GenMetodoPago.objects.all(), default=None, allow_null=True)
    empresa = serializers.PrimaryKeyRelatedField(queryset=GenEmpresa.objects.all(), default=1)    
    documento_referencia = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), default=None, allow_null=True)    
    plazo_pago = serializers.PrimaryKeyRelatedField(queryset=GenPlazoPago.objects.all(), default=None, allow_null=True)
    forma_pago = serializers.PrimaryKeyRelatedField(queryset=GenFormaPago.objects.all(), default=None, allow_null=True)
    asesor = serializers.PrimaryKeyRelatedField(queryset=GenAsesor.objects.all(), default=None, allow_null=True)
    sede = serializers.PrimaryKeyRelatedField(queryset=GenSede.objects.all(), default=None, allow_null=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None, allow_null=True)
    programacion_detalle = serializers.PrimaryKeyRelatedField(queryset=HumProgramacionDetalle.objects.all(), default=None, allow_null=True)
    aporte = serializers.PrimaryKeyRelatedField(queryset=HumAporte.objects.all(), default=None, allow_null=True)
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all(), default=None, allow_null=True)
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all(), default=None, allow_null=True)
    periodo = serializers.PrimaryKeyRelatedField(queryset=HumPeriodo.objects.all(), default=None, allow_null=True)
    cuenta_banco = serializers.PrimaryKeyRelatedField(queryset=GenCuentaBanco.objects.all(), default=None, allow_null=True)
    comprobante = serializers.PrimaryKeyRelatedField(queryset=ConComprobante.objects.all(), default=None, allow_null=True)
    grupo_contabilidad = serializers.PrimaryKeyRelatedField(queryset=ConGrupo.objects.all(), default=None, allow_null=True)
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    almacen = serializers.PrimaryKeyRelatedField(queryset=InvAlmacen.objects.all(), default=None, allow_null=True)

    class Meta:
        model = GenDocumento
        fields = ['id', 'numero', 'fecha', 'fecha_contable', 'fecha_vence', 'fecha_hasta', 
                  'descuento', 'subtotal', 'impuesto', 'impuesto_retencion', 'impuesto_operado', 'total_bruto', 'total', 
                  'afectado', 'pendiente', 'contacto', 'documento_tipo', 'metodo_pago', 'forma_pago', 'empresa', 'base_impuesto', 
                  'estado_aprobado', 'estado_anulado', 'estado_contabilizado', 'comentario', 'soporte', 'orden_compra', 'remision',  
                  'estado_electronico_enviado', 'estado_electronico', 'estado_electronico_notificado', 'estado_electronico_evento',
                  'estado_electronico_descartado',
                  'documento_referencia', 'plazo_pago', 'cue', 'asesor', 'sede', 'usuario', 'programacion_detalle', 'aporte',
                  'grupo', 'contrato', 'salario', 'devengado', 'deduccion', 'base_cotizacion', 'base_prestacion', 'base_prestacion_vacacion', 
                  'provision_cesantia', 'provision_interes', 'provision_prima', 'provision_vacacion',
                  'periodo', 'cuenta_banco', 
                  'comprobante', 'grupo_contabilidad', 'cuenta', 'dias', 'referencia_cue', 'referencia_numero', 'referencia_prefijo', 'almacen', 
                  'evento_documento', 'evento_recepcion', 'evento_aceptacion']

    def to_representation(self, instance):        
        contacto_nombre_corto = ""
        contacto_numero_identificacion = ""
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
            contacto_numero_identificacion = instance.contacto.numero_identificacion
        asesor_nombre_corto = ""
        if instance.asesor:
            asesor_nombre_corto = instance.asesor.nombre_corto    
        sede_nombre = ""
        if instance.sede:
            sede_nombre = instance.sede.nombre    
        cuenta_banco_nombre = ""
        if instance.cuenta_banco:
            cuenta_banco_nombre = instance.cuenta_banco.nombre  
        comprobante_nombre = ""
        if instance.comprobante:
            comprobante_nombre = instance.comprobante.nombre       
        grupo_contabilidad_nombre = ""
        if instance.grupo_contabilidad:
            grupo_contabilidad_nombre = instance.grupo_contabilidad.nombre   
        documento_tipo_nombre = ""
        if instance.documento_tipo:
            documento_tipo_nombre = instance.documento_tipo.nombre
        forma_pago_nombre = ""
        if instance.forma_pago:
            forma_pago_nombre = instance.forma_pago.nombre
        almacen_nombre = ""
        if instance.almacen:
            almacen_nombre = instance.almacen.nombre
        cuenta_nombre = ""
        cuenta_codigo = ""
        if instance.cuenta:
            cuenta_nombre = instance.cuenta.nombre
            cuenta_codigo = instance.cuenta.codigo
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha': instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'fecha_contable' : instance.fecha_contable,
            'fecha_hasta' : instance.fecha_hasta,
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,           
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'impuesto_retencion': instance.impuesto_retencion,
            'impuesto_operado': instance.impuesto_operado,
            'total_bruto' :  instance.total_bruto,
            'total' :  instance.total,
            'afectado' :  instance.afectado,
            'pendiente': instance.pendiente,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'base_cotizacion': instance.base_cotizacion,            
            'base_prestacion': instance.base_prestacion,
            'base_prestacion_vacacion': instance.base_prestacion_vacacion,
            'salario': instance.salario,            
            'contacto_id': instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto': contacto_nombre_corto,
            'documento_tipo_id': instance.documento_tipo_id,
            'documento_tipo_nombre': documento_tipo_nombre,
            'metodo_pago': instance.metodo_pago_id,        
            'estado_aprobado': instance.estado_aprobado,           
            'estado_contabilizado': instance.estado_contabilizado,
            'estado_anulado' : instance.estado_anulado,            
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'estado_electronico_evento' : instance.estado_electronico_evento,
            'estado_electronico_descartado' : instance.estado_electronico_descartado,
            'comentario' : instance.comentario,
            'soporte' : instance.soporte,
            'orden_compra' : instance.orden_compra,
            'remision' : instance.remision,
            'cue' : instance.cue,
            'referencia_cue' : instance.referencia_cue,
            'referencia_numero' : instance.referencia_numero,
            'referencia_prefijo' : instance.referencia_prefijo,
            'empresa': instance.empresa_id,            
            'resolucion': instance.resolucion_id,
            'documento_referencia' :  instance.documento_referencia_id,
            'plazo_pago': instance.plazo_pago_id,
            'asesor_id': instance.asesor_id,
            'asesor_nombre_corto': asesor_nombre_corto,
            'sede_id': instance.sede_id,
            'sede_nombre': sede_nombre,
            'programacion_detalle_id': instance.programacion_detalle_id,
            'contrato_id': instance.contrato_id,
            'cuenta_banco_id': instance.cuenta_banco_id,
            'cuenta_banco_nombre': cuenta_banco_nombre,
            'comprobante_id': instance.comprobante_id,
            'comprobante_nombre': comprobante_nombre,
            'grupo_contabilidad_id': instance.grupo_contabilidad_id,
            'grupo_contabilidad_nombre': grupo_contabilidad_nombre,
            'forma_pago_id': instance.forma_pago_id,
            'forma_pago_nombre': forma_pago_nombre,
            'almacen_id': instance.almacen_id,
            'almacen_nombre': almacen_nombre,
            'evento_documento': instance.evento_documento,
            'evento_recepcion': instance.evento_documento,
            'evento_aceptacion': instance.evento_aceptacion,
            'cuenta_id':instance.cuenta_id,
            'provision_cesantia': instance.provision_cesantia,
            'provision_interes': instance.provision_interes,
            'provision_prima': instance.provision_prima,
            'provision_vacacion': instance.provision_vacacion,
            'cuenta_id': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,
            'cuenta_nombre': cuenta_nombre
        }
    
class GenDocumentoListaSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    
    class Meta:
        model = GenDocumento
        fields = ['id', 
                  'documento_tipo__nombre',
                  'numero', 
                  'fecha',
                  'contacto__numero_identificacion',
                  'contacto__nombre_corto',                                     
                  'subtotal',
                  'impuesto',
                  'total',
                  'estado_aprobado',
                  'estado_anulado',
                  'estado_electronico',
                  'estado_electronico_evento',
                  'estado_contabilizado']
        select_related_fields = ['contacto','documento_tipo']

class GenDocumentoInformeSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    
    class Meta:
        model = GenDocumento
        fields = ['id',
                  'fecha',
                  'fecha_vence',
                  'fecha_contable',
                  'numero',
                  'documento_referencia',
                  'documento_tipo_id',
                  'documento_tipo__nombre',
                  'contacto_id',
                  'contacto__numero_identificacion',
                  'contacto__nombre_corto',
                  'descuento',       
                  'subtotal',  
                  'base_impuesto',              
                  'impuesto',
                  'total',
                  'afectado',
                  'pendiente',           
                  'soporte',
                  'orden_compra',
                  'cue',
                  'resolucion',
                  'estado_aprobado',
                  'estado_anulado',
                  'estado_electronico',
                  'estado_electronico_enviado',
                  'estado_electronico_notificado',
        ]
        select_related_fields = ['contacto','documento_tipo']


#Deprecated 

class GenDocumentoRetrieveSerializador(serializers.HyperlinkedModelSerializer):        
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=GenDocumentoTipo.objects.all())    
    documento_referencia = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), allow_null=True)    
    plazo_pago = serializers.PrimaryKeyRelatedField(queryset=GenPlazoPago.objects.all(), allow_null=True)
    forma_pago = serializers.PrimaryKeyRelatedField(queryset=GenFormaPago.objects.all(), allow_null=True)    
    almacen = serializers.PrimaryKeyRelatedField(queryset=InvAlmacen.objects.all(), allow_null=True)    
    resolucion = serializers.PrimaryKeyRelatedField(queryset=GenResolucion.objects.all(), allow_null=True)   
    class Meta:
        model = GenDocumento
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'impuesto_retencion', 'impuesto_operado', 
                  'total_bruto', 'total', 'afectado', 'estado_aprobado', 'estado_contabilizado', 'contacto', 'documento_tipo', 'metodo_pago', 
                  'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 'soporte', 'forma_pago'
                  'estado_electronico_enviado', 'estado_electronico_notificado', 'estado_electronico_evento', 'orden_compra', 'remision', 
                  'documento_referencia', 'plazo_pago', 'cue', 'referencia_cue', 'referencia_numero', 'referencia_prefijo', 'almacen', 'resolucion']

    def to_representation(self, instance):
        contacto_numero_identificacion = ""
        contacto_nombre_corto = ""
        if instance.contacto:
            contacto_numero_identificacion = instance.contacto.numero_identificacion
            contacto_nombre_corto = instance.contacto.nombre_corto
        metodo_pago = instance.metodo_pago
        metodo_pago_nombre = ""
        if metodo_pago is not None:
            metodo_pago_nombre = metodo_pago.nombre            
        plazo_pago = instance.plazo_pago
        plazo_pago_nombre = ""
        if plazo_pago is not None:
            plazo_pago_nombre = plazo_pago.nombre       
        documento_referencia = instance.documento_referencia
        documento_referencia_numero = ""
        if documento_referencia is not None:
            documento_referencia_numero = documento_referencia.numero     
        asesor = instance.asesor
        asesor_nombre_corto = None
        if asesor:
            asesor_nombre_corto = asesor.nombre_corto
        sede = instance.sede
        sede_nombre = None
        if sede:
            sede_nombre = sede.nombre 
        cuenta_banco_nombre = ""
        if instance.cuenta_banco:
            cuenta_banco_nombre = instance.cuenta_banco.nombre        
        comprobante_nombre = ""
        if instance.comprobante:
            comprobante_nombre = instance.comprobante.nombre   
        grupo_contabilidad_nombre = ""
        if instance.grupo_contabilidad:
            grupo_contabilidad_nombre = instance.grupo_contabilidad.nombre   
        forma_pago_nombre = ""
        if instance.forma_pago:
            forma_pago_nombre = instance.forma_pago.nombre    
        almacen_nombre = ""
        if instance.almacen:
            almacen_nombre = instance.almacen.nombre          
        resolucion_numero = ""
        if instance.resolucion:
            resolucion_numero = instance.resolucion.numero
        cuenta_nombre = ""
        cuenta_codigo = ""
        if instance.cuenta:
            cuenta_nombre = instance.cuenta.nombre
            cuenta_codigo = instance.cuenta.codigo              
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence, 
            'fecha_hasta' : instance.fecha_hasta, 
            'contacto_id' : instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto' : contacto_nombre_corto,            
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,
            'subtotal': instance.subtotal,  
            'afectado': instance.afectado,
            'pendiente': instance.pendiente,
            'impuesto': instance.impuesto,
            'impuesto_retencion': instance.impuesto_retencion,
            'impuesto_operado': instance.impuesto_operado,
            'total_bruto' :  instance.total_bruto,   
            'total' :  instance.total,   
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'base_cotizacion': instance.base_cotizacion,            
            'base_prestacion': instance.base_prestacion,
            'salario': instance.salario,     
            'estado_aprobado' : instance.estado_aprobado,
            'documento_tipo_id' : instance.documento_tipo_id,
            'metodo_pago_id' : instance.metodo_pago_id,
            'metodo_pago_nombre' : metodo_pago_nombre,
            'estado_anulado' :instance.estado_anulado,
            'estado_contabilizado' :instance.estado_contabilizado,
            'comentario': instance.comentario,
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'estado_electronico_evento' : instance.estado_electronico_evento,
            'soporte' : instance.soporte,
            'orden_compra': instance.orden_compra,
            'remision': instance.remision,
            'plazo_pago_id': instance.plazo_pago_id,
            'plazo_pago_nombre': plazo_pago_nombre,
            'documento_referencia_id': instance.documento_referencia_id,
            'documento_referencia_numero': documento_referencia_numero,
            'cue' : instance.cue,
            'referencia_cue' : instance.referencia_cue,
            'referencia_numero' : instance.referencia_numero,
            'referencia_prefijo' : instance.referencia_prefijo,            
            'electronico_id': instance.electronico_id,
            'asesor': instance.asesor_id,
            'asesor_nombre_corto': asesor_nombre_corto,
            'sede': instance.sede_id,
            'sede_nombre': sede_nombre,
            'programacion_detalle_id': instance.programacion_detalle_id,
            'contrato_id': instance.contrato_id,
            'cuenta_banco_id': instance.cuenta_banco_id,
            'cuenta_banco_nombre': cuenta_banco_nombre,
            'comprobante_id': instance.comprobante_id,
            'comprobante_nombre': comprobante_nombre,
            'grupo_contabilidad_id': instance.grupo_contabilidad_id,
            'grupo_contabilidad_nombre': grupo_contabilidad_nombre,
            'forma_pago_id': instance.forma_pago_id,
            'forma_pago_nombre': forma_pago_nombre,
            'almacen_id': instance.almacen_id,
            'almacen_nombre': almacen_nombre,
            'resolucion_id' : instance.resolucion_id,
            'resolucion_numero' : resolucion_numero,
            'cuenta_id': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,
            'cuenta_nombre': cuenta_nombre                
        }

class GenDocumentoExcelSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = GenDocumento

    def to_representation(self, instance):        
        contacto = instance.contacto
        contacto_nombre_corto = None
        if contacto:
            contacto_nombre_corto = contacto.nombre_corto
        return {
            'id': instance.id,            
            'tipo': instance.documento_tipo_id,
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,            
            'metodo_pago': instance.metodo_pago_id,
            'orden_compra' : instance.orden_compra,
            'contacto_id': instance.contacto_id,
            'identificacion': instance.contacto.numero_identificacion if instance.contacto else None,
            'contacto': contacto_nombre_corto,
            'descuento': instance.descuento,            
            'subtotal': instance.subtotal,            
            'base_impuesto': instance.base_impuesto,           
            'impuesto': instance.impuesto,
            'total' :  instance.total,
            'afectado' :  instance.afectado,
            'pendiente' :  instance.pendiente,
            'aprobado' : instance.estado_aprobado,
            'anulado' : instance.estado_anulado,
            'electronico' : instance.estado_electronico,
            'ele_enviado' : instance.estado_electronico_enviado,
            'ele_notificado' : instance.estado_electronico_notificado,        
            'empresa': instance.empresa_id,
            'resolucion': instance.resolucion_id,
            'comentario' : instance.comentario,
            'evento_documento': instance.evento_documento,
            'evento_recepcion': instance.evento_documento,
            'evento_aceptacion': instance.evento_aceptacion,
        }    
    
class GenDocumentoReferenciaSerializador(serializers.HyperlinkedModelSerializer):    
    numero = serializers.IntegerField(allow_null=True, label='Numero')
    class Meta:
        model = GenDocumento
        fields = ['id', 'numero']

    def to_representation(self, instance):        
        return {
            'id': instance.id,            
            'numero' : instance.numero
        }   
    
class GenDocumentoAdicionarSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = GenDocumento        

    def to_representation(self, instance):        
        contacto = instance.contacto
        contacto_nombre_corto = None
        if contacto:
            contacto_nombre_corto = contacto.nombre_corto
        documento_tipo_nombre = ""
        documento_tipo_cuenta_cobrar_id = ""
        documento_tipo_cuenta_cobrar_cuenta_codigo = ""
        documento_tipo_cuenta_pagar_id = ""
        documento_tipo_cuenta_pagar_cuenta_codigo = ""   
        documento_tipo_operacion = 0              
        if instance.documento_tipo:
            documento_tipo_cuenta_cobrar_id = instance.documento_tipo.cuenta_cobrar_id
            cuenta_cobrar = instance.documento_tipo.cuenta_cobrar
            documento_tipo_nombre = instance.documento_tipo.nombre
            if cuenta_cobrar:
                documento_tipo_cuenta_cobrar_cuenta_codigo = cuenta_cobrar.codigo
            documento_tipo_cuenta_pagar_id = instance.documento_tipo.cuenta_pagar_id
            cuenta_pagar = instance.documento_tipo.cuenta_pagar
            if cuenta_pagar:
                documento_tipo_cuenta_pagar_cuenta_codigo = cuenta_pagar.codigo  
            documento_tipo_operacion = instance.documento_tipo.operacion              
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'fecha_contable' : instance.fecha_contable,
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,           
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total, 
            'afectado':instance.afectado,
            'pendiente':instance.pendiente,
            'estado_aprobado' : instance.estado_aprobado,
            'contacto' : instance.contacto_id,            
            'documento_tipo': instance.documento_tipo_id,      
            'documento_tipo_nombre': documento_tipo_nombre,  
            'documento_tipo_cuenta_cobrar_id': documento_tipo_cuenta_cobrar_id,
            'documento_tipo_cuenta_cobrar_cuenta_codigo':documento_tipo_cuenta_cobrar_cuenta_codigo,
            'documento_tipo_cuenta_pagar_id': documento_tipo_cuenta_pagar_id,
            'documento_tipo_cuenta_pagar_cuenta_codigo':documento_tipo_cuenta_pagar_cuenta_codigo,
            'documento_tipo_operacion': documento_tipo_operacion,
            'metodo_pago': instance.metodo_pago_id,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'estado_anulado' : instance.estado_anulado,
            'comentario' : instance.comentario,
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'soporte' : instance.soporte,
            'orden_compra' : instance.orden_compra,
            'cue' : instance.cue,
            'empresa': instance.empresa_id,
            'resolucion': instance.resolucion_id,
            'documento_referencia' :  instance.documento_referencia_id,
            'plazo_pago': instance.plazo_pago_id
        }    
    
class GenDocumentoNominaSerializador(serializers.HyperlinkedModelSerializer):    

    class Meta:
        model = GenDocumento
    
    def to_representation(self, instance):        
        contacto_nombre_corto = ""
        contacto_numero_identificacion = ""
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
            contacto_numero_identificacion = instance.contacto.numero_identificacion
        return {
            'id': instance.id,            
            'documento_tipo_id': instance.documento_tipo_id,
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_hasta' : instance.fecha_hasta,            
            'contacto_id': instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto': contacto_nombre_corto,            
            'salario': instance.salario,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'total':  instance.total,
            'base_cotizacion': instance.base_cotizacion,
            'base_prestacion': instance.base_prestacion,
            'contrato_id': instance.contrato_id,
            'estado_aprobado': instance.estado_aprobado,
            'estado_anulado': instance.estado_anulado,
            'estado_electronico': instance.estado_electronico,
            'estado_contabilizado': instance.estado_contabilizado,
            'cue': instance.cue
        } 

class GenDocumentoNominaExcelSerializador(serializers.HyperlinkedModelSerializer):    

    class Meta:
        model = GenDocumento
    
    def to_representation(self, instance):        
        contacto_nombre_corto = ""
        contacto_numero_identificacion = ""
        numero_cuenta = ""
        banco_nombre = ""        
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
            contacto_numero_identificacion = instance.contacto.numero_identificacion
            numero_cuenta = instance.contacto.numero_cuenta
            if instance.contacto.banco:
                banco_nombre = instance.contacto.banco.nombre
        grupo_nombre = ""
        if instance.contrato:
            if instance.contrato.grupo:
                grupo_nombre = instance.contrato.grupo.nombre         
        return {
            'ID': instance.id,            
            'NUMERO' : instance.numero,
            'DESDE' : instance.fecha,
            'HASTA' : instance.fecha_hasta,            
            'COD_EMP': instance.contacto_id,
            'IDENTIFICACION': contacto_numero_identificacion,
            'EMPLEADO': contacto_nombre_corto,            
            'CUENTA': numero_cuenta,
            'BANCO': banco_nombre,            
            'CONT': instance.contrato_id,
            'GRUPO': grupo_nombre,
            'DIAS': instance.dias,
            'SALARIO': instance.salario,
            'DEVENGADO': instance.devengado,
            'DEDUCCION': instance.deduccion,
            'TOTAL':  instance.total,
            'IBC': instance.base_cotizacion,
            'IBP': instance.base_prestacion,                    
        }    
    
class GenDocumentoEventoCompraSerializador(serializers.HyperlinkedModelSerializer):        

    class Meta:
        model = GenDocumento

    def to_representation(self, instance):        
        contacto_nombre_corto = ""
        contacto_numero_identificacion = ""
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
            contacto_numero_identificacion = instance.contacto.numero_identificacion                            
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,                
            'soporte' : instance.soporte,
            'orden_compra' : instance.orden_compra,
            'cue' : instance.cue,
            'referencia_cue' : instance.referencia_cue,
            'referencia_numero' : instance.referencia_numero,
            'referencia_prefijo' : instance.referencia_prefijo,            
            'total' :  instance.total,                        
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado': instance.estado_electronico_enviado,
            'estado_electronico_evento' : instance.estado_electronico_evento,
            'estado_aprobado' : instance.estado_aprobado,           
            'estado_anulado' : instance.estado_anulado,
            'evento_documento': instance.evento_documento,
            'evento_recepcion': instance.evento_recepcion,
            'evento_aceptacion': instance.evento_aceptacion,
            'contacto_id': instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto': contacto_nombre_corto
        }    
         