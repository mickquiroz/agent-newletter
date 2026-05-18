import win32com.client as win32

def enviar_por_outlook(html_cuerpo, destinatarios, asunto="Newsletter Técnico: Lo último en automatización y desarrollo"):
    try:
        outlook = win32.Dispatch('outlook.application')
        correo = outlook.CreateItem(0) 
        
        correo.To = destinatarios
        correo.Subject = asunto
        correo.HTMLBody = html_cuerpo
         
        correo.Send() 
        
        print(f"Correo preparado en Outlook para: {destinatarios}")
        return True

    except Exception as e:
        print(f"Error al intentar conectar con Outlook local: {e}")
        return False