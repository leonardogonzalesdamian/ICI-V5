# evaluador.py
# ---------------------------------------------------------
# Sistema de Auditoría Indiciaria (ICI) – Versión 5 (C1–C12)
# ---------------------------------------------------------
# C1–C7: estructura clásica de la prueba indiciaria.
# C8   : máximas de la experiencia / reglas científicas.
# C9   : sesgos y estereotipos.
# C10  : falacias y razonamientos probatorios dudosos.
# C11  : inferencias avanzadas (cadena inferencial, hechos intermedios).
# C12  : integridad textual y "red flags" (doctrina vs. caso concreto).
# ---------------------------------------------------------

import re
from typing import Dict


# =========================================================
#  C1 – C8
# =========================================================

def evaluar_C1(texto: str) -> int:
    """
    C1: Existencia y claridad de HECHOS BASE / INDICIOS.
    """
    patron_indicios = [
        r"\bindicio[s]?\b",
        r"hecho[s]? indiciario[s]?",
        r"hecho[s]? base\b",
        r"hecho[s]? indicador[ea]s?",
        r"datos incriminatorios",
        r"datos indiciarios",
    ]

    patron_esquemas = [
        r"H\s*1\b", r"H\s*2\b", r"H\s*3\b", r"H\s*4\b",
        r"hecho base\s*\d",
        r"indic[ií]o\s*\d",
    ]

    coincidencias_ind = sum(len(re.findall(p, texto, flags=re.I)) for p in patron_indicios)
    coincidencias_esq = sum(len(re.findall(p, texto, flags=re.I)) for p in patron_esquemas)

    if coincidencias_ind == 0 and coincidencias_esq == 0:
        return 20

    score = 50
    if coincidencias_ind >= 2:
        score += 15
    if coincidencias_esq >= 2:
        score += 15
    if coincidencias_ind + coincidencias_esq >= 6:
        score += 10

    return max(20, min(score, 95))


def evaluar_C2(texto: str) -> int:
    """
    C2: Fiabilidad de las fuentes probatorias.
    """
    patrones_analisis = [
        r"fiabilidad\b",
        r"credibilidad\b",
        r"veros[ií]mil",
        r"coherente[s]?",
        r"contradicci[oó]n",
        r"condiciones de percepci[oó]n",
        r"rigor metodol[oó]gico",
        r"origen de la prueba",
        r"calidad de la pericia",
    ]

    patrones_fuentes = [
        r"declaraci[oó]n del testigo",
        r"testigo presencial",
        r"testigo de o[ií]das",
        r"pericia\b",
        r"informe pericial",
        r"acta\b",
        r"informe policial",
        r"dictamen pericial",
    ]

    coincidencias_analisis = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_analisis)
    coincidencias_fuentes = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_fuentes)

    if coincidencias_fuentes == 0:
        return 20

    score = 40
    if coincidencias_analisis >= 2:
        score += 20
    if coincidencias_analisis >= 4:
        score += 15
    if coincidencias_analisis >= 6:
        score += 15

    return max(20, min(score, 95))


def evaluar_C3(texto: str) -> int:
    """
    C3: Relevancia del indicio / vínculo lógico entre hecho base y hecho consecuencia.
    """
    patrones_relevancia = [
        r"relevan[cia]",
        r"pertinenc[ia]",
        r"conducente",
        r"idoneidad probatoria",
        r"v[ií]nculo (l[oó]gico|causal)",
        r"relaci[oó]n (l[oó]gica|causal)",
        r"peso (probatorio|indiciario)",
        r"aporte (probatorio|indiciario)",
    ]

    patrones_enlace = [
        r"estos hechos permiten",
        r"estos indicios permiten",
        r"de lo actuado se (colige|concluye|infier[ee])",
        r"de (estos|tales|los) hechos se (colige|concluye|infier[ee])",
        r"se colige que",
        r"se concluye que",
        r"permite establecer",
        r"permite afirmar",
        r"permite vincular",
        r"guarda relaci[oó]n con",
        r"resultado natural de",
    ]

    patrones_suma = [
        r"H\s*1\s*\+\s*H\s*2",
        r"H\s*[0-9]+\s*y\s*H\s*[0-9]+",
        r"en conjunto con H\s*[0-9]+",
        r"la combinaci[oó]n de estos indicios",
    ]

    coincidencias_relev = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_relevancia)
    coincidencias_enlace = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_enlace)
    coincidencias_suma = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_suma)

    if coincidencias_relev == 0 and coincidencias_enlace == 0 and coincidencias_suma == 0:
        return 10

    score = 40
    if coincidencias_relev >= 2:
        score += 15
    if coincidencias_enlace >= 2:
        score += 15
    if coincidencias_suma >= 1 or (coincidencias_relev + coincidencias_enlace) >= 5:
        score += 20

    return max(10, min(score, 95))


