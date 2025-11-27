import re
from typing import Dict, Any


# ============================================================
# UTILIDADES BÁSICAS
# ============================================================

def normalizar_texto(texto: str) -> str:
    """
    Limpia mínimamente el texto: pasa a minúsculas y quita espacios redundantes.
    """
    if not texto:
        return ""
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def contar_patrones(texto: str, patrones) -> int:
    """
    Cuenta cuántas veces aparecen uno o varios patrones (palabras o expresiones regulares).
    `patrones` puede ser una lista de strings o un solo string.
    """
    if isinstance(patrones, str):
        patrones = [patrones]
    total = 0
    for p in patrones:
        total += len(re.findall(p, texto, flags=re.IGNORECASE))
    return total


# ============================================================
# EVALUACIÓN POR CRITERIOS (C1–C12)
# ------------------------------------------------------------
# NOTA: Estos son criterios heurísticos básicos, pensados para
# que el sistema funcione de punta a punta. Luego podemos
# afinarlos juntos con tu metodología exacta.
# ============================================================

def evaluar_C1(texto: str) -> int:
    """
    C1: Existencia y claridad de INDICIOS / HECHOS BASE.
    Evalúa si el texto usa lenguaje propio de prueba indiciaria.
    """
    n = contar_patrones(texto, [
        r"\bindicio\b",
        r"\bhecho indiciario\b",
        r"\bhecho base\b",
        r"\bhechos base\b"
    ])
    if n >= 8:
        return 100
    elif n >= 4:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 20


def evaluar_C2(texto: str) -> int:
    """
    C2: Individualización de las FUENTES PROBATORIAS de cada indicio.
    Busca referencias explícitas a actas, pericias, declaraciones, etc.
    """
    n = contar_patrones(texto, [
        r"\bacta\b",
        r"\bpericia\b",
        r"\bdeclaraci[oó]n\b",
        r"\btestigo\b",
        r"\binforme pericial\b",
        r"\bata\b",
        r"\bfojas\b",
        r"\bfolio\b",
    ])
    if n >= 10:
        return 100
    elif n >= 6:
        return 80
    elif n >= 3:
        return 60
    elif n >= 1:
        return 40
    else:
        return 20


def evaluar_C3(texto: str) -> int:
    """
    C3: Conexión lógica entre HECHOS BASE y HECHOS CONSECUENCIA.
    Busca expresiones típicas de inferencia causal.
    """
    n = contar_patrones(texto, [
        r"\bpor lo tanto\b",
        r"\ben consecuencia\b",
        r"\bse infiere\b",
        r"\bse concluye\b",
        r"\bde ello se desprende\b",
        r"\bpor consiguiente\b",
    ])
    if n >= 8:
        return 100
    elif n >= 4:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 20


def evaluar_C4(texto: str) -> int:
    """
    C4: Pluralidad, convergencia y PERSISTENCIA de indicios.
    Busca referencias a 'conjunto de indicios', 'pluralidad', etc.
    """
    n = contar_patrones(texto, [
        r"\bconjunto de indicios\b",
        r"\bpluralidad de indicios\b",
        r"\bvarios indicios\b",
        r"\bindicios convergentes\b",
        r"\bconvergencia de indicios\b",
    ])
    if n >= 5:
        return 100
    elif n >= 3:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 20


def evaluar_C5(texto: str) -> int:
    """
    C5: Consideración de HIPÓTESIS ALTERNATIVAS / EXPLICACIONES INOCENTES.
    Este criterio es clave: suele ser bajo cuando la sentencia no discute
    seriamente la versión de descargo.
    """
    n = contar_patrones(texto, [
        r"\bhip[oó]tesis alternativa\b",
        r"\bversion de descargo\b",
        r"\bexplicaci[oó]n alternativa\b",
        r"\bposible explicaci[oó]n\b",
        r"\bno se descarta\b",
        r"\bpodr[ií]a explicarse\b",
    ])
    if n >= 5:
        return 100
    elif n >= 3:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 10  # C5 muy sensible: si no hay nada, puntaje casi nulo


