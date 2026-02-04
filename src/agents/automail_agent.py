from src.state import GraphState
from src.tasks.mail_prototype_llm import mail_prototype_llm
from src.tasks.smtp_tool import send_smtp_tool


def mail_prototype_node(state: GraphState) -> GraphState:
    result = mail_prototype_llm(state)
    state.update(result)
    return state


def send_smtp_node(state: GraphState) -> GraphState:
    # state에 들어있는 subject/body를 그대로 사용해 메일 전송
    send_smtp_tool(state)
    return state
