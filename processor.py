import json
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

def clasificar_y_seleccionar_top_3(noticias_recientes):
    if not noticias_recientes:
        return {"error": "No hay noticias recientes para analizar."}

    datos_noticias = json.dumps(noticias_recientes, indent=2, ensure_ascii=False)

    prompt_sistema = """
    Eres un Editor Técnico Experto para un equipo de Ingeniería de Software.
    Tu tarea es analizar una lista de noticias tecnológicas y seleccionar estrictamente las 3 más relevantes.
    
    CRITERIOS DE PRIORIDAD (del más importante al menos importante):
    1. Automatización (RPA, Scripts, Workflows)
    2. Inteligencia Artificial (LLMs, Agentes, ML)
    3. Seguridad (Ciberseguridad, DevSecOps, Vulnerabilidades)
    4. Arquitectura de software (Diseño de sistemas, Escalabilidad)
    5. Python
    6. Frontend
    7. Backend
    
    INSTRUCCIONES:
    - Evalúa las noticias basándote en los criterios de prioridad.
    - Selecciona el TOP 3.
    - Redacta un mensaje corto y directo en ESPAÑOL explicando por qué es importante.
    - Extrae el valor de "link" de la noticia original y ponlo en tu respuesta.
    - TU RESPUESTA DEBE SER ÚNICAMENTE UN OBJETO JSON VÁLIDO. No incluyas texto fuera del JSON.
    
    FORMATO JSON REQUERIDO:
    {
      "top_3": [
        {
          "titulo": "Título original de la noticia",
          "link": "El enlace (URL) extraído de la noticia original",
          "categoria_principal": "La categoría de la lista de prioridades que cumple",
          "resumen_corto": "Resumen técnico y corto en español de 2 líneas"
        }
      ]
    }
    """

    prompt_usuario = f"Aquí están las noticias de las últimas 48 horas:\n{datos_noticias}\n\nDevuelve únicamente el JSON con el Top 3."

    ip_servidor = os.getenv("IP_SERVIDOR", "127.0.0.1") 
    url_api = f"http://{ip_servidor}:11434/api/generate"
    
    payload = {
        "model": "llama3",
        "system": prompt_sistema,
        "prompt": prompt_usuario,
        "stream": False,
        "format": "json", 
        "options": {
            "temperature": 0.1, 
            "top_p": 0.9
        }
    }

    try:
        respuesta = requests.post(url_api, json=payload, timeout=720)
        respuesta.raise_for_status()
        
        datos_ollama = respuesta.json()
        texto_generado = datos_ollama.get("response", "")
        
        texto_limpio = texto_generado.strip()
        
        if texto_limpio.startswith("```json"):
            texto_limpio = texto_limpio.replace("```json", "", 1)
            
        if texto_limpio.endswith("```"):
            texto_limpio = re.sub(r'```$', '', texto_limpio)
        
        resultado_json = json.loads(texto_limpio.strip())
        
        if "top_3" in resultado_json:
            for noticia_ia in resultado_json["top_3"]:
                link_ia = noticia_ia.get("link", "")
                
                for noticia_original in noticias_recientes:
                    if noticia_original.get("link") == link_ia:
                        noticia_ia["imagen"] = noticia_original.get("imagen", "")
                        break

        return resultado_json

    except requests.exceptions.Timeout:
        return {"error": "El servidor de Ollama tardó demasiado y la conexión se cerró (Timeout)."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexión con Ollama: {str(e)}"}
    except json.JSONDecodeError:
        return {
            "error": "Ollama no devolvió un JSON válido.", 
            "texto_crudo": texto_generado
        }