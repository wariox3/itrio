from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFUtilidades:
    """
    Clase utilitaria para funcionalidades reutilizables en PDFs
    """
    
    # Canvas para pie de página
    class PieDePagina(canvas.Canvas):
        """Canvas reutilizable para numeración de páginas"""
        
        def __init__(self, *args, **kwargs):
            super(PDFUtilidades.PieDePagina, self).__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            """Agregar el número total de páginas a cada página"""
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.dibujar_numero_pagina(num_pages)
                super(PDFUtilidades.PieDePagina, self).showPage()
            super(PDFUtilidades.PieDePagina, self).save()

        def dibujar_numero_pagina(self, total_paginas):
            """Dibuja 'Página X de Y' en el footer"""
            pagina_actual = self.getPageNumber()
            texto = f"Página {pagina_actual} de {total_paginas}"
            
            self.setFont("Helvetica", 8)
            self.drawRightString(
                self._pagesize[0] - 0.5 * inch,
                0.4 * inch,
                texto
            )
    
    @staticmethod
    def dibujar_celda_con_borde(p, x, y, ancho, alto, titulo, valor=None, 
                            font_titulo="Helvetica-Bold", font_valor="Helvetica", 
                            size_titulo=9, size_valor=8, padding=5,
                            con_linea_divisora=True, solo_titulo=False,
                            ajuste_titulo=2):  # Nuevo parámetro para ajuste
        """
        Dibuja una celda con borde, con opción de solo título o título+valor
        
        Args:
            ... [parámetros existentes] ...
            ajuste_titulo: Ajuste vertical del título en puntos (positivo = subir)
        """
        
        # Dibujar el rectángulo del borde
        p.rect(x, y, ancho, alto)
        
        if solo_titulo:
            # Modo solo título - título centrado vertical y horizontalmente
            p.setFont(font_titulo, size_titulo)
            titulo_width = p.stringWidth(titulo.upper(), font_titulo, size_titulo)
            titulo_x = x + (ancho - titulo_width) / 2
            titulo_y = y + (alto - size_titulo) / 2 + ajuste_titulo  # Ajuste añadido
            p.drawString(titulo_x, titulo_y, titulo.upper())
        else:
            # Modo título + valor
            p.setFont(font_titulo, size_titulo)
            titulo_width = p.stringWidth(titulo.upper(), font_titulo, size_titulo)
            titulo_x = x + (ancho - titulo_width) / 2
            titulo_y = y + alto - size_titulo - padding + ajuste_titulo  # Ajuste añadido
            p.drawString(titulo_x, titulo_y, titulo.upper())
            
            if con_linea_divisora:
                # Ajustar también la línea divisora si es necesario
                p.line(x, titulo_y - padding, x + ancho, titulo_y - padding)
            
            if valor is not None:
                p.setFont(font_valor, size_valor)
                valor_str = str(valor) if valor is not None else ""
                valor_width = p.stringWidth(valor_str, font_valor, size_valor)
                valor_x = x + (ancho - valor_width) / 2
                valor_y = y + padding
                p.drawString(valor_x, valor_y, valor_str)
        
        return x + ancho
    
    # Métodos estáticos para estilos
    @staticmethod
    def obtener_estilos():
        """Retorna todos los estilos predefinidos"""
        estilos = getSampleStyleSheet()
        
        # Estilo etiqueta (bold)
        estilo_etiqueta = ParagraphStyle(
            'etiqueta',
            parent=estilos["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=11,
            spaceAfter=6
        )
        
        # Estilo dato (normal)
        estilo_dato = ParagraphStyle(
            'dato',
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            spaceAfter=6
        )
        
        # Estilo fecha
        estilo_fecha = ParagraphStyle(
            'fecha',
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            spaceAfter=6
        )
        
        # Estilo para tablas
        estilo_tabla = ParagraphStyle(
            'tabla',
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            wordWrap=True
        )
        
        # Estilo numérico para tablas (alineado a la derecha)
        estilo_numero_tabla = ParagraphStyle(
            'numero_tabla',
            parent=estilos["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            alignment=2,  # 2 = TA_RIGHT
            wordWrap=True
        )
        
        return {
            'etiqueta': estilo_etiqueta,
            'dato': estilo_dato,
            'fecha': estilo_fecha,
            'tabla': estilo_tabla,
            'numero_tabla': estilo_numero_tabla,
            'normal': estilos["Normal"],
            'titulo': estilos["Title"],
            'heading1': estilos["Heading1"],
            'heading2': estilos["Heading2"]
        }
    
    @staticmethod
    def estilo_etiqueta():
        """Retorna solo el estilo etiqueta"""
        estilos = PDFUtilidades.obtener_estilos()
        return estilos['etiqueta']
    
    @staticmethod
    def estilo_dato():
        """Retorna solo el estilo dato"""
        estilos = PDFUtilidades.obtener_estilos()
        return estilos['dato']
    
    @staticmethod
    def estilo_fecha():
        """Retorna solo el estilo fecha"""
        estilos = PDFUtilidades.obtener_estilos()
        return estilos['fecha']
    
    @staticmethod
    def estilo_tabla():
        """Retorna solo el estilo tabla"""
        estilos = PDFUtilidades.obtener_estilos()
        return estilos['tabla']
    
    @staticmethod
    def estilo_numero_tabla():
        """Retorna solo el estilo numérico para tablas"""
        estilos = PDFUtilidades.obtener_estilos()
        return estilos['numero_tabla']
    
    @staticmethod
    def formatear_fecha(fecha_obj, formato='%Y-%m-%d'):
        """
        Formatea un objeto fecha al formato especificado
        
        Args:
            fecha_obj: Objeto datetime o date
            formato: Formato de fecha (por defecto: '%Y-%m-%d')
        
        Returns:
            str: Fecha formateada o cadena vacía si no hay fecha
        """
        if not fecha_obj:
            return ""
        try:
            if hasattr(fecha_obj, 'strftime'):
                return fecha_obj.strftime(formato)
            else:
                # Si no es un objeto datetime, intentar convertirlo
                return str(fecha_obj)
        except (AttributeError, ValueError, TypeError):
            return str(fecha_obj) if fecha_obj else ""