def evaluar_C4(texto: str) -> int:
    """
    C4: Pluralidad y convergencia de indicios.
    """
    patrones_pluralidad = [
        r"pluralidad de indicios",
        r"diversos indicios",
        r"varios indicios",
        r"m[uú]ltiples indicios",
        r"conjunto de indicios",
        r"serie de indicios",
        r"m[uú]ltiples hechos",
    ]

    patrones_convergencia = [
        r"en conjunto permiten",
        r"considerados en su conjunto",
        r"convergen en",
        r"se refuerzan mutuamente",
        r"corroboran entre s[ií]",
        r"se corroboran",
        r"armonizan con",
        r"compatibles entre s[ií]",
        r"no se contradicen",
    ]

    patrones_explicitos = [
        r"indicios convergentes",
        r"estructura convergente",
        r"indicios perif[eé]ricos que convergen",
    ]

    coincidencias_plur = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_pluralidad)
    coincidencias_conv = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_convergencia)
    coincidencias_expl = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_explicitos)

    if coincidencias_plur == 0 and coincidencias_conv == 0 and coincidencias_expl == 0:
        return 10

    score = 35
    if coincidencias_plur >= 1:
        score += 15
    if coincidencias_conv >= 1:
        score += 15
    if coincidencias_conv >= 2 or coincidencias_expl >= 1:
        score += 20

    return max(10, min(score, 90))


def evaluar_C5(texto: str) -> int:
    """
    C5: Tratamiento de HIPÓTESIS ALTERNATIVAS.
    """
    patrones_menciona = [
        r"hip[oó]tesis alternativa",
        r"otras explicaciones razonables",
        r"explicaci[oó]n alternativa",
        r"posibilidad alternativa",
        r"otra versi[oó]n de los hechos",
    ]

    patrones_analiza = [
        r"esta hip[oó]tesis queda descartada",
        r"se descarta (esta|dicha) hip[oó]tesis",
        r"no resulta razonable aceptar",
        r"no es veros[ií]mil",
        r"no encuentra respaldo probatorio",
        r"carece de apoyo probatorio",
    ]

    coincidencias_m = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_menciona)
    coincidencias_a = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_analiza)

    if coincidencias_m == 0 and coincidencias_a == 0:
        return 20

    score = 40
    if coincidencias_m >= 2 and coincidencias_a >= 1:
        score += 20
    if coincidencias_m >= 3 and coincidencias_a >= 2:
        score += 20

    return max(20, min(score, 90))


def evaluar_C6(texto: str) -> int:
    """
    C6: Estándar de prueba y presunción de inocencia.
    """
    patrones = [
        r"presunci[oó]n de inocencia",
        r"duda razonable",
        r"m[aá]s all[aá] de toda duda razonable",
        r"est[aá]ndar probatorio",
        r"carga de la prueba",
        r"in dubio pro reo",
        r"certeza m[oó]ral",
        r"certeza m[aá]s all[aá] de la duda razonable",
    ]

    coincidencias = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones)

    if coincidencias == 0:
        return 30

    score = 55
    if coincidencias >= 3:
        score += 15
    if coincidencias >= 5:
        score += 15

    return max(30, min(score, 90))


def evaluar_C7(texto: str) -> int:
    """
    C7: Coherencia global del razonamiento indiciario.
    """
    patrones_estructura = [
        r"metodolog[ií]a (de la)? prueba indiciaria",
        r"esquema operativo",
        r"estructura (de la)? prueba indiciaria",
        r"en primer lugar[,;]",
        r"en segundo lugar[,;]",
        r"finalmente[,;]",
        r"en suma[,;]",
    ]

    patrones_contra = [
        r"contradicci[oó]n interna",
        r"incongruencia",
        r"incoherencia",
    ]

    coincidencias_estr = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_estructura)
    coincidencias_contra = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_contra)

    score = 40
    if coincidencias_estr >= 2:
        score += 20
    if coincidencias_estr >= 4:
        score += 20
    if coincidencias_contra >= 1:
        score -= 15

    return max(25, min(score, 90))


