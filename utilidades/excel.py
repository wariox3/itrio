from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment, Font
from openpyxl.utils import get_column_letter

class WorkbookEstilos(Workbook):
    def __init__(self, wb):
        self.wb = wb
        self.font = Font(name='Arial', size=10, bold=False)
        self.bold_font = Font(name='Arial', size=10, bold=True)
        self.alignment = Alignment(horizontal='left')
        self.fill = PatternFill(start_color="9CDFEB", end_color="9CDFEB", fill_type="solid")

    def aplicar_estilos(self):
        for sheet in self.wb.sheetnames:
            ws = self.wb[sheet]
            
            # Aplicar estilos por celda
            for row in ws.iter_rows():
                for cell in row:
                    cell.font = self.font
                    if cell.row == 1:  # Si es la primera fila (encabezado)
                        cell.font = self.bold_font
                        cell.fill = self.fill
                    if isinstance(cell.value, (int, float)):
                        cell.alignment = Alignment(horizontal='right')                         
                    if isinstance(cell.value, bool):
                        cell.value = "SI" if cell.value else "NO"

            # Ajustar el ancho de las columnas según el contenido más amplio
            for column in ws.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                for cell in column:
                    try:
                        if cell.value is not None:  # Asegurarse de que no sea None
                            max_length = max(max_length, len(str(cell.value)))
                    except Exception as e:
                        print(f"Error al calcular el ancho para la celda {cell.coordinate}: {e}")
                
                # Ajustar el ancho de la columna con un margen adicional
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column_letter].width = adjusted_width