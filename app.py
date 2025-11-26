# app.py
# ---------------------------------------------------------
# Sistema de Auditoría Indiciaria (ICI) – Versión 5
# ---------------------------------------------------------
# Interfaz en Streamlit para:
#   - Cargar sentencias (PDF / Word)
#   - O pegar texto directamente
#   - Limpiar el texto
#   - Evaluar C1–C12 e Índice de Coherencia Indiciaria (ICI)
# ---------------------------------------------------------

import streamlit as st
from io import StringIO

from extractores import leer_pdf, leer_word, limpiar_texto
from evaluador import evaluar_texto

st.set_page_config(
    page_title="Sistema de Auditoría Indiciaria (ICI) – Versión 5",
    layout="wide"
)

st.title("Sistema de Auditoría Indiciaria (ICI) – Versión 5")
st.caption(
    "Herramienta experimental para evaluar la calidad del razonamiento indiciario "
    "en sentencias y resoluciones penales, basada en los criterios C1–C12 y en un "
    "Índice de Coherencia Indiciaria (ICI) ponderado."
)

st.markdown(
    """
    **Advertencia:**  
    Este sistema no sustituye el análisis jurídico humano.  
    Ofrece una auditoría automática de patrones textuales asociados al método de prueba indiciaria, 
    máximas de experiencia, control de sesgos y coherencia global del razonamiento.
    """
)

st.write("---")

col_izq, col_der = st.columns([1.1, 1])

with col_izq:
    st.subheader("1. Ingreso del documento")

    opcion = st.radio(
        "¿Cómo deseas ingresar la sentencia o resolución a analizar?",
        ("Subir archivo PDF/Word", "Pegar texto manualmente")
    )

    texto_bruto = ""

    if opcion == "Subir archivo PDF/Word":
        archivo = st.file_uploader(
            "Sube aquí el archivo de la sentencia (PDF o Word):",
            type=["pdf", "docx", "doc"]
        )

        if archivo is not None:
            nombre = archivo.name.lower()
            try:
                if nombre.endswith(".pdf"):
                    texto_bruto = leer_pdf(archivo)
                elif nombre.endswith(".docx") or nombre.endswith(".doc"):
                    texto_bruto = leer_word(archivo)
                else:
                    st.error("Formato de archivo no reconocido.")

                if texto_bruto:
                    st.success("Archivo cargado correctamente.")
                    with st.expander("Ver texto bruto extraído (opcional)"):
                        st.text_area(
                            "Texto bruto extraído",
                            value=texto_bruto,
                            height=200
                        )
            except Exception as e:
                st.error(f"Ocurrió un error leyendo el archivo: {e}")
    else:
        texto_bruto = st.text_area(
            "Pega aquí el texto de la sentencia o resolución:",
            height=250,
            placeholder=(
                "Pega la parte relevante de la sentencia "
                "(considerandos, fundamentos, motivación indiciaria, etc.)"
            )
        )

    texto_limpio = ""
    if texto_bruto:
        try:
            texto_limpio = limpiar_texto(texto_bruto)
        except Exception:
            texto_limpio = texto_bruto

    st.write("")
    analizar = st.button("Analizar coherencia indiciaria (C1–C12)", type="primary")

with col_der:
    st.subheader("2. Resultados del análisis")

    if analizar:
        if not texto_limpio.strip():
            st.warning("No hay texto para analizar. Sube un archivo o pega contenido antes de presionar el botón.")
        else:
            try:
                resultados = evaluar_texto(texto_limpio)
            except Exception as e:
                st.error(f"Error al evaluar el texto: {e}")
            else:
                criterios = resultados.get("criterios", {})
                ici_sin = resultados.get("ICI_sin_penalizacion", 0.0)
                ici_aj = resultados.get("ICI_ajustado", 0.0)
                interpretacion = resultados.get("interpretacion", "")

                st.markdown("### Resultados por criterio (C1–C12)")
                st.json(criterios)

                st.write("")
                st.markdown("### Índice de Coherencia Indiciaria (ICI) global")

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("ICI ajustado", f"{ici_aj:.2f}")
                with c2:
                    st.metric("ICI sin penalización por C5", f"{ici_sin:.2f}")
                with c3:
                    st.metric("C5 (hipótesis alternativas)", f"{criterios.get('C5', 0)}")

                st.write("")
                st.markdown("**Interpretación:** " + interpretacion)

                st.info(
                    "Nota metodológica: la Versión 5 incorpora, además de los criterios clásicos de la prueba indiciaria, "
                    "el uso de máximas de experiencia (C8), el control de sesgos y estereotipos (C9), la detección de "
                    "falacias probatorias (C10), el análisis de cadenas inferenciales (C11) y la diferenciación entre "
                    "doctrina citada y aplicación al caso concreto (C12)."
                )
    else:
        st.write("Cuando cargues o pegues una sentencia, presiona el botón de análisis para ver los resultados.")