def evaluar_C8(texto: str) -> int:
    """
    C8: Máximas de la experiencia, reglas científicas y generalizaciones empíricas.
    """
    patrones_experiencia = [
        r"de acuerdo con la experiencia",
        r"seg[uú]n la experiencia",
        r"reglas de la experiencia",
        r"regla de experiencia",
        r"por regla general",
        r"lo normal es que",
        r"lo habitual es que",
        r"usualmente",
        r"ordinariamente",
        r"lo esperable es que",
    ]

    patrones_ciencia = [
        r"seg[uú]n la evidencia cient[ií]fica",
        r"seg[uú]n estudios cient[ií]ficos",
        r"la criminolog[ií]a muestra que",
        r"estudios criminol[oó]gicos indican",
        r"estudios emp[ií]ricos indican",
        r"estudios emp[ií]ricos muestran",
        r"la ciencia (jur[ií]dica|forense) indica",
    ]

    patrones_probabilidad = [
        r"en la mayor[ií]a de los casos",
        r"con alta probabilidad",
        r"es altamente probable",
        r"resulta poco probable que",
        r"resulta muy probable que",
    ]

    coincidencias_exp = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_experiencia)
    coincidencias_cien = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_ciencia)
    coincidencias_prob = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_probabilidad)

    total = coincidencias_exp + coincidencias_cien + coincidencias_prob

    if total == 0:
        return 20

    score = 45
    if coincidencias_exp >= 2:
        score += 15
    if coincidencias_cien >= 1:
        score += 15
    if coincidencias_prob >= 2 or total >= 5:
        score += 15

    return max(20, min(score, 90))


# =========================================================
#  C9 – SESGOS Y ESTEREOTIPOS
# =========================================================

def evaluar_C9(texto: str) -> int:
    """
    C9: Sesgos cognitivos y estereotipos en la valoración de la prueba,
    especialmente en la valoración de víctimas (p.ej. delitos sexuales,
    violencia, etc.).
    """
    patrones_estereotipos = [
        r"si realmente hubiera sido v[íi]ctima.*(habr[ií]a denunciado|denunciado de inmediato)",
        r"si realmente fuese v[íi]ctima.*(habr[ií]a denunciado|denunciado de inmediato)",
        r"no (denunci[oó]|denunci[óo]) de inmediato",
        r"no (pidi[oó]|solicit[oó]) ayuda",
        r"no (grit[oó]|emiti[oó] gritos)",
        r"no opuso resistencia",
        r"no presenta signos de violencia f[ií]sica",
        r"su comportamiento no se condice con el de una v[íi]ctima",
        r"conducta provocadora",
        r"se coloc[oó] en situaci[oó]n de riesgo",
        r"pudo haber evitado los hechos",
        r"no resulta cre[ií]ble que una v[íi]ctima",
    ]

    patrones_criticos = [
        r"no es v[aá]lido exigir a la v[íi]ctima",
        r"no puede exigirse a la v[íi]ctima",
        r"no puede sostenerse que.*(por no denunciar de inmediato|por no pedir ayuda)",
        r"no puede considerarse que la falta de denuncia inmediata reste credibilidad",
        r"no puede fundarse la incredulidad en estereotipos",
        r"sin acudir a estereotipos",
        r"evitando estereotipos",
        r"los estereotipos de g[eé]nero no pueden",
    ]

    est = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_estereotipos)
    crit = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_criticos)

    if est == 0 and crit == 0:
        return 60  # neutro

    if est >= 3 and crit == 0:
        return 25  # fuerte sesgo

    if est >= 1 and crit == 0:
        return 35  # cierto sesgo

    if est >= 1 and crit >= 1:
        return 55  # mixto

    if est == 0 and crit >= 1:
        return 80  # muy buen control de estereotipos

    return 50


# =========================================================
#  C10 – FALACIAS Y RAZONAMIENTOS DUDOSOS
# =========================================================

