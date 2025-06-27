from openpyxl import Workbook
from openpyxl.styles import Font, NamedStyle
from django.utils.encoding import smart_str
from django.http import HttpResponse
from decimal import Decimal
from io import BytesIO

class ExcelExportar:
    def __init__(self, data, sheet_name="Datos", filename="export.xlsx"):
        self.data = data
        self.sheet_name = sheet_name
        self.filename = filename

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

    def exportar_estilo_informe(self):
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