def evaluar_C6(texto: str) -> int:
    """
    C6: Respeto de la PRESUNCIÓN DE INOCENCIA y estándares de prueba.
    """
    n = contar_patrones(texto, [
        r"\bpresunci[oó]n de inocencia\b",
        r"\bm[aá]s all[aá] de toda duda razonable\b",
        r"\best[aá]ndar probatorio\b",
        r"\bcarga de la prueba\b",
    ])
    if n >= 5:
        return 100
    elif n >= 3:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 20


def evaluar_C7(texto: str) -> int:
    """
    C7: Coherencia global del razonamiento (ausencia de contradicciones internas).
    Heurística: penalizamos la coexistencia de expresiones contradictorias
    tipo 'no se ha acreditado' / 'se encuentra plenamente probado'.
    """
    neg = contar_patrones(texto, [
        r"\bno se ha acreditado\b",
        r"\bno se prob[oó]\b",
        r"\bno existe prueba\b",
    ])
    pos = contar_patrones(texto, [
        r"\bse encuentra plenamente probado\b",
        r"\bqueda acreditado\b",
        r"\bprueba suficiente\b",
    ])
    # Si hay mucho de ambos, asumimos posible incoherencia
    if pos == 0 and neg == 0:
        return 40
    if pos > 0 and neg > 0 and abs(pos - neg) <= 2:
        return 30  # posible contradicción
    if pos >= 3 and neg == 0:
        return 90
    if pos >= 1 and neg == 0:
        return 70
    if neg >= 3 and pos == 0:
        # reconoce falta de prueba: puede ser un razonamiento garantista
        return 80
    return 50


def evaluar_C8(texto: str) -> int:
    """
    C8: Claridad en la descripción del HECHO IMPUTADO y su marco fáctico.
    """
    n = contar_patrones(texto, [
        r"\bfecha\b",
        r"\blugar\b",
        r"\bhecho imputado\b",
        r"\bocurri[oó]\b",
        r"\baconteci[oó]\b",
        r"\brelato f[aá]ctico\b",
    ])
    if n >= 8:
        return 100
    elif n >= 4:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 30


def evaluar_C9(texto: str) -> int:
    """
    C9: Individualización del aporte del acusado (rol funcional).
    """
    n = contar_patrones(texto, [
        r"\bfunci[oó]n\b",
        r"\brol\b",
        r"\bparticipaci[oó]n\b",
        r"\baporte\b",
        r"\bintervenci[oó]n\b",
    ])
    if n >= 6:
        return 100
    elif n >= 3:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 30


def evaluar_C10(texto: str) -> int:
    """
    C10: Tratamiento de la prueba de descargo (testigos de defensa, documentos, etc.).
    """
    n = contar_patrones(texto, [
        r"\bprueba de descargo\b",
        r"\btestigo de descargo\b",
        r"\bse valor[oó] la versi[oó]n del acusado\b",
        r"\bprueba ofrecida por la defensa\b",
    ])
    if n >= 4:
        return 100
    elif n >= 2:
        return 80
    elif n >= 1:
        return 60
    else:
        return 25


def evaluar_C11(texto: str) -> int:
    """
    C11: Claridad en la motivación sobre la TIPICIDAD (subsunción).
    """
    n = contar_patrones(texto, [
        r"\bt[ií]pico\b",
        r"\btipicidad\b",
        r"\bencuadra en el tipo penal\b",
        r"\belementos del tipo penal\b",
        r"\badecuaci[oó]n t[ií]pica\b",
    ])
    if n >= 5:
        return 100
    elif n >= 3:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 30


