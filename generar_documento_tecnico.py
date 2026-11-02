# -*- coding: utf-8 -*-
import os
import sys
from datetime import date

from fpdf import FPDF

sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Documento_tecnico_Post-Cronos.pdf')

CYAN = (110, 193, 228)
DARK = (10, 10, 10)
GREY_BG = (244, 244, 246)
GREY = (110, 110, 115)
BORDER = (200, 200, 205)
TEXT = (30, 30, 34)

M = 14
PW = 210
CW = PW - 2 * M


class Doc(FPDF):

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', '', 8)
            self.set_text_color(*GREY)
            self.set_y(8)
            self.cell(0, 5, 'Post-Cronos: Cordoba 2060 - Documento Tecnico', align='L')
            self.cell(0, 5, f'Pagina {self.page_no()}', align='R')
            self.set_draw_color(*BORDER)
            self.line(M, 15, PW - M, 15)
            self.set_y(20)

    def footer(self):
        self.set_y(-12)
        self.set_font('helvetica', '', 7)
        self.set_text_color(*GREY)
        self.cell(0, 5, 'Proyecto participativo - Cordoba, Argentina - 2026', align='C')

    def section(self, num, title):
        self.check_page(8)
        self.ln(3)
        self.set_font('helvetica', 'B', 13)
        self.set_text_color(*DARK)
        self.cell(0, 7, f'{num}. {title}', new_x='LMARGIN', new_y='NEXT')
        self.set_fill_color(*CYAN)
        self.rect(M, self.get_y() + 0.5, 40, 1.2, 'F')
        self.ln(4)

    def sub(self, title):
        self.check_page(6)
        self.set_font('helvetica', 'B', 10.5)
        self.set_text_color(*DARK)
        self.cell(0, 6, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(1.5)

    def body(self, txt):
        self.set_font('helvetica', '', 9.5)
        self.set_text_color(*TEXT)
        self.multi_cell(CW, 5, txt, align='L')
        self.ln(1.5)

    def bullets(self, items):
        self.set_font('helvetica', '', 9.5)
        self.set_text_color(*TEXT)
        for it in items:
            self.multi_cell(CW, 5, '  -  ' + it)
            self.ln(0.8)
        self.ln(1.5)

    def check_page(self, need_mm):
        if self.get_y() + need_mm > 278:
            self.add_page()


def table(doc, headers, rows, widths=None, align_center=()):
    doc.check_page(len(rows) * 7 + 25)
    if widths is None:
        widths = [CW / len(headers)] * len(headers)
    doc.set_font('helvetica', 'B', 8.5)
    doc.set_fill_color(*DARK)
    doc.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        doc.cell(widths[i], 7, h, border=1, fill=True, align='C')
    doc.ln()
    doc.set_font('helvetica', '', 8.5)
    doc.set_text_color(*TEXT)
    fill = False
    for row in rows:
        doc.set_fill_color(*GREY_BG)
        for i, cell in enumerate(row):
            align = 'C' if i in align_center else 'L'
            doc.cell(widths[i], 6.5, str(cell), border=1, fill=fill, align=align)
        doc.ln()
        fill = not fill
    doc.ln(3)


doc = Doc(orientation='P', unit='mm', format='A4')
doc.set_margins(M, M, M)
doc.set_auto_page_break(auto=False)

# ---------- Portada / encabezado ----------
doc.add_page()
doc.set_fill_color(*DARK)
doc.rect(0, 0, PW, 78, 'F')
doc.set_fill_color(*CYAN)
doc.rect(0, 78, PW, 2, 'F')

doc.set_text_color(255, 255, 255)
doc.set_font('helvetica', 'B', 26)
doc.set_y(30)
doc.cell(CW, 12, 'Post-Cronos: Cordoba 2060', align='C')
doc.set_y(42)
doc.set_font('helvetica', '', 13)
doc.cell(CW, 8, 'Documento Tecnico del Proyecto', align='C')
doc.set_y(51)
doc.set_font('helvetica', '', 10)
doc.set_text_color(*CYAN)
doc.cell(CW, 6, 'Visualizacion de dibujos de ninos y adolescentes', align='C')
doc.set_y(60)
doc.set_font('helvetica', '', 9)
doc.set_text_color(230, 230, 235)
doc.cell(CW, 5, f'Version 1.0  |  {date.today().strftime("%d/%m/%Y")}', align='C')

doc.set_y(92)
doc.section(1, 'Resumen Ejecutivo')
doc.body(
    'Post-Cronos es un proyecto participativo en el que ninos y adolescentes imaginan y dibujan como sera la '
    'ciudad de Cordoba en el anio 2060. Cada participante completa un formulario en papel junto a su dibujo. El '
    'material se escanea, se almacena en Google Cloud Storage y se procesa con inteligencia artificial (Gemini, '
    'de Google) para extraer los datos estructurados del formulario: edad, genero, eje tematico, colegio, barrio '
    'y las descripciones textuales del dibujo. Los resultados se guardan en BigQuery y se publican en una pagina '
    'web con dashboard de estadisticas, galeria de dibujos y un analisis de tendencias generado con IA.'
)
doc.body(
    'Al dia de hoy el proyecto cuenta con 7 encuestas procesadas, todas del Instituto Santa Ana, y la web '
    'publica se encuentra en linea a traves de GitHub Pages.'
)

doc.section(2, 'Contexto y Objetivos')
doc.sub('Objetivo general')
doc.body(
    'Dar visibilidad a la vision que los jovenes tienen del futuro de su ciudad, combinando el material creativo '
    '(dibujos) con informacion estructurada procesable para el analisis educativo y urbano.'
)
doc.sub('Objetivos especificos')
doc.bullets([
    'Digitalizar y centralizar las encuestas y dibujos en la nube (GCS).',
    'Automatizar la extraccion de datos con vision por IA (Gemini).',
    'Consolidar los datos en BigQuery para consultas y analisis.',
    'Publicar un tablero web interactivo con estadisticas, galeria y tendencias.',
    'Generar resumenes de tendencias de los dibujos con IA para el equipo del proyecto.',
])

# ---------- Arquitectura ----------
doc.section(3, 'Arquitectura General')
doc.body(
    'El flujo de datos es un pipeline ETL simple y desacoplado: los datos fluyen del papel fisico hacia la nube '
    'y terminan en una pagina web estatica. Cada etapa usa un servicio de Google Cloud o GitHub Pages, sin '
    'servidores propios.'
)

box_w = 29
gap = 2.2
boxes = [
    ('Encuesta', 'papel + dibujo'),
    ('Escaneo', 'carga a GCS'),
    ('GCS', 'bucket de imagenes'),
    ('Gemini', 'extraccion IA'),
    ('BigQuery', 'tabla de datos'),
    ('Web', 'GitHub Pages'),
]
y0 = doc.get_y() + 4
x0 = M + (CW - (box_w * len(boxes) + gap * (len(boxes) - 1))) / 2
doc.set_font('helvetica', 'B', 6.5)
for i, (t, s) in enumerate(boxes):
    x = x0 + i * (box_w + gap)
    doc.set_fill_color(*DARK)
    doc.rect(x, y0, box_w, 20, 'F')
    doc.set_text_color(255, 255, 255)
    doc.set_xy(x, y0 + 4)
    doc.cell(box_w, 5, t, align='C')
    doc.set_font('helvetica', '', 6)
    doc.set_text_color(*CYAN)
    doc.set_xy(x, y0 + 10.5)
    doc.cell(box_w, 5, s, align='C')
    doc.set_font('helvetica', 'B', 6.5)
    if i < len(boxes) - 1:
        ax = x + box_w + 0.3
        doc.set_text_color(*GREY)
        doc.set_xy(ax, y0 + 7)
        doc.cell(gap - 0.6, 5, '>', align='C')
doc.set_y(y0 + 24)

doc.sub('Descripcion de las etapas')
doc.bullets([
    'Escaneo: los formularios y dibujos se escanean como imagenes (JPG) y se organizan en carpetas por colegio.',
    'Storage: las imagenes se suben al bucket publico "post-cronos-dibujos-2060" (GCS).',
    'Extraccion: Gemini recibe cada imagen y devuelve JSON con los campos del formulario (la IA busca las X/tildes marcadas).',
    'Persistencia: los JSON se insertan en la tabla post_cronos.encuestas de BigQuery.',
    'Publicacion: scripts locales generan archivos JS (data.js, resumen_ia.js) que consume la pagina estatica publicada en GitHub Pages.',
])

# ---------- Stack ----------
doc.section(4, 'Stack Tecnologico')
table(doc,
      ['Componente', 'Servicio', 'Uso'],
      [
          ['Storage de imagenes', 'Google Cloud Storage', 'Bucket post-cronos-dibujos-2060'],
          ['Base de datos analitica', 'BigQuery', 'Tabla post_cronos.encuestas'],
          ['IA / Vision', 'Vertex AI Gemini', 'Modelo gemini-2.5-flash-lite'],
          ['Pagina web', 'GitHub Pages', 'index.html estatico'],
          ['Lenguaje de scripts', 'Python', 'ETL, procesamiento y generacion de datos'],
          ['Graficos web', 'Chart.js', 'Dashboard interactivo'],
      ],
      widths=[46, 44, 100],
      align_center=())

# ---------- Pipeline ----------
doc.section(5, 'Pipeline de Procesamiento')
doc.body('El procesamiento de una tanda de encuestas se realiza con el script process_with_gemini.py:')
doc.bullets([
    'Paso 1 - Verifica la tabla en BigQuery (crea el esquema si no existe).',
    'Paso 2 - Lista las imagenes de la carpeta del colegio en GCS y las ordena por nombre.',
    'Paso 3 - Para cada imagen arma un prompt que pide a Gemini extraer JSON (edad, genero, institucion, barrio, ejes tematicos, interpretacion del dibujo y transcripcion literal del texto).',
    'Paso 4 - Inserta cada registro en BigQuery con la URL publica de la imagen.',
    'Paso 5 - Corrige y normaliza datos con scripts auxiliares (generos, URLs, nombres de colegios).',
])

# ---------- Modelo de datos ----------
doc.section(6, 'Modelo de Datos (BigQuery)')
doc.body('Esquema de la tabla laboratorio-cordoba-2060.post_cronos.encuestas:')
table(doc,
      ['Campo', 'Tipo', 'Descripcion'],
      [
          ['id_encuesta', 'STRING', 'Identificador (colegio_numero, ej. santa_ana_5334)'],
          ['edad', 'INTEGER', 'Edad del participante'],
          ['genero', 'STRING', 'Masculino / Femenino / No binario / Otro / No responder'],
          ['colegio', 'STRING', 'Institucion educativa'],
          ['ciudad_barrio', 'STRING', 'Barrio o ciudad'],
          ['fecha_registro', 'TIMESTAMP', 'Fecha de procesamiento'],
          ['url_imagen_dibujo', 'STRING', 'URL publica del dibujo en GCS'],
          ['eje', 'STRING', 'Eje tematico (puede ser multiple, separado por coma)'],
          ['descripcion_audio_o_ia', 'STRING', 'Interpretacion del dibujo generada por IA'],
          ['descripcion_final_texto', 'STRING', 'Texto literal escrito por el participante'],
      ],
      widths=[44, 28, 118],
      align_center=())
doc.body(
    'Los ejes tematicos admitidos son: Moda, Tecnologia, Mobiliario, Educacion, Herramientas, Salud, '
    'Comunicacion y Otro. El campo "eje" puede contener varios valores separados por coma.'
)

# ---------- Scripts ----------
doc.section(7, 'Scripts del Proyecto')
table(doc,
      ['Script', 'Funcion'],
      [
          ['process_with_gemini.py', 'Procesa una tanda de encuestas desde GCS con Gemini hacia BigQuery'],
          ['generate_data.py', 'Lee BigQuery y genera data.js (datos de la web)'],
          ['analisis_tendencias.py', 'Envia los datos a Gemini y genera resumen_ia.js (tendencias IA)'],
          ['update_generos.py', 'Corrige generos en BigQuery'],
          ['update_urls_bq.py', 'Migra URLs de gs:// a https://'],
          ['add_genero.py / add_eje_column.py', 'Agrega columnas al esquema'],
          ['check_schema.py / check_acl.py', 'Verificacion de esquema y permisos del bucket'],
          ['create_bucket.py / make_public.py', 'Creacion y publicacion del bucket'],
      ],
      widths=[70, 120],
      align_center=())

# ---------- Web ----------
doc.section(8, 'Pagina Web y Dashboard')
doc.body(
    'La pagina (index.html) se publica en https://post-cronos.github.io/post-cronos/ y se actualiza '
    'regenerando los archivos data.js y resumen_ia.js y subiendo los cambios al repositorio. Tiene dos vistas:'
)
doc.sub('Vista 1 - Dashboard')
doc.bullets([
    'Tarjetas de resumen: participantes, con dibujo, ejes tematicos, colegios y edad promedio.',
    'Graficos (Chart.js): distribucion por edad, genero, ejes tematicos, colegios y barrios.',
    'Panel "Tendencias 2060": resumen general, tendencias detectadas, insights por eje y recomendaciones, generado con Gemini.',
    'Tabla de participantes con todas las encuestas.',
])
doc.sub('Vista 2 - Galeria de dibujos')
doc.bullets([
    'Tarjetas con el dibujo completo (sin recortes), colegio, badges de eje/genero/edad/barrio, interpretacion de IA y texto del participante.',
    'Filtros por eje tematico, genero y busqueda por barrio o colegio.',
])

# ---------- IA ----------
doc.section(9, 'Analisis de Tendencias con IA')
doc.body(
    'El script analisis_tendencias.py consulta BigQuery, arma un prompt con el detalle de todos los participantes '
    'y pide a Gemini un analisis de tendencias en JSON con: resumen general, lista de tendencias detectadas '
    '(con ejemplos citando IDs), observaciones por eje tematico y recomendaciones para el equipo. El resultado se '
    'guarda en resumen_ia.js y se muestra en el dashboard.'
)
doc.body(
    'El analisis actual detecto que la vision predominante es una Cordoba tecnologica pero en armonia con la '
    'naturaleza, con tendencias en tecnologia integrada y sostenible, interfaces digitales avanzadas, '
    'automatizacion para la limpieza urbana y mobiliario inteligente.'
)

# ---------- Seguridad ----------
doc.section(10, 'Seguridad y Consideraciones')
doc.bullets([
    'Credenciales: el acceso a Google Cloud usa una cuenta de servicio; el archivo de credenciales (.json) esta excluido de git (.gitignore).',
    'El bucket de imagenes es publico de solo lectura (necesario para la web estatica).',
    'No se almacenan datos personales sensibles mas alla de edad, genero y localidad, con fines del proyecto.',
    'La pagina no expone claves ni datos internos; los datos publicos se limitan a los de la galeria y dashboard.',
    'Modelo Gemini: gemini-2.5-flash-lite, optimizado en costo para vision por lotes.',
])

# ---------- Resultados ----------
doc.section(11, 'Resultados Actuales')
table(doc,
      ['Indicador', 'Valor'],
      [
          ['Encuestas procesadas', '7'],
          ['Colegios', '1 (Instituto Santa Ana)'],
          ['Rango de edades', '15 - 17 anios'],
          ['Edad promedio', '16'],
          ['Generos', '7 Femenino'],
          ['Ejes predominantes', 'Tecnologia (5), Otro (1), Mobiliario (1)'],
          ['Estado de la web', 'En linea (GitHub Pages)'],
      ],
      widths=[70, 120],
      align_center=())

# ---------- Proximos pasos ----------
doc.section(12, 'Proximos Pasos')
doc.bullets([
    'Incorporar mas colegios y tandas de encuestas (la galeria y el analisis crecen automaticamente).',
    'Automatizar el pipeline en la nube (Cloud Scheduler + Cloud Run o funciones) para no depender de scripts locales.',
    'Mejorar la normalizacion de datos (localidades, colegios) y enriquecer el dashboard con mas metricas.',
    'Generar reportes periodicos en PDF a partir del analisis de tendencias.',
])

doc.output(OUTPUT)
print(f'OK - PDF generado: {OUTPUT}')
