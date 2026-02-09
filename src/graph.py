from langgraph.graph import StateGraph, START, END
from src.state import GraphState
from src.agents.automail_agent import mail_write, feedback, smtp_or_feedback, smtp

def build_automail_graph():
    g = StateGraph(GraphState)

    g.add_node("mail_write", mail_write)
    g.add_node("feedback", feedback)
    g.add_node("smtp", smtp)

    g.add_edge(START, "mail_write")

    g.add_conditional_edges(
        "mail_write",
        smtp_or_feedback,
        {"smtp": "smtp", "feedback": "feedback"},
    )

    # ✅ 피드백 입력 후 다시 작성 노드로
    g.add_edge("feedback", "mail_write")

    g.add_edge("smtp", END)

    return g.compile()

graph = build_automail_graph()