def evaluar_C12(texto: str) -> int:
    """
    C12: Claridad en la motivación de la PENA (proporcionalidad, culpabilidad, etc.).
    """
    n = contar_patrones(texto, [
        r"\bpena\b",
        r"\bproporcionalidad\b",
        r"\bculpabilidad\b",
        r"\bgravedad del hecho\b",
        r"\bdeterminaci[oó]n judicial de la pena\b",
        r"\bcircunstancias atenuantes\b",
        r"\bcircunstancias agravantes\b",
    ])
    if n >= 7:
        return 100
    elif n >= 4:
        return 80
    elif n >= 2:
        return 60
    elif n >= 1:
        return 40
    else:
        return 30


# ============================================================
# CÁLCULO DEL ICI GLOBAL E INTERPRETACIÓN
# ============================================================

def calcular_ici(criterios: Dict[str, int]) -> Dict[str, Any]:
    """
    A partir del diccionario de criterios (C1–C12) calcula:
    - ICI_sin_penalizacion: media simple de los criterios.
    - ICI_ajustado: penaliza fuertemente C5 bajo (hipótesis alternativas).
    - Interpretación cualitativa del resultado.
    """
    valores = [v for v in criterios.values() if isinstance(v, (int, float))]
    if valores:
        ici_sin = sum(valores) / len(valores)
    else:
        ici_sin = 0.0

    # Penalización por mal tratamiento de hipótesis alternativas (C5)
    c5 = criterios.get("C5", 50)
    # Cuanto más bajo C5, mayor la penalización (hasta 20 puntos)
    penalizacion_c5 = max(0, (70 - c5) / 70 * 20)
    ici_aj = max(0.0, ici_sin - penalizacion_c5)

    # Interpretación
    if ici_aj >= 80:
        interpretacion = (
            "Riesgo BAJO: la coherencia indiciaria es globalmente sólida, "
            "aunque siempre debe contrastarse con una revisión cualitativa."
        )
    elif ici_aj >= 70:
        interpretacion = (
            "Riesgo MEDIO-BAJO: existen algunos puntos discutibles, pero la "
            "estructura indiciaria parece relativamente consistente."
        )
    elif ici_aj >= 60:
        interpretacion = (
            "Riesgo MEDIO: el razonamiento presenta debilidades relevantes, "
            "especialmente en la valoración de algunas fuentes o en la "
            "articulación de los indicios."
        )
    elif ici_aj >= 50:
        interpretacion = (
            "Riesgo ALTO: la coherencia indiciaria es frágil; se recomiendan "
            "observaciones críticas y eventualmente un recurso."
        )
    else:
        interpretacion = (
            "Riesgo MUY ALTO: la coherencia indiciaria es deficiente o casi "
            "inexistente, especialmente en hipótesis alternativas y "
            "coherencia global. Se sugiere un análisis profundo y replanteo "
            "de la decisión judicial."
        )

    return {
        "criterios": criterios,
        "ICI_sin_penalizacion": round(ici_sin, 2),
        "ICI_ajustado": round(ici_aj, 2),
        "interpretacion": interpretacion,
    }


# ============================================================
# FUNCIÓN PRINCIPAL PARA LA APP: evaluar_todo
# ============================================================

def evaluar_todo(texto: str) -> Dict[str, Any]:
    """
    Punto de entrada que usa la app de Streamlit.
    Recibe el texto completo de la sentencia y devuelve
    el paquete de resultados (criterios + ICI + interpretación).
    """
    texto = normalizar_texto(texto)

    criterios = {
        "C1": evaluar_C1(texto),
        "C2": evaluar_C2(texto),
        "C3": evaluar_C3(texto),
        "C4": evaluar_C4(texto),
        "C5": evaluar_C5(texto),
        "C6": evaluar_C6(texto),
        "C7": evaluar_C7(texto),
        "C8": evaluar_C8(texto),
        "C9": evaluar_C9(texto),
        "C10": evaluar_C10(texto),
        "C11": evaluar_C11(texto),
        "C12": evaluar_C12(texto),
    }

    return calcular_ici(criterios)
