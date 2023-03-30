import smtplib
import os
from decouple import config

#password = os.environ.get('EMAIL_PASSWORD')
password = config('PASSWORD')
FROM = config('FROM')
TO = config('TO')

def send_email(mensaje="Prueba"):
    message = mensaje
    subject = 'Unclaimed NFTs found'

    message = 'Subject: {}\n\n{}'.format(subject, message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, password)

    server.sendmail(FROM, TO, message)

    server.quit()