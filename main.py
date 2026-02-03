from extract_llm import extract_llm

def main():
    user_input = input("요청 내용> ").strip()
    first_data = extract_llm(user_input)
    
    print("\n")
    print(first_data)
    print("\n[LLM 추출 결과]")
    for k, v in first_data.items():
        print(f"- {k}: {v}")

if __name__ == "__main__":
    main()