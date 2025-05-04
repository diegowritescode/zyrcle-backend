import requests 

GEMINI_API_KEY = "REDACTED_SET_GEMINI_API_KEY_IN_ENV"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def optimize_route_with_gemini(containers, user_location):
    prompt = generate_prompt(containers, user_location)

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()
        text_response = reply["candidates"][0]["content"]["parts"][0]["text"]
        print("Respuesta Gemini:", text_response)  # 👈 Verifica esto
        return parse_ids_from_response(reply["candidates"][0]["content"]["parts"][0]["text"])
    else:
        raise Exception(f"Error en la API Gemini: {response.status_code}, {response.text}")

def generate_prompt(containers, user_location):
    return f"""
Dado el siguiente listado de contenedores de reciclaje en Medellín con su ubicación, tipo, peso estimado y porcentaje de llenado, y la ubicación del recolector, responde una lista de IDs ordenados desde el más cercano y necesario de recolectar hasta el último.

Ubicación del recolector:
Latitud: {user_location['latitude']}, Longitud: {user_location['longitude']}

Contenedores:
{format_containers(containers)}

Solo responde una lista JSON como esta: [8, 3, 6, 1]
"""

def format_containers(containers):
    return "\n".join(
        f"ID: {c.id}, Tipo: {c.type}, Peso: {c.estimatedWeight}, Llenado: {c.fillPercentage}%, Lat: {c.latitude}, Lon: {c.longitude}"
        for c in containers
    )

def parse_ids_from_response(text):
    import json, re

    try:
        # Quitar markdown ```json ... ``` si existe
        cleaned = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()

        # Parsear directamente como JSON
        return json.loads(cleaned)
    except Exception as e:
        print("❌ Error al parsear JSON:", e)
        return []
