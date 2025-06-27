from openpyxl import Workbook
from openpyxl.styles import Font, NamedStyle
from django.utils.encoding import smart_str
from django.http import HttpResponse
from decimal import Decimal
from io import BytesIO

class ExcelExportar:
    HEADERS_MAP = {
        'id': 'ID',
        'numero': 'Numero',
        'fecha': 'Fecha',
        'fecha_vence': 'Vencimiento',
        'documento_tipo_id': 'Documento ID',
        'documento_tipo__nombre': 'Documento',
        'contacto_id': 'Contacto ID',
        'contacto__numero_identificacion': 'Numero identificacion',
        'contacto__nombre_corto': 'Contacto',
        'descuento': 'Descuento',
        'subtotal': 'Subtotal',
        'base_impuesto': 'Base',
        'impuesto': 'Impuesto',
        'total': 'Total',
        'afectado': 'Abono',
        'pendiente': 'Pendiente',
        'estado_aprobado': 'Aprobado',
        'estado_anulado': 'Anulado',
        'estado_electronico': 'Electronico',
        'estado_electronico_enviado': 'Electronico enviado',
        'estado_electronico_notificado': 'Electronico notificado'
    }

    def __init__(self, data, sheet_name="Datos", filename="export.xlsx"):
        self.data = data
        self.sheet_name = sheet_name
        self.filename = filename

    def _get_headers(self):        
        if not self.data:
            return []
        
        original_headers = list(self.data[0].keys())
        return [self.HEADERS_MAP.get(header, header) for header in original_headers]

    def _get_original_headers(self):
        return list(self.data[0].keys()) if self.data else []

    def exportar(self):
        # Debe quedar write_only y no permite estilos para procesamiento de grandes volumenes
        wb = Workbook(write_only=True)
        ws = wb.create_sheet(title=self.sheet_name)        
        if self.data:
            headers = list(self.data[0].keys())
            ws.append(headers)                       
            for row_data in self.data:
                row = []
                for col in headers:
                    value = row_data.get(col, '')
                    if value is None:
                        value = ''
                    row.append(str(value))
                ws.append(row)    
        virtual_workbook = BytesIO()
        wb.save(virtual_workbook)
        virtual_workbook.seek(0)        
        response = HttpResponse(
            virtual_workbook.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        return response
    
    def exportar_estilo(self):
        wb = Workbook()
        ws = wb.active
        ws.title = self.sheet_name        
        estilo = Font(name='Arial', size=10)        
        estilo_decimal = '#,##0.00'
        if self.data:
            headers = list(self.data[0].keys())
            ws.append(headers)                        
            estilo_encabezado = Font(name='Arial', size=10, bold=True)
            for cell in ws[1]:
                cell.font = estilo_encabezado

            for row_data in self.data:
                row = []
                for col in headers:
                    value = row_data.get(col, '')     
                    if value is None:
                        value = ''                               
                    if not isinstance(value, (int, float, Decimal)):
                        value = smart_str(value)
                    row.append(value)                
                ws.append(row)                
                
                for cell in ws[ws.max_row]:
                    if isinstance(cell.value, (float, Decimal)):
                        cell.number_format = estilo_decimal
                    cell.font = estilo

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        wb.save(response)
        return response    

    def exportar_informe(self):
        wb = Workbook()
        ws = wb.active
        ws.title = self.sheet_name

        if self.data:
            # Estilos
            estilo_normal = Font(name='Arial', size=10)
            estilo_encabezado = Font(name='Arial', size=10, bold=True)
            estilo_decimal = NamedStyle(name="decimal_style")
            estilo_decimal.font = estilo_normal
            estilo_decimal.number_format = '#,##0.00'
            if "decimal_style" not in wb.named_styles:
                wb.add_named_style(estilo_decimal)

            #headers = list(self.data[0].keys())
            headers = self._get_headers()
            original_headers = self._get_original_headers()
            # Encabezados
            for col_idx, col_name in enumerate(headers, start=1):
                cell = ws.cell(row=1, column=col_idx, value=col_name)
                cell.font = estilo_encabezado

            # Filas de datos
            for row_idx, row_data in enumerate(self.data, start=2):
                for col_idx, col in enumerate(original_headers, start=1):
                    value = row_data.get(col, '')
                    if value is None:
                        value = ''
                    elif isinstance(value, bool):
                        value = 'SI' if value else 'NO'                        
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    cell.font = estilo_normal

                    if isinstance(value, (float, Decimal)):
                        cell.style = estilo_decimal

        virtual_workbook = BytesIO()
        wb.save(virtual_workbook)
        virtual_workbook.seek(0)
        response = HttpResponse(
            virtual_workbook.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        return response
    