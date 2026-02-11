from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from src.prompt import mail_prompt, general_prototype_prompt, feedback_prompt
from src.state import SupervisorState, TypeState, FeedbackState, PrototypeState, GraphState
from src.settings import settings


# 메일 타입 판단, 일반 타입(템플릿 없는 경우), 피드백을 통해 메일 수정 관련 LLM. 총 3개의 LLM 사용
def mail_type_llm(state: SupervisorState) -> TypeState:
    """
    1. 메일 타입 분류
    - LLM이 사용자 입력(supervisor_messages)를 보고 템플릿을 고르기 위한 메일 타입 답변
    - mail_type[보고서, 견적서, 일반] 중 하나 출력
    """
    llm = init_chat_model(
        api_key=settings.openai_api,
        model=settings.llm_model,
        temperature=0.0,).with_structured_output(TypeState)

    return llm.invoke([
        SystemMessage(content=mail_prompt),
        HumanMessage(content=state["supervisor_messages"])])


def general_prototype_llm(state: GraphState) -> PrototypeState:
    """
    2. 일반 타입인 경우 LLM이 초안 작성
    - 템플릿이 아닌 LLM이 직접 사용자 입력(supervisor_messages)을 보고 LLM 초안 작성
    title, context, confirm(=False로 무조건 출력) 출력
    """
    llm = init_chat_model(
        api_key=settings.openai_api,
        model=settings.llm_model,
        temperature=0.3,
    ).with_structured_output(PrototypeState)

    system_prompt = general_prototype_prompt.format(
        supervisor_messages=state["supervisor_messages"],
        receive_name=state["receive_name"],
        send_name=state["send_name"],
        files=state.get("files", ""),
    )
    return llm.invoke([SystemMessage(content=system_prompt)])


def feedback_llm(state: GraphState) -> FeedbackState:
    """
    3. 사용자 피드백
    - 윗 단계를 통해 초안이 나오면 LLM이 사용자 피드백 내용을 보고 컨펌 판단 및 메일 수정
    - confirm=True 인 경우 메일 전송
    - title, context, confirm 출력
    """
    llm = init_chat_model(
        api_key=settings.openai_api,
        model=settings.llm_model,
        temperature=0.0,
    ).with_structured_output(FeedbackState)

    system_prompt = feedback_prompt.format(
        feedback=state["feedback"],
        title=state["title"],
        context=state["context"]
    )

    return llm.invoke([
        SystemMessage(content=system_prompt),
    ])