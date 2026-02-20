from langgraph.graph import StateGraph, START, END
from src.state import GraphState
from src.agents.automail_agent import (
    mail_type, prototype_or_template, feedback, write_mail_from_feedback, smtp_or_feedback, smtp
)

def build_automail_graph():
    """
    1단계. 메일 타입 분류(mail_type)

    2단계. 메일 타입에 따라 초안 작성(prototype_or_template)
     - [보고서, 견적서]인 경우 => 템플릿 초안 작성
     - [일반]인 경우 => LLM을 통한 초안 작성

    3단계. 작성된 초안을 가지고 사용자에게 피드백 요청(feedback)

    4단계. feedback 단계에서 받은 사용자 입력을 토대로 다음 단계를 결정(write_mail_from_feedback)
     - 수정이 필요한 경우 => 다시 feedback 단계로 돌아감
     - 수정이 필요없는 경우 => smtp 단계로 넘어감

    5단계. 최종 메일 전송(smtp)
    """
    g = StateGraph(GraphState)
    g.add_node("mail_type", mail_type)
    g.add_node("prototype_or_template", prototype_or_template)
    g.add_node("feedback", feedback)
    g.add_node("write_mail_from_feedback", write_mail_from_feedback)
    g.add_node("smtp", smtp)

    g.add_edge(START, "mail_type")
    g.add_edge("mail_type", "prototype_or_template")
    g.add_edge("prototype_or_template", "feedback")
    g.add_edge("feedback", "write_mail_from_feedback")

    g.add_conditional_edges(
        "write_mail_from_feedback",
        smtp_or_feedback,
        {"smtp": "smtp", "feedback": "feedback"},
    )
    g.add_edge("smtp", END)

    return g.compile()

graph = build_automail_graph()
