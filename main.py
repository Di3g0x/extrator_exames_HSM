from flask import Flask, render_template, request
import re

app = Flask(__name__)


def normalizar(texto):
    return texto.replace(" ", "").upper()


def extrair_valor_apos_chave(texto, chave):
    chave_normalizada = normalizar(chave)
    linhas = texto.splitlines()
    for linha in linhas:
        if normalizar(linha).find(chave_normalizada) != -1:
            pos_dois_pontos = linha.find(":")
            if pos_dois_pontos != -1:
                valor = linha[pos_dois_pontos + 1:].strip(" -_\t\r\n")
                return valor
    return None


def extrair_data_hora(texto):
    return extrair_valor_apos_chave(texto, "Data/hora Coleta")


def extrair_exames(texto):
    exames = {
        "DOSAGEM DE URÉIA": "UR",
        "DOSAGEM DE CREATININA": "CR",
        "TAXA DE FILTRAÇÃO GLOMERULAR ESTIMADA": "TFG",
        "DOSAGEM DE SÓDIO": "NA",
        "DOSAGEM DE POTÁSSIO": "K",
        "DOSAGEM DE CLORO": "CL",
        "DOSAGEM DE CALCIO": "CA",
        "DOSAGEM DE MAGNÉSIO": "MG",
        "DOSAGEM DE FÓSFORO": "P",
        "DOSAGEM DE FERRO": "FE",
        "FERRO SÉRICO": "FE",
        "FERRITINA": "FERRITINA",
        "PROTEINAS TOTAIS ....": "PT",
        "ALBUMINA": "ALB",
        "GLOBULINAS": "GLOB",
        "RELAÇÃO ALBUMINA/GLOBULINA": "Alb/Glob",
        "BILIRRUBINA DIRETA": "BD",
        "BILIRRUBINA INDIRETA": "BI",
        "DOSAGEM DE FOSFATASE ALCALINA (ALP)": "FA",
        "DOSAGEM DE TRANSAMINASE PIRÚVICA (ALT)": "ALT",
        "DOSAGEM DE TRANSAMINASE OXALACÉTICA (AST)": "AST",
        "DOSAGEM DE GAMA GLUTAMIL TRANSFERASE (GGT)": "GGT",
        "DOSAGEM DE DESIDROGENASE LÁCTICA (DHL)": "DHL",
        "DOSAGEM DE AMILASE": "AMILASE",
        "DOSAGEM DE LIPASE": "LIPASE",
        "DOSAGEM DE PROTEINA C REATIVA (PCR)": "PCR",
        "DOSAGEM DE LACTATO": "LAC",
        "INR": "INR",
        "TEMPO DE TROMB. PARC. ATIVADA (TTPA)": "TTPA",
        "RTTPA": "RTTPA",
        "ATIVIDADE DE PROTROMBINA (TAP)": "TAP",
        "DOSAGEM DE GLICOSE": "GLIC",
        "SOROLOGIA PARA SÍFILIS (REAÇÃO DO VDRL)": "VDRL",
        "DOSAGEM DE TRIGLICÉRIDES": "TG",
        "DOSAGEM DE COLESTEROL": "COLESTEROL",
        "DOSAGEM DE HDL COLESTEROL": "HDL",
        "DOSAGEM DE VITAMINA B12": "B12",
        "VITAMINA D-25 HIDROXI": "VIT D",
        "DOSAGEM DE TIROXINA LIVRE (FT4)": "FT4",
        "DOSAGEM DE HORMÔNIO TIREO ESTIMULANTE (TSH)": "TSH",
        "DOSAGEM DE HEMOGLOBINA GLICADA": "HbA1c",
        "DOSAGEM DE CORTISOL SÉRICO": "CORTISOL",
        "DOSAGEM ANTÍGENO CARCINOEMBRIOGENICO-(CEA)": "CEA",
        "DOSAGEM DO ANTÍGENO CA 125": "CA 125",
        "DOSAGEM DO ANTÍGENO CA 19/9": "CA 19/9",
        "DOSAGEM DE CÁLCIO IONIZADO": "CaIO",
        "TESTE DE GRAVIDEZ": "GRAVIDEZ",
        "HEPATITE B (HBsAg)": "HBsAg",
        "ANTIC ANTI VIRUS DA HEPATITE C (Anti HCV)": "Anti HCV",
        "PESQUISA DE ANTICORPOS ANTI HIV-1/HIV-2": "HIV",
        "DOSAGEM DE TROPONINA I(Sensibilidade elevada)": "TROPONINA",
        "DOSAGEM DE CREATINA FOSFOQUINASE (CK)": "CK",
        "VELOCIDADE DE HEMOSSEDIMENTAÇÃO (VHS)": "VHS",

    }

    resultados = []
    for chave, sigla in exames.items():
        valor = extrair_valor_apos_chave(texto, chave)
        if valor:
            resultados.append(f"{sigla}: {valor}")
    return " | ".join(resultados)


def extrair_gasometria(texto):
    if "GASOMETRIA ARTERIAL" not in texto.upper():
        return None
    padroes = {
        "PH": r"PH\s*[:\-.]*\s*([0-9.,]+)",
        "pCO2": r"PCO2\s*(?:\(.*?\))?\s*[:\-.]*\s*([0-9.,]+)",
        "BIC": r"(?:CHCO3\(P\)C|HCO3|BICARBONATO)\s*[:\-.]*\s*([0-9.,]+)",
        "pO2": r"PO2\s*(?:\(.*?\))?\s*[:\-.]*\s*([0-9.,]+)",
        "SO2": r"SO2\s*(?:\(.*?\))?\s*[:\-.]*\s*([0-9.,%]+)"
    }
    resultados = []
    for sigla, regex in padroes.items():
        match = re.search(regex, texto, re.IGNORECASE)
        if match:
            valor = match.group(1).strip(" -_\t\r\n")
            resultados.append(f"{sigla} {valor}")
        else:
            resultados.append(f"{sigla} ''")
    return f"GASOA({'; '.join(resultados)})"


