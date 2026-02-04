# src/prompt.py

mail_prompt = """
너는 이메일 초안을 생성하는 함수다.
아래의 정보를 가지고 사용자 요구에 맞는 이메일 초안을 작성하라.

[요청사항]
{supervisor_messages}

[수신자 이름]
{receive_name}

[발신자 이름]
{send_name}
"""
