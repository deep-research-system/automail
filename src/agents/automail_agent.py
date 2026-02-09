from pathlib import Path
import yaml

from src.state import GraphState
from src.tasks.mail_writer_llm import mail_type_llm
from src.tasks.smtp import send_smtp

template_path = Path("templates.yaml")  # 루트 기준


def mail_type(state: GraphState) -> GraphState:
    result = mail_type_llm(state)
    state.update(result)
    return state


def mail_write(state: GraphState) -> GraphState:
    """
    LLM으로 부터 얻은 메일 타입에 맞는 초안 템플릿 선택해 변수값 채움
    """
    templates = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    mail_shape = templates[state["mail_type"]]

    state["title"] = mail_shape["title"]
    state["context"] = mail_shape["context"].format(
        receive_name=state["receive_name"],
        send_name=state["send_name"])
    
    return state


def smtp(state: GraphState) -> GraphState:
    """
    메일 전송
    """
    send_smtp(state)
    return state
