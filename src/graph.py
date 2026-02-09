# src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import GraphState
from src.agents.automail_agent import mail_type, mail_write, smtp

def build_automail_graph():
    """
    mail_type : 메일 타입 판단 단계
    mail_write : 타입에 맞는 템플릿 선택 후 변수값 채워 초안 작성 단계
    smtp : 메일 전송 단계
    """
    g = StateGraph(GraphState)

    g.add_node("mail_type", mail_type)
    g.add_node("mail_write", mail_write)
    g.add_node("smtp", smtp)

    g.add_edge(START, "mail_type")
    g.add_edge("mail_type", "mail_write")
    g.add_edge("mail_write", "smtp")
    g.add_edge("smtp", END)

    return g.compile()

graph = build_automail_graph()
