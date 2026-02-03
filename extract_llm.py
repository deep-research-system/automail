import os
from typing import Optional, Literal, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from openai import OpenAI
from prompt import input_extract_prompt

load_dotenv()

MailType = Literal["견적서", "보고서", "일정", "일반"]

class Extractdata(BaseModel):
    user_request: Optional[str] = Field(description="요구사항", default=None)
    receive_name: Optional[str] = Field(description="수산지명", default=None)
    to_mail: Optional[str] = Field(description="수신자 메일", default=None)
    mail_type: Optional[MailType] = Field(description="메일 타입(견적서/보고서)", default=None)

    from_mail: Optional[str] = Field(description="발신자 메일", default=None)
    app_password: Optional[str] = Field(description="앱 비밀번호", default=None)
    send_name: Optional[str] = Field(description="발신자명", default=None)
    send_team: Optional[str] = Field(description="발신자 소속", default=None)

def extract_llm(user_request: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    resp = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": input_extract_prompt},
            {"role": "user", "content": user_request}],
        text_format=Extractdata)

    data = resp.output_parsed
    out = data.model_dump(exclude_none=True) # exclude_none=True : None 값인 필드 제거

    # user_request는 원본을 항상 들고 가는 게 편하니 여기서 강제로 세팅해도 됨
    out["user_request"] = user_request

    return out
