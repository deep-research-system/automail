from langgraph.types import interrupt
from src.state import GraphState
from src.tasks.mail_writer_llm import mail_writer_llm
from src.tasks.smtp import send_smtp_tool

def mail_write(state: GraphState) -> GraphState:
    result = mail_writer_llm(state)
    state.update(result)
    return state

def feedback(state: GraphState) -> GraphState:
    feedback_answer = interrupt("feedback_needed")
    state["feedback"] = feedback_answer
    return state

def smtp_or_feedback(state: GraphState) -> str:
    return "smtp" if state.get("confirm") is True else "feedback"

def smtp(state: GraphState) -> GraphState:
    send_smtp_tool(state)
    return state
