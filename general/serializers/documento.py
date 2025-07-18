from rest_framework import serializers
from django.db import models
from general.models.documento import GenDocumento
from general.models.documento_tipo import GenDocumentoTipo
from general.models.contacto import GenContacto
from general.models.metodo_pago import GenMetodoPago
from general.models.empresa import GenEmpresa
from general.models.plazo_pago import GenPlazoPago
from general.models.forma_pago import GenFormaPago
from general.models.asesor import GenAsesor
from general.models.resolucion import GenResolucion
from general.models.sede import GenSede
from general.models.cuenta_banco import GenCuentaBanco
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.contrato import HumContrato
from humano.models.grupo import HumGrupo
from humano.models.periodo import HumPeriodo
from humano.models.aporte import HumAporte
from humano.models.liquidacion import HumLiquidacion
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
    liquidacion = serializers.PrimaryKeyRelatedField(queryset=HumLiquidacion.objects.all(), default=None, allow_null=True)
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
        fields = ['id', 'numero', 'fecha', 'fecha_contable', 'fecha_vence', 'fecha_desde', 'fecha_hasta', 
                  'descuento', 'subtotal', 'impuesto', 'impuesto_retencion', 'impuesto_operado', 'total_bruto', 'total', 
                  'afectado', 'pendiente', 'contacto', 'documento_tipo', 'metodo_pago', 'forma_pago', 'empresa', 'base_impuesto', 
                  'estado_aprobado', 'estado_anulado', 'estado_contabilizado', 'comentario', 'soporte', 'orden_compra', 'remision',  
                  'estado_electronico_enviado', 'estado_electronico', 'estado_electronico_notificado', 'estado_electronico_evento',
                  'estado_electronico_descartado',
                  'documento_referencia', 'plazo_pago', 'cue', 'asesor', 'sede', 'usuario', 'programacion_detalle', 'aporte', 'liquidacion',
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

class GenDocumentoDetalleNominaSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    
    class Meta:
        model = GenDocumento
        fields = [
                    'id', 
                    'documento_tipo__nombre',
                    'numero', 
                    'fecha',
                    'soporte',
                    'contacto_id',                  
                    'contacto__numero_identificacion',
                    'contacto__nombre_corto',                                     
                    'devengado',
                    'deduccion',
                    'base_cotizacion',
                    'base_prestacion',
                    'subtotal',
                    'impuesto',
                    'total',
                    'cue',
                    'estado_aprobado',
                    'estado_anulado',
                    'estado_electronico_enviado',
                    'estado_electronico',
                    'estado_electronico_evento',
                    'estado_contabilizado'
                ]
        select_related_fields = ['contacto','documento_tipo']

class GenDocumentoDetalleCierreSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    grupo_contabilidad__nombre = serializers.CharField(source='grupo_contabilidad.nombre', read_only=True, allow_null=True, default=None)
    
    class Meta:
        model = GenDocumento
        fields = [
                    'id',                     
                    'numero', 
                    'fecha',
                    'contacto_id',                  
                    'contacto__numero_identificacion',
                    'contacto__nombre_corto',                                     
                    'comentario',
                    'estado_aprobado',
                    'estado_anulado',
                    'grupo_contabilidad'
                    'grupo_contabilidad__nombre'                    
                ]
        select_related_fields = ['contacto', 'grupo', 'grupo_contabilidad']

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
                  'soporte',
                  'contacto_id',                  
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

class GenDocumentoListaVentaSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    
    class Meta:
        model = GenDocumento
        fields = ['id', 
                  'documento_tipo__nombre',
                  'numero', 
                  'fecha',
                  'soporte',
                  'orden_compra',
                  'contacto_id',                  
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

class GenDocumentoListaNominaSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    
    class Meta:
        model = GenDocumento
        fields = ['id', 
                  'documento_tipo__nombre',
                  'numero', 
                  'fecha',
                  'fecha_desde',
                  'fecha_hasta',                  
                  'contacto_id',
                  'contacto__numero_identificacion',
                  'contacto__nombre_corto', 
                  'contrato_id',                                    
                  'salario',
                  'base_cotizacion',
                  'base_prestacion',
                  'devengado',
                  'deduccion',
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

class GenDocumentoInformeCuentaCobrarSerializador(serializers.ModelSerializer):  
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    
    class Meta:
        model = GenDocumento
        fields = ['id',
                  'numero',
                  'fecha',
                  'fecha_vence',                                    
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
                  'estado_electronico'
        ]
        select_related_fields = ['contacto','documento_tipo']

class GenDocumentoSeleccionarSerializador(serializers.ModelSerializer):
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)  
    class Meta:
        model = GenDocumento
        fields = ['id',
                  'numero',
                  'fecha',
                  'fecha_vence',                                    
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
        ]
        select_related_fields = ['contacto','documento_tipo']

class GenDocumentoAdicionarSerializador(serializers.ModelSerializer):
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)
    documento_tipo__cuenta_cobrar_id = serializers.CharField(source='documento_tipo.cuenta_cobrar_id', read_only=True)
    documento_tipo__cuenta_pagar_id = serializers.CharField(source='documento_tipo.cuenta_pagar_id', read_only=True)
    documento_tipo__operacion = serializers.IntegerField(source='documento_tipo.operacion', read_only=True)
    documento_tipo__cuenta_pagar__codigo = serializers.CharField(source='documento_tipo.cuenta_pagar.codigo', read_only=True)
    documento_tipo__cuenta_cobrar__codigo = serializers.CharField(source='documento_tipo.cuenta_cobrar.codigo', read_only=True)
    cuenta__codigo = serializers.CharField(source='cuenta.codigo', read_only=True)
    class Meta:
        model = GenDocumento
        fields = [
            'id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 
            'impuesto_retencion', 'impuesto_operado', 'total_bruto', 'total', 'afectado', 
            'estado_aprobado', 'estado_contabilizado', 'contacto', 'documento_tipo', 
            'metodo_pago', 'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 
            'soporte', 'forma_pago', 'estado_electronico_enviado', 'estado_electronico_notificado', 
            'estado_electronico_evento', 'orden_compra', 'remision', 'documento_referencia', 
            'plazo_pago', 'cue', 'referencia_cue', 'referencia_numero', 'referencia_prefijo', 
            'almacen', 'resolucion', 'contacto__nombre_corto', 'documento_tipo__nombre',
            'documento_tipo__cuenta_pagar__codigo', 'documento_tipo__cuenta_cobrar__codigo',
            'documento_tipo__cuenta_cobrar_id', 'documento_tipo__cuenta_pagar_id', 'documento_tipo__operacion', 'fecha_contable', 'pendiente', 'cuenta', 'cuenta__codigo'
        ]
        select_related_fields = [
            'contacto',
            'documento_tipo',
            'documento_tipo__cuenta_cobrar',
            'documento_tipo__cuenta_pagar',
            'metodo_pago',
            'plazo_pago',
            'resolucion',
            'cuenta'
        ]  

class GenDocumentoEventoCompraSerializador(serializers.ModelSerializer):        
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    class Meta:
        model = GenDocumento
        fields = [
            'id', 'numero', 'fecha', 'fecha_vence', 'soporte', 'orden_compra', 'cue',
            'referencia_cue', 'referencia_numero', 'referencia_prefijo', 'total',
            'estado_electronico', 'estado_electronico_enviado', 'estado_electronico_evento',
            'estado_aprobado', 'estado_anulado', 'evento_documento', 'evento_recepcion',
            'evento_aceptacion', 'contacto', 'contacto__numero_identificacion',
            'contacto__nombre_corto'
        ]
        select_related_fields = ['contacto']

class GenDocumentoNominaSerializador(serializers.ModelSerializer):    
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    class Meta:
        model = GenDocumento
        fields = [
            'id', 'documento_tipo', 'numero', 'fecha', 'fecha_hasta', 'contacto', 'contacto__numero_identificacion', 'contacto__nombre_corto',
            'salario', 'devengado', 'deduccion', 'total', 'base_cotizacion', 'base_prestacion', 'contrato_id', 'estado_aprobado',
            'estado_anulado', 'estado_electronico', 'estado_contabilizado', 'cue'
        ]
        select_related_fields = ['contacto']

class GenDocumentoNominaExcelSerializador(serializers.ModelSerializer):    
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    contacto__numero_cuenta = serializers.CharField(source='contacto.numero_cuenta', read_only=True)
    contacto__banco__nombre = serializers.CharField(source='contacto.banco.nombre', read_only=True)
    contrato__grupo__nombre = serializers.CharField(source='contrato.grupo.nombre', read_only=True)
    class Meta:
        model = GenDocumento
        fields = [
            'id', 'numero', 'fecha', 'fecha_hasta', 'contacto', 'contacto__numero_identificacion', 'contacto__nombre_corto', 'contacto__numero_cuenta', 'contacto__banco__nombre',
            'contrato_id', 'contrato__grupo__nombre' ,'dias', 'salario', 'devengado', 'deduccion', 'total', 'base_cotizacion', 'base_prestacion',
            'estado_anulado', 'estado_electronico', 'estado_contabilizado', 'cue'
        ]
        select_related_fields = ['contacto', 'contacto__banco', 'contrato', 'contrato__grupo']  

class GenDocumentoNominaElectronicaExcelSerializador(serializers.ModelSerializer):    
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True)
    contacto__numero_cuenta = serializers.CharField(source='contacto.numero_cuenta', read_only=True)
    contacto__banco__nombre = serializers.CharField(source='contacto.banco.nombre', read_only=True)
    contrato__grupo__nombre = serializers.CharField(source='contrato.grupo.nombre', read_only=True)
    class Meta:
        model = GenDocumento
        fields = [
            'id', 'numero', 'fecha', 'fecha_hasta', 'contacto', 'contacto__numero_identificacion', 'contacto__nombre_corto', 'contacto__numero_cuenta', 'contacto__banco__nombre',
            'contrato_id', 'contrato__grupo__nombre' ,'dias', 'salario', 'devengado', 'deduccion', 'total', 'base_cotizacion', 'base_prestacion',
            'estado_anulado', 'estado_electronico', 'estado_contabilizado', 'cue'
        ]
        select_related_fields = ['contacto', 'contacto__banco', 'contrato', 'contrato__grupo']  
        
class GenDocumentoReferenciaSerializador(serializers.ModelSerializer):    
    documento_tipo__nombre = serializers.CharField(source='documento_tipo.nombre', read_only=True)
    class Meta:
        model = GenDocumento
        fields = ['id', 'numero', 'fecha', 'documento_tipo__nombre'] 
        select_related_fields = ['documento_tipo']


#deprecated

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
 
    

       

    
