from langgraph.graph import StateGraph, START, END
from src.state import GraphState
from src.agents.automail_agent import mail_prototype_node, send_smtp_node


def build_automail_graph():
    g = StateGraph(GraphState)

    g.add_node("mail_prototype", mail_prototype_node)
    g.add_node("smtp", send_smtp_node)

    g.add_edge(START, "mail_prototype")
    g.add_edge("mail_prototype", "smtp")
    g.add_edge("smtp", END)

    return g.compile()


graph = build_automail_graph()
