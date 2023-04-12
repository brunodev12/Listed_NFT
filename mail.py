import smtplib
import os

password = os.environ.get('PASSWORD')
FROM = os.environ.get('FROM')
TO = os.environ.get('TO')

def send_email(_message= "Prueba", _subject='Test'):
    message = _message
    subject = _subject

    message = 'Subject: {}\n\n{}'.format(subject, message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, password)

    server.sendmail(FROM, TO, message)

    server.quit()
