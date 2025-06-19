from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment, Font, numbers
from openpyxl.utils import get_column_letter

class ExcelFunciones:
    def __init__(self):
        pass

    def agregar_titulo(self, ws, titulo, rango_titulo):
        ws.merge_cells(rango_titulo)
        celda_titulo = ws[rango_titulo.split(":")[0]]
        celda_titulo.value = titulo
        celda_titulo.font = Font(bold=True, size=14, color="000000")
        celda_titulo.alignment = Alignment(horizontal="center", vertical="center")
        celda_titulo.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

    def aplicar_estilos(self, ws, formato_numero=None):
        font = Font(name='Arial', size=10, bold=False)
        bold_font = Font(name='Arial', size=10, bold=True)
        fill = PatternFill(start_color="9CDFEB", end_color="9CDFEB", fill_type="solid")
        for row in ws.iter_rows():
            for cell in row:
                cell.font = font                    
                if cell.row == 1: 
                    cell.font = bold_font
                    cell.fill = fill
                else:
                    if formato_numero is not None and cell.column in formato_numero:
                        cell.number_format = '#,##0.00'
                if isinstance(cell.value, (int, float)):
                    cell.alignment = Alignment(horizontal='right')                                                                                                
                if isinstance(cell.value, bool):
                    cell.value = "SI" if cell.value else "NO"

        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if cell.value is not None:
                        max_length = max(max_length, len(str(cell.value)))
                except Exception as e:
                    print(f"Error al calcular el ancho para la celda {cell.coordinate}: {e}")                
            adjusted_width = (max_length + 1)
            ws.column_dimensions[column_letter].width = adjusted_width       