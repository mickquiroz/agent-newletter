import base64
import os

def obtener_imagen_base64(ruta_archivo, tipo_mime="image/png"):
    if not os.path.exists(ruta_archivo):
        print(f"Advertencia: No se encontró la imagen en {ruta_archivo}")
        return ""
        
    with open(ruta_archivo, "rb") as archivo_imagen:
        cadena_codificada = base64.b64encode(archivo_imagen.read()).decode('utf-8')
        return f"data:{tipo_mime};base64,{cadena_codificada}"

def generar_html_newsletter(datos_ia):
    logo_scl_b64 = obtener_imagen_base64("image/scl-icon.png", "image/png")
    logo_ollama_b64 = obtener_imagen_base64("image/ollama-icon.png", "image/png")

    # Todo envuelto en una gran tabla 100% que hace de fondo gris
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f6f8fa; font-family: Arial, Helvetica, sans-serif;">
        
        <table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f6f8fa" style="background-color: #f6f8fa;">
            <tr>
                <td align="center" valign="top" style="padding: 40px 20px;">
                    
                    <table width="800" border="0" cellspacing="0" cellpadding="0" bgcolor="#ffffff" style="width: 100%; max-width: 800px; background-color: #ffffff; border: 1px solid #e1e4e8;">
                        
                        <tr>
                            <td align="center" style="padding: 30px 30px 20px 30px; border-bottom: 1px solid #eaecef;">
                                <h2 style="color: #24292e; font-size: 24px; margin: 0 0 5px 0; font-family: Arial, sans-serif;">
                                    <img src="{logo_scl_b64}" alt="SCL Consultores" height="35" style="vertical-align: middle; margin-right: 10px;"> 
                                    Newsletter Técnico
                                </h2>
                                <p style="color: #586069; font-size: 14px; margin: 0; font-family: Arial, sans-serif;">Lo más relevante de las últimas 48 horas para el equipo</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 20px 30px 10px 30px;">
    """

    noticias = datos_ia.get("top_3", [])

    for noticia in noticias:
        titulo = noticia.get("titulo", "Sin título")
        categoria_badge = noticia.get("categoria_principal", "GENERAL")
        resumen = noticia.get("resumen_corto", "")
        link = noticia.get("link", "#")
        
        html += f"""
                                <div style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f0;">
                                    
                                    <table border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 12px;">
                                        <tr>
                                            <td bgcolor="#0366d6" align="center" style="background-color: #0366d6; padding: 6px 12px; border-radius: 12px; font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; color: #ffffff; text-transform: uppercase;">
                                                {categoria_badge}
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <h3 style="margin: 0 0 10px 0; font-size: 18px; line-height: 1.4; font-family: Arial, sans-serif;">
                                        <a href="{link}" target="_blank" style="color: #24292e; text-decoration: none; font-weight: bold;">
                                            {titulo}
                                        </a>
                                    </h3>
                                    <p style="color: #444d56; font-size: 14px; line-height: 1.6; margin: 0; font-family: Arial, sans-serif;">
                                        {resumen}
                                    </p>
                                </div>
        """

    html += f"""
                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="padding: 10px 30px 30px 30px;">
                                <p style="color: #959da5; font-size: 12px; margin: 0; font-family: Arial, sans-serif;">
                                    Generado automáticamente por nuestro sistema de RPA + IA (Ollama)
                                    <img src="{logo_ollama_b64}" alt="Ollama" width="16" height="16" style="vertical-align: middle; margin-left: 4px;">
                                </p>
                            </td>
                        </tr>

                    </table>
                    </td>
            </tr>
        </table>
        </body>
    </html>
    """
    
    return html

"""
# --- PRUEBA CON DATOS QUE INCLUYEN ENLACES ---
datos_ejemplo = {
    'top_3': [
        {
            'titulo': 'Ubuntu Embraces Local AI Instead of Cloud-First OS Integration', 
            'link': 'https://www.darkreading.com/ejemplo-ubuntu',
            'categoria_principal': 'Automatización (RPA, Scripts, Workflows)', 
            'resumen_corto': 'Noticia destacando la estrategia de Ubuntu para centrarse en inteligencia localizada y modulares diseños.'
        }, 
        {
            'titulo': 'Google Introduces Cloud Fraud Defense as Successor to reCAPTCHA', 
            'link': 'https://feed.infoq.com/ejemplo-google',
            'categoria_principal': 'Seguridad (Ciberseguridad, DevSecOps, Vulnerabilidades)', 
            'resumen_corto': 'Anuncio de Google sobre su nuevo sistema para defender contra el fraude en línea.'
        }, 
        {
            'titulo': 'Microsoft Releases Aspire 13.3 with Major Deployment and Frontend Updates', 
            'link': 'https://huggingface.co/blog/ejemplo-microsoft',
            'categoria_principal': 'Arquitectura de software (Diseño de sistemas, Escalabilidad)', 
            'resumen_corto': 'Actualización importante para Microsoft con nuevos comandos y mejoras en la publicación frontal.'
        }
    ]
}

codigo_html_final = generar_html_newsletter(datos_ejemplo)

with open("vista_previa_correo.html", "w", encoding="utf-8") as f:
    f.write(codigo_html_final)
"""