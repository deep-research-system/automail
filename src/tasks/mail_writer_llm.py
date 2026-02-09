from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from src.prompt import mail_prompt
from src.state import SupervisorState, AutomailState
from src.settings import settings

def mail_type_llm(state: SupervisorState) -> AutomailState:
    """
    LLM이 사용자 입력(supervisor_messages)를 보고 템플릿을 고르기 위한 메일 타입 답변
    - [보고서, 견적서, 일반] 중 하나 출력
    """
    llm = init_chat_model(
        api_key=settings.openai_api,
        model=settings.llm_model,
        temperature=0.0,).with_structured_output(AutomailState)

    return llm.invoke([
        SystemMessage(content=mail_prompt),
        HumanMessage(content=state["supervisor_messages"])])





