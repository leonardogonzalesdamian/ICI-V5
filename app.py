import streamlit as st
import tempfile
import traceback
from pathlib import Path

# Importamos tus módulos internos
from extractores import leer_pdf, leer_word
from evaluador import evaluar_todo
from incongruencias import analizar_incongruencias
from informe_word import generar_informe


# ==============================
#   INTERFAZ PRINCIPAL
# ==============================

st.title("📘 Sistema de Auditoría Indiciaria - ICI V5")
st.write("Evaluación automática de sentencias y resoluciones judiciales (C1–C12).")


# ==============================
#   OPCIÓN DE INGRESO DE TEXTO
# ==============================

opcion = st.radio(
    "¿Cómo deseas ingresar la sentencia o resolución a analizar?",
    ("Subir archivo PDF/Word", "Pegar texto manualmente")
)

texto_bruto = ""


# ==============================
#   OPCIÓN 1: SUBIR ARCHIVO
# ==============================

if opcion == "Subir archivo PDF/Word":

    archivo = st.file_uploader(
        "Sube aquí el archivo de la sentencia (PDF o Word):",
        type=["pdf", "docx", "doc"]
    )

    if archivo is not None:
        st.info("📄 Archivo recibido, procesando…")

        try:
            # Aseguramos puntero al inicio
            archivo.seek(0)

            nombre = archivo.name.lower()

            # Detectamos el tipo de archivo
            if nombre.endswith(".pdf"):
                texto_bruto = leer_pdf(archivo)

            elif nombre.endswith(".docx") or nombre.endswith(".doc"):
                texto_bruto = leer_word(archivo)

            else:
                st.error("❌ Formato de archivo no reconocido.")
                st.stop()

            st.success("✔ Texto extraído correctamente.")

        except Exception:
            st.error("❌ Ocurrió un error al leer el archivo.")
            st.code(traceback.format_exc())
            st.stop()


# ==============================
#   OPCIÓN 2: PEGAR TEXTO
# ==============================

if opcion == "Pegar texto manualmente":

    texto_bruto = st.text_area(
        "Pega aquí el texto completo de la sentencia o resolución:",
        height=300
    )

    if texto_bruto.strip() == "":
        st.warning("⚠ Por favor ingresa el texto para continuar.")
        st.stop()


# ==============================
#   BOTÓN PARA INICIAR ANÁLISIS
# ==============================

if st.button("🔍 Iniciar análisis indiciario"):

    if texto_bruto.strip() == "":
        st.error("❌ No hay texto para analizar.")
        st.stop()

    st.info("🧠 Procesando… esto puede tardar unos segundos.")

    try:
        # 1. Evaluación completa (C1–C12)
        resultados = evaluar_todo(texto_bruto)
        st.success("✔ Evaluación completada.")

        # 2. Análisis de incongruencias
        incong = analizar_incongruencias(texto_bruto, resultados)
        st.success("✔ Análisis de incongruencias completado.")

        # 3. Mostrar resultados en pantalla
        st.subheader("📊 Resultados del Análisis (C1–C12)")
        st.json(resultados)

        st.subheader("🧩 Incongruencias detectadas")
        st.json(incong)

        # 4. Generación del informe Word
        st.info("📑 Generando informe en Word…")

        docx_bytes = generar_informe(texto_bruto, resultados, incong)

        st.success("✔ Informe generado correctamente.")

        st.download_button(
            "⬇ Descargar Informe ICI-V5 (Word)",
            data=docx_bytes,
            file_name="Informe_Indiciario_ICI-V5.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except Exception:
        st.error("❌ Ocurrió un error durante el análisis.")
        st.code(traceback.format_exc())
        st.stop()