def extrair_gasometriaV(texto):
    if "GASOMETRIA VENOSA" not in texto.upper():
        return None
    padroes = {
        "PH": r"PH\s*[:\-.]*\s*([0-9.,]+)",
        "pCO2": r"PCO2\s*(?:\(.*?\))?\s*[:\-.]*\s*([0-9.,]+)",
        "BIC": r"(?:CHCO3\(P\)C|HCO3|BICARBONATO)\s*[:\-.]*\s*([0-9.,]+)",
        "pO2": r"PO2\s*(?:\(.*?\))?\s*[:\-.]*\s*([0-9.,]+)",
        "SO2": r"SO2\s*(?:\(.*?\))?\s*[:\-.]*\s*([0-9.,%]+)"
    }
    resultados = []
    for sigla, regex in padroes.items():
        match = re.search(regex, texto, re.IGNORECASE)
        if match:
            valor = match.group(1).strip(" -_\t\r\n")
            resultados.append(f"{sigla} {valor}")
        else:
            resultados.append(f"{sigla} ''")
    return f"GASOV({'; '.join(resultados)})"


def extrair_CKMB(texto):
    if "DOSAGEM DA ISOENZIMA DA CREATINA QUINASE (CK-MB MASSA)" not in texto.upper():
        return None
    padroes = {
        "CKMB": r"Resultado\s*[:\-.]*\s*([0-9.,]+)"
    }
    resultados = []
    for sigla, regex in padroes.items():
        match = re.search(regex, texto, re.IGNORECASE)
        if match:
            valor = match.group(1).strip(" -_\t\r\n")
            resultados.append(f"{sigla} {valor}")
        else:
            resultados.append(f"{sigla} ''")
    return f"{''.join(resultados)}"


def extrair_URINA1(texto):
    if "ANÁLISE DE URINA" not in texto.upper():
        return None

    padroes = {
        "Aspecto:": "Aspecto",
        "Cor:": "Cor",
        "Ph:": "ph",
        "Proteínas:": "Proteínas",
        "Glicose:": "Glicose",
        "Corpos Cetônicos:": "Corpos Cetônicos",
        "Hemoglobina Livre:": "Hemoglobina Livre",
        "Nitritos:": "Nitritos",
        "Leucócitos:": "Leucócitos",
        "Hemácias:": "Hemácias",
        "Filamentos de muco:": "Filamentos de muco",
        "Cilindros:": "Cilindros",
    }

    resultados = []

    linhas = texto.splitlines()
    linhas_normalizadas = [normalizar(l) for l in linhas]

    for sigla, termo in padroes.items():
        termo_norm = normalizar(termo)
        valor = "''"
        for i, linha_norm in enumerate(linhas_normalizadas):
            if termo_norm in linha_norm:
                linha_original = linhas[i]

                # Tenta extrair número com ponto ou vírgula (como milhar ou decimal)
                match_num = re.search(r":\s*[-_]*\s*([\d.,]+)", linha_original)
                if match_num:
                    valor = match_num.group(1).strip(" -_\t\r\n")
                else:
                    # Se não for número, extrai texto até muitos pontos ou espaços
                    match_txt = re.search(r":\s*[-_]*\s*(.+?)(?:\s{2,}|\.{3,})", linha_original)
                    if match_txt:
                        valor = match_txt.group(1).strip(" -_\t\r\n")
                break

        resultados.append(f"{sigla} {valor}")

    return f"URINA( {' | '.join(resultados)})"


def extrair_hemograma(texto):
    if "HEMOGRAMA COMPLETO" not in texto.upper():
        return None

    padroes = {
        "HB": "Hemoglobina",
        "HT": "Hematocrito",
        "Leuco": "Leucócitos",
        "Plaq": "Plaquetas"
    }

    resultados = []

    linhas = texto.splitlines()
    linhas_normalizadas = [normalizar(l) for l in linhas]

    for sigla, termo in padroes.items():
        termo_norm = normalizar(termo)
        valor = "''"
        for i, linha_norm in enumerate(linhas_normalizadas):
            if termo_norm in linha_norm:
                match = re.search(r":\s*[-_]*\s*([0-9.,]+)", linhas[i])
                if match:
                    valor = match.group(1).strip(" -_\t\r\n")
                break
        resultados.append(f"{sigla} {valor}")

    return f"HMG({'; '.join(resultados)})"


@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ''
    if request.method == 'POST':
        texto = request.form['texto']
        saida = []

        data_hora = extrair_data_hora(texto)
        exames_formatados = extrair_exames(texto)
        CKMB_formatado = extrair_CKMB(texto)
        gaso_formatado = extrair_gasometria(texto)
        gasoV_formatado = extrair_gasometriaV(texto)
        HMG_formatado = extrair_hemograma(texto)
        urina1_formatado = extrair_URINA1(texto)

        if data_hora:
            linha = f"({data_hora})"
            if exames_formatados:
                linha += f": {exames_formatados}"
            saida.append(linha)

        if CKMB_formatado:
            saida.append(CKMB_formatado)

        if gaso_formatado:
            saida.append(gaso_formatado)

        if gasoV_formatado:
            saida.append(gasoV_formatado)

        if HMG_formatado:
            saida.append(HMG_formatado)

        if urina1_formatado:
            saida.append(urina1_formatado)

        resultado = " | ".join(saida)
    return render_template('index.html', resultado=resultado)


if __name__ == '__main__':
    app.run()