def evaluar_C10(texto: str) -> int:
    """
    C10: Falacias probatorias y razonamientos dudosos.
    Se buscan expresiones típicas de:
      - razonamiento circular,
      - "por el solo hecho de...",
      - inferencias post hoc,
      - generalizaciones abusivas.
    Y se valora positivamente cuando la sentencia dice
    "no basta con..." o "no puede fundarse solo en...".
    """
    patrones_falacias = [
        r"por el solo hecho de",
        r"por el simple hecho de",
        r"basta (para concluir|para tener por acreditado)",
        r"ello demuestra sin m[aá]s",
        r"sin mayor an[aá]lisis",
        r"no cabe duda de que.*por cuanto",
        r"es evidente que.*porque as[ií] lo declara",
    ]

    patrones_correctivos = [
        r"no basta con el solo hecho de",
        r"no puede fundarse [uú]nicamente en",
        r"no puede sostenerse solo en",
        r"no resulta suficiente por s[ií] mismo",
        r"requiere corroboraci[oó]n adicional",
    ]

    fal = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_falacias)
    cor = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_correctivos)

    if fal == 0 and cor == 0:
        return 60  # neutro

    if fal >= 3 and cor == 0:
        return 30  # muchas señales de falacia

    if fal >= 1 and cor == 0:
        return 40  # algunas señales

    if fal >= 1 and cor >= 1:
        return 55  # hay falacias pero también correcciones

    if fal == 0 and cor >= 1:
        return 80  # muy buena actitud crítica

    return 50


# =========================================================
#  C11 – INFERENCIAS AVANZADAS
# =========================================================

def evaluar_C11(texto: str) -> int:
    """
    C11: Inferencias avanzadas y cadena inferencial.
    Evalúa si la sentencia:
      - distingue hechos base, hechos intermedios y conclusión,
      - habla de niveles inferenciales,
      - articula cadenas ("a partir de", "este indicio, unido a...").
    """
    patrones_inferencias = [
        r"hecho intermedio",
        r"hechos intermedios",
        r"hecho consecuencia",
        r"hecho final",
        r"a partir de (estos|tales|los) hechos",
        r"de estos hechos se infiere",
        r"este indicio, unido a",
        r"unido a este otro indicio",
        r"primera inferencia",
        r"segunda inferencia",
        r"primer nivel inferencial",
        r"segundo nivel inferencial",
        r"cadena inferencial",
        r"estructura escalonada",
    ]

    coincidencias = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_inferencias)

    if coincidencias == 0:
        return 30  # no hay trabajo inferencial explícito

    score = 50
    if coincidencias >= 2:
        score += 15
    if coincidencias >= 4:
        score += 15

    return max(30, min(score, 90))


# =========================================================
#  C12 – INTEGRIDAD TEXTUAL Y "RED FLAGS"
# =========================================================

def evaluar_C12(texto: str) -> int:
    """
    C12: Integridad textual y red flags:
      - exceso de doctrina / Acuerdos Plenarios sin referencia al caso concreto,
      - copia/pega teórico sin aplicación,
      - o, por el contrario, buena conexión con "el presente caso", "en autos", etc.
    """
    patrones_doctrina = [
        r"Acuerdo Plenario",
        r"Ferrer Beltr[aá]n",
        r"Taruffo",
        r"Atienza",
        r"Perfecto Andr[eé]s Ib[aá][ñn]ez",
        r"Nieva Fenoll",
        r"doctrina (nacional|comparada)",
        r"jurisprudencia comparada",
    ]

    patrones_concreto = [
        r"en el presente caso",
        r"en el caso concreto",
        r"en autos",
        r"en la presente causa",
        r"en el proceso de autos",
        r"en este proceso penal",
        r"aplicado al caso",
        r"aplicando dicha doctrina al caso",
    ]

    doc = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_doctrina)
    cas = sum(len(re.findall(p, texto, flags=re.I)) for p in patrones_concreto)

    # Escenarios:
    # - Mucha doctrina, casi nada de caso concreto -> red flag (baja nota)
    # - Algo de doctrina y buena referencia al caso -> bien
    # - Casi nada de doctrina pero buena referencia al caso -> muy bien
    # - Nada de ambos -> neutro

    if doc >= 3 and cas == 0:
        return 35  # doctrinalista sin aplicación clara

    if doc >= 1 and cas >= 1:
        return 65  # se cita doctrina y se aplica

    if doc == 0 and cas >= 2:
        return 80  # muy centrado en el caso concreto

    if doc == 0 and cas == 0:
        return 60  # neutro

    # Escenario residual
    return 55


# =========================================================
#  CÁLCULO DEL ICI GLOBAL (C1–C12)
# =========================================================

def calcular_ici_sin_penalizacion(c: Dict[str, int]) -> float:
    """
    Pesos ajustados para C1–C12. Suman exactamente 1.0.
    Se privilegia:
      - estructura básica (C1–C7),
      - máximas de experiencia (C8),
      - sin dejar de lado control de sesgos/falacias (C9–C12).
    """
    pesos = {
        "C1": 0.10,
        "C2": 0.10,
        "C3": 0.07,
        "C4": 0.07,
        "C5": 0.16,  # hipótesis alternativas sigue siendo clave
        "C6": 0.10,
        "C7": 0.10,
        "C8": 0.10,
        "C9": 0.07,
        "C10": 0.06,
        "C11": 0.04,
        "C12": 0.03,
    }

    ici = sum(c[k] * pesos[k] for k in pesos)
    return round(ici, 2)


