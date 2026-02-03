import os
from typing import Dict, Any

from app.llm.extract_llm import extract_llm
from app.agents.remain_form import ask_missing_fields
from app.tools.profile_store import (
    profile_path_default,
    profile_check,
    create_profile,
    save_profile,
)
from app.tools.smtp_tool import send_smtp_tool

def extract_node(state: Dict[str, Any]) -> Dict[str, Any]:
    user_request = state["user_request"]
    state.update(extract_llm(user_request))
    return state

def ensure_profile_node(state: Dict[str, Any]) -> Dict[str, Any]:
    cfg_path = state.get("config_path") or profile_path_default()

    if not profile_check(cfg_path):
        print("\n[프로필 없음] 발신자 정보 입력")
        profile = create_profile(state)
        save_profile(cfg_path, profile)
        state.update(profile)
        print("\n프로필 생성 완료.\n")

    return state

def ask_missing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    ask_missing_fields(state)
    return state

def send_smtp_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n[SMTP 테스트 전송]")
    result = send_smtp_tool(state)
    state["tool_result"] = result
    state["last_message"] = f"메일 전송 성공 → {result.get('to_mail')}"
    return state
