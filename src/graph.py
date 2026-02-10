# src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import GraphState
from src.agents.automail_agent import (
    mail_type, prototype_from_templates, feedback, write_mail_from_feedback, smtp_or_feedback, smtp
)

def build_automail_graph():
    g = StateGraph(GraphState)

    g.add_node("mail_type", mail_type)
    g.add_node("prototype_from_templates", prototype_from_templates)
    g.add_node("feedback", feedback)
    g.add_node("write_mail_from_feedback", write_mail_from_feedback)
    g.add_node("smtp", smtp)

    g.add_edge(START, "mail_type")
    g.add_edge("mail_type", "prototype_from_templates")
    g.add_edge("prototype_from_templates", "feedback")
    g.add_edge("feedback", "write_mail_from_feedback")

    g.add_conditional_edges(
        "write_mail_from_feedback",
        smtp_or_feedback,
        {"smtp": "smtp", "feedback": "feedback"},
    )
    g.add_edge("smtp", END)

    return g.compile()
graph = build_automail_graph()
