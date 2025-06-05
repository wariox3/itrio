from openpyxl import Workbook
from django.utils.encoding import smart_str
from django.http import HttpResponse

class ExportarExcel:
    def __init__(self, data, sheet_name="Datos", filename="export.xlsx"):
        self.data = data
        self.sheet_name = sheet_name
        self.filename = filename

    def export(self):
        wb = Workbook()
        ws = wb.active
        ws.title = self.sheet_name

        if self.data:
            headers = list(self.data[0].keys())
            ws.append(headers)

            for row_data in self.data:
                row = [smart_str(row_data.get(col, '')) for col in headers]
                ws.append(row)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        wb.save(response)
        return response

