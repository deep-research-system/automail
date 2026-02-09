from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage

from src.prompt import mail_prompt
from src.state import GraphState, AutomailState
from src.settings import settings


def mail_writer_llm(state: GraphState) -> AutomailState:
    llm = init_chat_model(
        api_key=settings.openai_api,
        model=settings.llm_model,
        temperature=0.3,
    ).with_structured_output(AutomailState)

    system_prompt = mail_prompt.format(
        supervisor_messages=state["supervisor_messages"],
        receive_name=state["receive_name"],
        send_name=state["send_name"],
        files=state["files"],
        feedback=state.get("feedback", ""),
        title=state.get("title", ""),
        context=state.get("context", ""))

    return llm.invoke([SystemMessage(content=system_prompt)])
