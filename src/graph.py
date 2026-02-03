from langgraph.graph import StateGraph, START, END
from app.state import AutomailState
from app.agents.automail_agent import (
    extract_node,
    ensure_profile_node,
    ask_missing_node,
    send_smtp_node,
)

def build_automail_graph():
    g = StateGraph(AutomailState)

    g.add_node("extract", extract_node)
    g.add_node("ensure_profile", ensure_profile_node)
    g.add_node("ask_missing", ask_missing_node)
    g.add_node("send_smtp", send_smtp_node)

    g.add_edge(START, "extract")
    g.add_edge("extract", "ensure_profile")
    g.add_edge("ensure_profile", "ask_missing")
    g.add_edge("ask_missing", "send_smtp")
    g.add_edge("send_smtp", END)

    return g.compile()
