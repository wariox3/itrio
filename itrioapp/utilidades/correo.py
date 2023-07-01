from decouple import config 
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

class Correo():

    def __init__(self):
        self.sg = SendGridAPIClient(config('KEY_SENDGRID'))

    def enviar(self, email, asunto, contenido):                      
        message = Mail(
            from_email='tisemantica@gmail.com',
            to_emails=email,
            subject=asunto,
            html_content=contenido)
        respuesta = self.sg.send(message)
        return respuesta   
