import json
import os

profile_path = os.path.join(os.path.dirname(__file__), "config.json")

PROFILE_KEYS = ["from_mail", "app_password", "send_name", "send_team"]

def profile_check() -> bool:
    """
    프로필 유무 확인(True/False)
    """
    if not os.path.exists(profile_path):
        return False

    with open(profile_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    profiles = cfg.get("profiles", [])
    if not profiles:
        return False

    p = profiles[0] or {}
    return all(p.get(k) for k in PROFILE_KEYS)


def create_profile(state: dict | None = None) -> dict:
    """
    프로필 생성에 필요한 것들만 폼으로 반환
    """
    LABELS = {
    "from_mail": "발신자 이메일",
    "app_password": "앱 비밀번호",
    "send_name": "발신자명",
    "send_team": "발신자 소속"}

    state = state or {}
    profile = {}

    for k in PROFILE_KEYS:
        if state.get(k):
            profile[k] = state[k]
            continue
        profile[k] = input(f"{LABELS[k]}> ").strip()

    return profile


# 3) 저장하는 함수
def save_profile(profile: dict) -> None:
    """
    프로필에 값 저장
    - 발신자명, 발신자 소속, 발신자 메일, 앱 비밀번호
    """
    cfg = {}
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

    cfg["profiles"] = [{k: profile.get(k, "") for k in PROFILE_KEYS}]

    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
