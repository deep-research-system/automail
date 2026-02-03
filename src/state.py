from typing import TypedDict, Optional, Literal, Dict, Any, List

MailType = Literal["견적서", "보고서", "일정", "일반"]

class AutomailState(TypedDict, total=False):
    user_request: str
    receive_name: Optional[str]
    to_mail: Optional[str]
    mail_type: Optional[MailType]

    from_mail: Optional[str]
    app_password: Optional[str]
    send_name: Optional[str]
    send_team: Optional[str]