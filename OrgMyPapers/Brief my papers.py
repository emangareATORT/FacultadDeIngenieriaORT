import os
import json
import requests
import PyPDF2

# Ajusta estos parámetros a tu entorno
PDF_FOLDER = r"C:\Users\eduar\OneDrive - Universidad ORT Uruguay\__Papers and Reports\Demo"
GPT4_MINI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")

def obtener_primer_pagina_pdf(ruta_pdf):
    """Lee y retorna el texto de la primera página de un PDF."""
    with open(ruta_pdf, "rb") as f:
        lector = PyPDF2.PdfReader(f)
        if len(lector.pages) > 0:
            primera_pagina = lector.pages[0].extract_text()
            return primera_pagina.strip()
    return ""

def obtener_resumen_gpt4(texto):
    """
    Envía la solicitud a la API de GPT-4 mini (o similar) para obtener un resumen.
    Se retorna el resumen completo obtenido.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "gpt-4o-mini-2024-07-18",  # Verifica que el nombre del modelo sea el correcto, por ejemplo "gpt-4o-mini"
        "messages": [
            {"role": "system", "content": "Eres un asistente que resume textos."},
            {"role": "user", "content": f"Resume el siguiente texto:\n{texto}"}
        ],
        "max_tokens": 100
    }
    response = requests.post(GPT4_MINI_API_ENDPOINT, headers=headers, json=payload)
    response_json = response.json()

    if "choices" in response_json and len(response_json["choices"]) > 0:
        return response_json["choices"][0]["message"]["content"].strip()
    return ""

def crear_resumenes_json():
    resultado = []
    for archivo in os.listdir(PDF_FOLDER):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(PDF_FOLDER, archivo)
            texto_primer_pagina = obtener_primer_pagina_pdf(ruta_pdf)

            if texto_primer_pagina:
                resumen = obtener_resumen_gpt4(texto_primer_pagina)
                # Imprime en la consola el resumen completo obtenido para cada archivo
                print(f"Resumen obtenido para {archivo}:\n{resumen}\n")
                resultado.append({
                    "nombre_articulo": archivo,
                    "link_archivo": ruta_pdf,
                    "resumen": resumen
                })

    with open("resumenes.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    crear_resumenes_json()
