from extract_llm import extract_llm
from profile import profile_check, create_profile, save_profile
from remain_form import ask_missing_fields
from smtp import send_smtp

def main():
    user_request = input("요청 내용> ").strip()
    state = extract_llm(user_request)

    if not profile_check():
        print("\n[프로필 없음] 발신자 정보 입력")
        profile = create_profile(state)
        save_profile(profile)
        state.update(profile)
        print("\n프로필 생성 완료.\n")

    ask_missing_fields(state)

    print("\n[현재 state]")
    for k, v in state.items():
        print(f"- {k}: {v}")

    print("\n[SMTP 테스트 전송]")
    send_smtp(state)   

if __name__ == "__main__":
    main()
