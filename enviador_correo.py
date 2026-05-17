import win32com.client as win32

def enviar_por_outlook(html_cuerpo, destinatarios, asunto="Newsletter Técnico: Lo último en automatización y desarrollo"):
    try:
        # Conectar a la instancia de Outlook que ya está abierta en tu PC
        outlook = win32.Dispatch('outlook.application')
        correo = outlook.CreateItem(0) # 0 = MailItem
        
        correo.To = destinatarios
        correo.Subject = asunto
        correo.HTMLBody = html_cuerpo
        
        # Opcional: Si tienes varias cuentas en Outlook y quieres forzar 
        # que salga por equiroz@sclconsultores.com, descomenta estas líneas:
        # for cuenta in outlook.Session.Accounts:
        #     if cuenta.SmtpAddress == "equiroz@sclconsultores.com":
        #         correo.SendUsingAccount = cuenta
        #         break

        # MODO DE PRUEBA: .Display() abrirá la ventana del correo para que lo veas.
        # Cuando valides que todo está perfecto, cambia .Display() por .Send() para que sea 100% automático.
        # correo.Display() 
        correo.Send() 
        
        print(f"Correo preparado en Outlook para: {destinatarios}")
        return True

    except Exception as e:
        print(f"Error al intentar conectar con Outlook local: {e}")
        return False