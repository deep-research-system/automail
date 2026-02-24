import smtplib, imaplib, time, html
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid


def send_smtp(state: dict) -> dict:
    """
    서명 양식의 그림을 첨부하는 방법
    """
    from_mail = state["from_mail"]
    to_mail = state["to_mail"]
    app_password = state["app_password"]
    title = state["title"]
    context = state["context"]
    files = state["files"]

    sign_image_path = Path("sign_test.png")

    smtp = MIMEMultipart()
    smtp["Subject"] = title
    smtp["From"] = from_mail
    smtp["To"] = to_mail
    smtp["Date"] = formatdate(localtime=True)
    smtp["Message-ID"] = make_msgid()

    related = MIMEMultipart("related")
    context_to_html = html.escape(context).replace("\n", "<br>")

    cid = make_msgid(domain="sig")
    cid_value = cid[1:-1]

    sign_html = f"""
    <br><br>
    <div style="border-top:1px solid #e5e5e5; margin-top:16px; padding-top:12px;">
      <img src="cid:{cid_value}" alt="signature"
           style="max-width:720px; height:auto; display:block;">
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

    related.attach(MIMEText(body_html, "html", _charset="utf-8"))

    with sign_image_path.open("rb") as f:
        img = MIMEImage(f.read())
    img.add_header("Content-ID", cid)
    img.add_header("Content-Disposition", "inline", filename=sign_image_path.name)
    related.attach(img)
    smtp.attach(related)

    # 일반 첨부파일
    for file in files:
        file_path = Path(file)
        with file_path.open("rb") as f:
            part = MIMEApplication(f.read(), _subtype="octet-stream")
        part.add_header("Content-Disposition", "attachment", filename=file_path.name)
        smtp.attach(part)

    # SMTP 전송
    with smtplib.SMTP_SSL("smtp.daum.net", 465) as server:
        server.login(from_mail, app_password)
        server.send_message(smtp)

    # 보낸편지함 기록
    raw_bytes = smtp.as_bytes()
    with imaplib.IMAP4_SSL("imap.daum.net", 993) as imap:
        imap.login(from_mail, app_password)
        imap.append("Sent", None, imaplib.Time2Internaldate(time.time()), raw_bytes)

    return state