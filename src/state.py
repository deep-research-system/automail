from typing import TypedDict, Optional, Literal, Dict, Any, Annotated, NotRequired

class SupervisorState(TypedDict):
    # SUPERVISOR로 부터 받을 내용
    supervisor_messages: Annotated[str, "요청사항"]
    receive_name: Annotated[str, "수신자명"]
    to_mail: Annotated[str, "수신자 메일"]
    send_name: Annotated[str, "발신자명"]
    from_mail: Annotated[str, "발신자 메일"]
    app_password: Annotated[str, "앱 비밀번호"]
    files: Annotated[str, "첨부파일"]


MailType = Literal["견적서", "보고서", "일반"]
class AutomailState(TypedDict):
    # LLM 출력 형식 고정용
    mail_type: Annotated[MailType, "메일 타입"]

    
class GraphState(SupervisorState, total=False):
    mail_type: Annotated[MailType, "메일 타입"]
    title: Annotated[str, "제목"]
    context: Annotated[str,"본문"]