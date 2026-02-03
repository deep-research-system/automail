from typing import Dict, Any, List, Tuple
from app.llm.extract_llm import Extractdata

def get_fields_and_labels() -> Tuple[List[str], Dict[str, str]]:
    """Extractdata 스키마에서 (필드 목록, 라벨) 자동 추출"""
    fields: List[str] = []
    labels: Dict[str, str] = {}

    for name, field in Extractdata.model_fields.items():
        fields.append(name)
        labels[name] = field.description or name

    return fields, labels

def get_missing_fields(state: Dict[str, Any], fields: List[str]) -> List[str]:
    """state에 아직 값이 없거나 빈 문자열인 필드만 추려냄"""
    missing: List[str] = []
    for key in fields:
        v = state.get(key)
        if v is None or (isinstance(v, str) and v.strip() == ""):
            missing.append(key)
    return missing

def ask_missing_fields(state: Dict[str, Any]) -> None:
    """Extractdata 스키마 기준으로 state에 없는 값만 input()으로 채움"""
    fields, labels = get_fields_and_labels()
    missing = get_missing_fields(state, fields)

    for key in missing:
        state[key] = input(f"{labels[key]}> ").strip()
