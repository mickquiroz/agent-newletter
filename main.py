from extractor import FEEDS, obtener_noticias_recientes
from processor import clasificar_y_seleccionar_top_3
from generador_html import generar_html_newsletter
from enviador_correo import enviar_por_outlook 

def ejecutar_pipeline():
    print("Iniciando pipeline de Newsletter Tech para SCL Consultores...")
    
    noticias = obtener_noticias_recientes(FEEDS, horas_limite=48)
    print(f"Se encontraron {len(noticias)} noticias en las últimas 48 horas.\n")
    
    if not noticias:
        print("No hay noticias para procesar. Abortando pipeline.")
        return

    print("Enviando a Ollama para clasificación. Esto puede demorar...")
    resultado_final_json = clasificar_y_seleccionar_top_3(noticias)
    
    if "error" in resultado_final_json:
        print(f"Error en la IA: {resultado_final_json['error']}")
        return

    print("Generando plantilla HTML con imágenes Base64 y enlaces...")
    codigo_html_final = generar_html_newsletter(resultado_final_json)
    
    print("Conectando con Outlook...")
    
    lista_destinatarios = "equiroz@sclconsultores.com" 
    
    envio_exitoso = enviar_por_outlook(
        html_cuerpo=codigo_html_final, 
        destinatarios=lista_destinatarios,
        asunto="Top 3 Noticias Tech para el Equipo SCL"
    )

    if envio_exitoso:
        print("¡Pipeline ejecutado con éxito total! Revisa tu Outlook.")
    else:
        print("El pipeline terminó, pero hubo un problema enviando el correo.")

if __name__ == "__main__":
    ejecutar_pipeline()