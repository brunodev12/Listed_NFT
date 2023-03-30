import smtplib
import os

password = os.environ.get('PASSWORD')
FROM = os.environ.get('FROM')
TO = os.environ.get('TO')

def send_email(mensaje="Prueba"):
    message = mensaje
    subject = 'Unclaimed NFTs found'

    message = 'Subject: {}\n\n{}'.format(subject, message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, password)

    server.sendmail(FROM, TO, message)

    server.quit()
