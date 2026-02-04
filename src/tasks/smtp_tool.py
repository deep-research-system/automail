import smtplib
import imaplib
import time
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid


def send_smtp_tool(state: dict) -> dict:
    from_mail = state["from_mail"]
    app_password = state["app_password"]
    to_mail = state["to_mail"]

    title = state["title"]   # ← LLM 초안 제목
    context = state["context"]         # ← LLM 초안 본문

    # 1) SMTP 전송
    msg = MIMEText(context, _charset="utf-8")
    msg["Subject"] = title
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()

    with smtplib.SMTP_SSL("smtp.daum.net", 465) as server:
        server.login(from_mail, app_password)
        server.send_message(msg)

    # 2) 보낸편지함 저장 (IMAP APPEND)
    raw_bytes = msg.as_bytes()

    with imaplib.IMAP4_SSL("imap.daum.net", 993) as imap:
        imap.login(from_mail, app_password)
        imap.append(
            "Sent",
            None,
            imaplib.Time2Internaldate(time.time()),
            raw_bytes,
        )
        imap.logout()

    return {
        "ok": True,
        "to_mail": to_mail,
        "subject": title,
    }
