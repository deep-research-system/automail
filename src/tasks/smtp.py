import smtplib
import imaplib
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid


def send_smtp_tool(state: dict) -> dict:
    from_mail = state["from_mail"]
    app_password = state["app_password"]
    to_mail = state["to_mail"]

    title = state["title"]       # LLM 초안 제목
    context = state["context"]   # LLM 초안 본문
    files = state["files"]       # 첨부파일명

    # 1) 메일 컨테이너 (본문 + 첨부)
    msg = MIMEMultipart()
    msg["Subject"] = title
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()

    # 2) 본문
    msg.attach(MIMEText(context, _charset="utf-8"))

    # 3) 첨부파일 (무조건 1개, 문자열 경로)
    file_path = Path(files)
    with open(file_path, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="octet-stream")
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=file_path.name,
        )
        msg.attach(part)

    # 4) SMTP 전송
    with smtplib.SMTP_SSL("smtp.daum.net", 465) as server:
        server.login(from_mail, app_password)
        server.send_message(msg)

    # 5) 보낸편지함 저장 (IMAP APPEND)
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
        "title": title,
        "file": file_path.name,
    }
