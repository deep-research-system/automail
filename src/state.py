from typing import TypedDict, Optional, Literal, Dict, Any, Annotated

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
    # LLM으로부터 얻을 메일 타입
    mail_type: MailType

    # 초안 결과
    title: Annotated[str, "제목"]
    context: Annotated[str, "본문"]

class GraphState(SupervisorState, AutomailState):
    pass