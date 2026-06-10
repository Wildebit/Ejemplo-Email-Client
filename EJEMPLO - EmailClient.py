import poplib
import smtplib
from email.mime.text import MIMEText
from email.parser import BytesParser
from email.policy import default

from email_rate_limit import throttle_email_send
from mail_config import EMAIL_PASSWORD, EMAIL_USER, POP3_PORT, POP3_SERVER, SMTP_PORT, SMTP_SERVER


def enviar_correo(from_email, _password, to_email, message):
    try:
        throttle_email_send()
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = "Nova reserva: Francesco De Luca Bosso - 9-16 agost 2025"
        msg["From"] = from_email
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.login(from_email, _password)
            server.sendmail(from_email, [to_email], msg.as_string())
        print(f"[OK] Enviado desde: {from_email} a {to_email}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar desde {from_email}: {e}")


def leer_mails(_email, _password):
    server = None
    try:
        server = poplib.POP3(POP3_SERVER, POP3_PORT, timeout=10)
        server.user(_email)
        server.pass_(_password)

        num_messages = len(server.list()[1])
        print(f"[INFO] {_email} tiene {num_messages} mensajes.")

        if num_messages > 0:
            response, lines, octets = server.retr(num_messages)
            msg_content = b"\r\n".join(lines)
            msg = BytesParser(policy=default).parsebytes(msg_content)
            print(f"    Último asunto recibido: {msg['subject']}")
    except Exception as e:
        print(f"[ERROR] No se pudo leer desde {_email}: {e}")
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass


email = EMAIL_USER
password = EMAIL_PASSWORD

enviar_correo(email, password, to_email="destination@example.com", message="Hello World!")
leer_mails(email, password)