def aplicar_penalizacion_c5(ici_base: float, c5: int) -> float:
    """
    Penalización especial cuando C5 (hipótesis alternativas) es bajo.
    """
    if c5 >= 40:
        return round(ici_base, 2)

    penalizacion_max = 15.0
    factor = (40 - c5) / 40.0
    ici_ajustado = ici_base - penalizacion_max * factor
    return round(max(0, ici_ajustado), 2)


def interpretar_ici(ici_ajustado: float,
                    c5: int, c7: int, c8: int, c9: int, c10: int, c11: int, c12: int) -> str:
    """
    Interpretación cualitativa global.
    """
    if ici_ajustado < 40:
        return (
            "Riesgo MUY ALTO: la coherencia indiciaria es deficiente. "
            "El razonamiento presenta serias lagunas en la estructura de indicios y en el "
            "tratamiento de hipótesis alternativas, con uso insuficiente de reglas de "
            "experiencia y posible presencia de sesgos o falacias relevantes."
        )
    elif ici_ajustado < 55:
        return (
            "Riesgo ALTO: la motivación presenta fallas relevantes. "
            "Aunque se identifican algunos elementos indiciarios, el descarte de hipótesis "
            "alternativas y/o el uso de máximas de la experiencia resulta insuficiente, y "
            "se aprecian debilidades en el control de sesgos, falacias o en la aplicación "
            "concreta de la doctrina al caso."
        )
    elif ici_ajustado < 70:
        return (
            "Riesgo MEDIO: motivación aceptable pero incompleta. "
            "Se aprecian indicios y cierta lógica inferencial, pero existen debilidades en la "
            "convergencia, en el análisis de hipótesis alternativas o en el uso explícito de "
            "reglas de experiencia, así como en el control sistemático de sesgos y falacias."
        )
    elif ici_ajustado < 85:
        return (
            "Riesgo BAJO: razonamiento indiciario sólido en general. "
            "La sentencia identifica hechos base, analiza fuentes, descarta hipótesis "
            "alternativas y utiliza reglas de experiencia de forma razonable, con un nivel "
            "aceptable de control de sesgos, falacias y una aplicación suficiente de la "
            "doctrina al caso concreto."
        )
    else:
        return (
            "Estándar ALTO de coherencia indiciaria: la motivación sigue un método claro, "
            "con hechos base definidos, fuentes analizadas, pluralidad y convergencia real "
            "de indicios, hipótesis alternativas tratadas rigurosamente, uso consistente de "
            "máximas de la experiencia y un control explícito de estereotipos, falacias y "
            "aplicación cuidadosa de la doctrina al caso concreto."
        )


# =========================================================
#  FUNCIÓN PRINCIPAL
# =========================================================

def evaluar_texto(texto: str) -> Dict[str, object]:
    """
    Evalúa el texto y devuelve:
      - C1–C12
      - ICI_sin_penalizacion
      - ICI_ajustado
      - interpretación cualitativa
    """
    texto_norm = re.sub(r"\s+", " ", texto or "")

    criterios = {
        "C1": evaluar_C1(texto_norm),
        "C2": evaluar_C2(texto_norm),
        "C3": evaluar_C3(texto_norm),
        "C4": evaluar_C4(texto_norm),
        "C5": evaluar_C5(texto_norm),
        "C6": evaluar_C6(texto_norm),
        "C7": evaluar_C7(texto_norm),
        "C8": evaluar_C8(texto_norm),
        "C9": evaluar_C9(texto_norm),
        "C10": evaluar_C10(texto_norm),
        "C11": evaluar_C11(texto_norm),
        "C12": evaluar_C12(texto_norm),
    }

    ici_sin = calcular_ici_sin_penalizacion(criterios)
    ici_aj = aplicar_penalizacion_c5(ici_sin, criterios["C5"])
    interpretacion = interpretar_ici(
        ici_aj,
        criterios["C5"],
        criterios["C7"],
        criterios["C8"],
        criterios["C9"],
        criterios["C10"],
        criterios["C11"],
        criterios["C12"],
    )

    return {
        "criterios": criterios,
        "ICI_sin_penalizacion": ici_sin,
        "ICI_ajustado": ici_aj,
        "interpretacion": interpretacion,
    }
