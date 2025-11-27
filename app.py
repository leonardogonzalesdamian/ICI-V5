import streamlit as st
import traceback

# ==============================
#   TÍTULO PRINCIPAL
# ==============================

st.title("📘 Sistema de Auditoría Indiciaria – ICI Versión 5")
st.write("""
Bienvenido, Leonardo.  
Este sistema permite evaluar automáticamente la coherencia indiciaria de sentencias y resoluciones judiciales basada en los criterios C1–C12.
""")


# ==============================
#   OPCIÓN DE INGRESO DE TEXTO
# ==============================

opcion = st.radio(
    "¿Cómo deseas ingresar la sentencia o resolución a analizar?",
    ("Subir archivo PDF/Word", "Pegar texto manualmente")
)

texto_bruto = ""


# =================================================
#   BLOQUE: SUBIR ARCHIVO PDF o WORD
# =================================================

if opcion == "Subir archivo PDF/Word":

    archivo = st.file_uploader(
        "Sube aquí el archivo de la sentencia:",
        type=["pdf", "docx", "doc"]
    )

    if archivo is not None:
        st.info("📄 Archivo recibido. Iniciando extracción de texto…")

        try:
            from extractores import leer_pdf, leer_word
        except Exception:
            st.error("❌ Error al importar el módulo `extractores.py`.")
            st.code(traceback.format_exc())
            st.stop()

        try:
            archivo.seek(0)
            nombre = archivo.name.lower()

            if nombre.endswith(".pdf"):
                texto_bruto = leer_pdf(archivo)
            elif nombre.endswith(".docx") or nombre.endswith(".doc"):
                texto_bruto = leer_word(archivo)
            else:
                st.error("Formato no reconocido.")
                st.stop()

            if not texto_bruto or texto_bruto.strip() == "":
                st.warning("⚠ No se pudo extraer texto del archivo.")
            else:
                st.success("✔ Texto extraído correctamente.")

        except Exception:
            st.error("❌ Error al procesar el archivo.")
            st.code(traceback.format_exc())
            st.stop()


# =================================================
#   BLOQUE: PEGAR TEXTO MANUALMENTE
# =================================================

if opcion == "Pegar texto manualmente":

    texto_bruto = st.text_area(
        "Pega aquí el texto de la sentencia:",
        height=300
    )

    if texto_bruto.strip() == "":
        st.warning("⚠ Por favor ingresa el texto para continuar.")


# =================================================
#   BOTÓN PARA INICIAR ANÁLISIS
# =================================================

if st.button("🔍 Iniciar Análisis Indiciario"):

    if texto_bruto.strip() == "":
        st.error("❌ No hay texto para analizar.")
        st.stop()

    st.info("🧠 Iniciando análisis… Por favor espera.")

    # Importamos los módulos de análisis dentro del botón
    try:
        from evaluador import evaluar_todo
        from incongruencias import analizar_incongruencias
        from informe_word import generar_informe
    except Exception:
        st.error("❌ Error al cargar los módulos de análisis.")
        st.code(traceback.format_exc())
        st.stop()

    try:
        resultados = evaluar_todo(texto_bruto)
        incong = analizar_incongruencias(texto_bruto, resultados)

        # Mostrar resultados
        st.subheader("📊 Resultados del análisis (C1–C12)")
        st.json(resultados)

        st.subheader("🧩 Incongruencias detectadas")
        st.json(incong)

        # Generar informe
        st.info("📑 Generando informe…")

        docx_bytes = generar_informe(texto_bruto, resultados, incong)

        st.success("✔ Informe generado exitosamente.")

        st.download_button(
            "⬇ Descargar Informe Word (ICI-V5)",
            data=docx_bytes,
            file_name="Informe_ICI_V5.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except Exception:
        st.error("❌ Error durante el análisis indiciario.")
        st.code(traceback.format_exc())
        st.stop()
