from pathlib import Path
import yaml
from langgraph.types import interrupt

from src.state import GraphState
from src.tasks.mail_writer_llm import mail_type_llm, general_prototype_llm, feedback_llm
from src.tasks.smtp import send_smtp

# 템플릿 불러오기
template_path = Path("templates.yaml")


def mail_type(state: GraphState) -> GraphState:
    """
    LLM이 supervisor messages를 보고 메일 타입 판단
    [견적서, 보고서, 일반] 중 하나 선택
    """
    result = mail_type_llm(state)
    state.update(result)
    return state


def prototype_or_template(state: GraphState) -> GraphState:
    """
    견적서/보고서 => 템플릿으로 초안 작성
    일반 => LLM을 통한 초안 작성
    초안 단계이므로 feedback 단계에서 사용될 confirm은 False로 초기값 설정
    """
    # 견적서/보고서 타입(템플릿이 있는 경우)
    if state["mail_type"] in ("견적서", "보고서"):
        templates = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        template_prototype = templates[state["mail_type"]]
        state["title"] = template_prototype["title"]
        state["context"] = template_prototype["context"].format(
            receive_name=state["receive_name"],
            send_name=state["send_name"])
        state["confirm"] = False
        return state
    
    # 일반 타입(LLM, 템플릿이 없는 경우)
    prototype = general_prototype_llm(state)
    state["title"] = prototype["title"]
    state["context"] = prototype["context"]
    state["confirm"] = False
    return state


def feedback(state: GraphState) -> GraphState:
    """
    사용자에게 피드백 받을 인터럽트 단계
    """
    feedback_answer = interrupt("feedback_needed")
    state["feedback"] = feedback_answer
    return state

def write_mail_from_feedback(state: GraphState) -> GraphState:
    """
    LLM이 사용자로부터 받은 피드백을 가지고 컨펌 판단 및 이메일 유지/수정
    """
    result = feedback_llm(state)
    state.update(result)
    return state

def smtp_or_feedback(state: GraphState) -> str:
    """
    confirm=True면 전송, 아니면 다시 피드백 받기(루프)
    """
    if state["confirm"] is True:
        return "smtp"
    else:
        return "feedback"


def smtp(state: GraphState) -> GraphState:
    """
    메일 전송
    """
    send_smtp(state)
    return state
