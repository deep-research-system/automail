import smtplib
import imaplib
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid


def send_smtp(state: dict) -> dict:
    # state에서 필요한 값만 한 번 꺼내서 통일
    from_mail = state["from_mail"]
    to_mail = state["to_mail"]
    app_password = state["app_password"]
    title = state["title"]
    context = state["context"]
    files = state["files"]


    smtp = MIMEMultipart()
    smtp["Subject"] = title  # 제목
    smtp["From"] = from_mail # 발신자
    smtp["To"] = to_mail     # 수신자
    smtp["Date"] = formatdate(localtime=True)    # 보내는 날짜
    smtp["Message-ID"] = make_msgid()
    smtp.attach(MIMEText(context, _charset="utf-8"))


    # 첨부파일
    if files:
        for file in files:
            file_path = Path(file)
            with file_path.open("rb") as f:
                part = MIMEApplication(f.read(), _subtype="octet-stream")
                part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=file_path.name
                )
                smtp.attach(part)

    # SMTP 전송
    with smtplib.SMTP_SSL("smtp.daum.net", 465) as server:
        server.login(from_mail, app_password)
        server.send_message(smtp)

    # 보낸편지함 기록
    raw_bytes = smtp.as_bytes()
    with imaplib.IMAP4_SSL("imap.daum.net", 993) as imap:
        imap.login(from_mail, app_password)
        imap.append(
            "Sent",
            None,
            imaplib.Time2Internaldate(time.time()),
            raw_bytes,
        )