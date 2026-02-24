import smtplib
import imaplib
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
import html


def send_smtp(state: dict) -> dict:
    """
    html문에서 직접 서명 양식 작성 방법
    """
    # state에서 필요한 값만 한 번 꺼내서 통일
    send_name = state["send_name"]
    from_mail = state["from_mail"]
    to_mail = state["to_mail"]
    app_password = state["app_password"]
    title = state["title"]
    context = state["context"]
    files = state["files"]

    # 제목 및 본문
    smtp = MIMEMultipart()
    smtp["Subject"] = title  # 제목
    smtp["From"] = from_mail # 발신자
    smtp["To"] = to_mail     # 수신자
    smtp["Message-ID"] = make_msgid()

    context_escape = html.escape(context)
    context_to_html = context_escape.replace("\n", "<br>")

    sign_html = f"""
    <br><br>
    <div style="border-top:1px solid #e5e5e5; margin-top:16px; padding-top:12px;
                font-family:Arial, sans-serif; font-size:12px; color:#222;">
      <div style="font-size:14px; font-weight:700;">{send_name}
        <span style="font-size:12px; font-weight:400; color:#666; margin-left:8px;">사원</span>
      </div>
      <div style="margin-top:8px; line-height:1.6;">
        <div><b>Phone: </b>010-1234-5678</div>
        <div><b>Email: </b>mail@daum.net</div>
        <div><b>Adress: </b>부산광역시 해운대구 센텀북대로</div>
      </div>
    </div>
    """

    body_html = f"""
    <html>
      <body>
        <div style="font-family:Arial, sans-serif; font-size:14px; color:#111;">
          {context_to_html}
        </div>
        {sign_html}
      </body>
    </html>
    """

    # 본문을 HTML로 첨부
    smtp.attach(MIMEText(body_html, "html", _charset="utf-8"))

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