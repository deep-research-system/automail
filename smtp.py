import smtplib
from email.mime.text import MIMEText

def send_smtp(state: dict):
    EMAIL = state["from_mail"]
    PASSWORD = state["app_password"]
    TO_MAIL = state["to_mail"]

    SMTP_SERVER = "smtp.daum.net"
    SMTP_PORT = 465

    msg = MIMEText("다음 SMTP 테스트 메일입니다.")
    msg["Subject"] = "SMTP 테스트"
    msg["From"] = EMAIL
    msg["To"] = TO_MAIL

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

    print(f"메일 전송 성공 → {TO_MAIL}")
