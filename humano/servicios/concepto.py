from general.models.configuracion import GenConfiguracion
from humano.models.liquidacion import HumLiquidacion
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from datetime import timedelta


class ConceptoServicio():

    @staticmethod
    def datos_documento_detalle(data_general, data, concepto):        
        data['operacion'] = concepto.operacion
        data['pago_operado'] = data['pago'] * concepto.operacion
        if concepto.operacion == 1:
            data['devengado'] = data['pago']
            data_general['devengado'] += data['pago']
        if concepto.operacion == -1:
            data['deduccion'] = data['pago']   
            data_general['deduccion'] += data['pago']     
        if concepto.ingreso_base_cotizacion:
            if concepto.id == 28:
                base =  round(data['cantidad'] * data['hora'])
                data['base_cotizacion'] = base
                data_general['base_cotizacion'] += base
                data_general['base_licencia'] += base
            else:
                data['base_cotizacion'] = data['pago']
                data_general['base_cotizacion'] += data['pago']
        if concepto.ingreso_base_prestacion:
            data['base_prestacion'] = data['pago']
            data_general['base_prestacion'] += data['pago']
        if concepto.ingreso_base_prestacion_vacacion:        
            data['base_prestacion_vacacion'] = data['pago']
            data_general['base_prestacion_vacacion'] += data['pago']        
        return data             