import streamlit as st
import traceback

# ======================================
#   TÍTULO PRINCIPAL
# ======================================

st.title("📘 Sistema de Auditoría Indiciaria - ICI V5")
st.write("Evaluación automática de sentencias y resoluciones judiciales (C1–C12).")

# ======================================
#   OPCIÓN DE INGRESO
# ======================================

opcion = st.radio(
    "¿Cómo deseas ingresar la sentencia o resolución a analizar?",
    ("Subir archivo PDF/Word", "Pegar texto manualmente")
)

texto_bruto = ""


# ======================================
#   OPCIÓN 1: SUBIR ARCHIVO
# ======================================

if opcion == "Subir archivo PDF/Word":

    archivo = st.file_uploader(
        "Sube aquí el archivo de la sentencia (PDF o Word):",
        type=["pdf", "docx", "doc"]
    )

    if archivo is not None:
        st.info("📄 Archivo recibido, intentando leer…")

        # 1. Intentamos importar las funciones de lectura
        try:
            from extractores import leer_pdf, leer_word
        except Exception:
            st.error("❌ Error al importar el módulo 'extractores.py'.")
            st.code(traceback.format_exc())
            st.stop()

        # 2. Intentamos leer el archivo
        try:
            archivo.seek(0)
            nombre = archivo.name.lower()

            if nombre.endswith(".pdf"):
                texto_bruto = leer_pdf(archivo)

            elif nombre.endswith(".docx") or nombre.endswith(".doc"):
                texto_bruto = leer_word(archivo)

            else:
                st.error("Formato de archivo no reconocido. Usa PDF o Word.")
                st.stop()

            if not texto_bruto or texto_bruto.strip() == "":
                st.warning("⚠ El archivo se leyó, pero el texto está vacío o no se pudo extraer.")
            else:
                st.success("✔ Texto extraído correctamente.")

        except Exception:
            st.error("❌ Ocurrió un error al leer el archivo.")
            st.code(traceback.format_exc())
            st.stop()


# ======================================
#   OPCIÓN 2: PEGAR TEXTO MANUALMENTE
# ======================================

if opcion == "Pegar texto manualmente":
    texto_bruto = st.text_area(
        "Pega aquí el texto completo de la sentencia o resolución:",
        height=300
    )


# ======================================
#   BOTÓN PARA INICIAR ANÁLISIS
# ======================================

if st.button("🔍 Iniciar análisis indiciario"):

    if not texto_bruto or texto_bruto.strip() == "":
        st.error("❌ No hay texto para analizar. Sube un archivo o pega el contenido primero.")
        st.stop()

    st.info("🧠 Iniciando análisis… esto puede tardar unos segundos.")

    # 1. Intentamos importar los módulos de análisis
    try:
        from evaluador import evaluar_todo
        from incongruencias import analizar_incongruencias
        from informe_word import generar_informe
    except Exception:
        st.error("❌ Error al importar 'evaluador.py', 'incongruencias.py' o 'informe_word.py'.")
        st.code(traceback.format_exc())
        st.stop()

    # 2. Ejecutamos el análisis completo dentro de un try/except
    try:
        # Evaluación C1–C12 (ajusta al nombre real de tu función si es necesario)
        resultados = evaluar_todo(texto_bruto)

        # Análisis de incongruencias
        incong = analizar_incongruencias(texto_bruto, resultados)

        # Mostramos resultados en pantalla
        st.subheader("📊 Resultados del Análisis (C1–C12)")
        st.json(resultados)

        st.subheader("🧩 Incongruencias detectadas")
        st.json(incong)

        # Generamos informe en Word
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
