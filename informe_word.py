from io import BytesIO
from typing import Dict, Any
from docx import Document
from docx.shared import Pt


# ============================
# UTILIDADES DE FORMATO
# ============================

def agregar_titulo(doc, texto, size=16, bold=True):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.bold = bold
    r.font.size = Pt(size)


def agregar_parrafo(doc, texto, size=11, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.bold = bold
    r.font.size = Pt(size)


def agregar_tabla_criterios(doc, criterios: Dict[str, int]):
    if not criterios:
        agregar_parrafo(doc, "No se encontraron criterios evaluados.")
        return

    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"

    hdr = table.rows[0].cells
    hdr[0].text = "Criterio"
    hdr[1].text = "Puntaje"

    for k, v in criterios.items():
        row = table.add_row().cells
        row[0].text = k
        row[1].text = str(v)


def agregar_incongruencias(doc, incong):
    if not incong:
        agregar_parrafo(doc, "No se registraron incongruencias detectadas.")
        return

    if isinstance(incong, str):
        agregar_parrafo(doc, incong)
    elif isinstance(incong, list):
        for i, item in enumerate(incong, 1):
            agregar_parrafo(doc, f"{i}. {item}")
    elif isinstance(incong, dict):
        for k, v in incong.items():
            agregar_parrafo(doc, f"- {k}: {v}")
    else:
        agregar_parrafo(doc, str(incong))


# ============================
# FUNCIÓN PRINCIPAL
# ============================

def generar_informe(texto, resultados: Dict[str, Any], incong):
    doc = Document()

    # PORTADA
    agregar_titulo(doc, "INFORME DE COHERENCIA INDICIARIA – ICI V5", size=18)
    agregar_parrafo(doc, "Sistema de Auditoría Indiciaria – versión V5.")
    agregar_parrafo(doc, "")
    agregar_parrafo(doc, "Este informe resume el análisis automatizado realizado sobre la sentencia cargada.")
    doc.add_page_break()

    # RESUMEN ICI
    agregar_titulo(doc, "1. RESUMEN DEL ÍNDICE DE COHERENCIA INDICIARIA", size=14)
