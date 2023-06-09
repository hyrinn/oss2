import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = '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'

# 사용자 입력에 대한 응답을 생성하는 함수
def generate_response(prompt):
    if prompt.startswith("Is the proof valid?"):  # 입력이 "Is the proof valid?"로 시작하면
        return is_proof_valid(prompt)  # is_proof_valid 함수를 호출하여 증명의 유효성을 확인하고 응답을 생성
    elif prompt.startswith("Is the expression true?"):  # 입력이 "Is the expression true?"로 시작하면
        return is_expression_true(prompt)  # is_expression_true 함수를 호출하여 논리식의 참/거짓을 확인하고 응답을 생성
    else:  # 위 조건에 해당하지 않는 경우
        completions = openai.Completion.create( # GPT-3 모델을 사용하는 엔진 지정
            engine="text-davinci-003", # GPT-3 모델을 사용하는 엔진 지정
            prompt=prompt, # 입력 프롬프트 전달
            max_tokens=1024, # 최대 토큰 수를 지정해 응답의 길이를 제한한다.
            stop=None, # 중간 단어를 지정하지 않음 (응답에 대한 강제 중단 없음)
            temperature=0, # 응답 생성의 보수적인 정도를 조정한다. (0은 보수적)
            top_p=1, # 다음 가능한 토큰 중에서 최상위 확률을 갖는 토큰만 고려한다.
        )
        message = completions["choices"][0]["text"].replace("\n", "")  # OpenAI의 API를 사용하여 대화 응답 생성
        return message # 응답 반환

# 증명이 유효한지 확인하는 함수
def is_proof_valid(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003", # GPT-3 모델 사용하는 엔진 지정
        prompt=prompt, # 입력 프롬프트를 전달
        max_tokens=1, # 응답으로 받을 최대 토큰 수를 1로 지정
        temperature=0, # 응답 생성의 보수적인 정도를 조정
        top_p=1, # 다음 가능한 토큰 중에서 최상위 확률을 갖는 토큰만 고려
        n=1, # 응답 중에서 가장 확률적으로 높은 하나의 응답만 받기
        stop=None # 중간 단어 지정하지 않음. (응답에 대한 강제 중단 없음)
    )
    answer = completions["choices"][0]["text"].strip() # 응답에서 텍스트 추출 후 양쪽 공백 제거
    return answer == "Yes" # 응답이 “Yes”인지 확인하여 유효성 반환.


# 논리식이 참인지 확인하는 실험 코드 ( 사용자 지정 )
def is_expression_true(prompt):
    # 공백 제거
    expression = prompt.replace(" ", "")

    # 논리식 평가
    if expression == "A+(B·C)=(A+B)·(A+C)": 
        return True # 참이니 True 반환
    elif expression == "A·B·C=(A·B)·C=A·(B·C)":
        return True 
    elif expression == "(A+B)·(A+C)=A+(B·C)":
        return True
    else:
        return False # 이 식 이외 논리식 False ( 실제로 사용되는 코드 아니라 실험을 위해 넣은 코드)


# Streamlit 애플리케이션 설정
st.header("🤖Logic ChatGPT-3 (Demo)") # 헤더를 설정
st.markdown("[Be Original](https://yunwoong.tistory.com/)") # 링크가 있는 마크다운 텍스트를 추가

 
# 세션 상태 초기화
if 'generated' not in st.session_state:
    st.session_state['generated'] = [] # ‘generated’ 라는 키가 세션 상태에 없으면 빈 리스트로 초기화


if 'past' not in st.session_state:
    st.session_state['past'] = [] # ‘past’ 라는 키가 세션 상태에 없으면 빈 리스트로 초기화


# 사용자 입력 처리
with st.form('form', clear_on_submit=True): # form 시작. 제출 시 입력값 초기화
    user_input = st.text_input('You: ', '', key='input') # 사용자 입력 받기
    submitted = st.form_submit_button('Send') # 제출 버튼 생성


# 사용자 입력이 있는 경우 응답 생성
if submitted and user_input:
    if user_input.lower() == "is the expression true?":  # 입력이 "Is the expression true?"인 경우
        st.session_state.past.append(user_input) # 사용자 입력 기록에 추가
        st.session_state.generated.append("Please provide the logical expression to evaluate.") # 응답 기록에 추가
    else:  # 위 조건에 해당하지 않는 경우
        output = generate_response(user_input) # 응답 생성
        st.session_state.past.append(user_input) # 사용자 입력 기록에 추가
        st.session_state.generated.append(output) # 응답 기록에 추가


# 생성된 응답을 출력
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1): # 응답 기록을 역순으로 순회
        if st.session_state['past'][i].startswith("Is the proof valid?"):  # 입력이 "Is the proof valid?"로 시작하는 경우
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') # 사용자 입력 출력
            if st.session_state["generated"][i] == "Yes": # 응답이 “Yes”인 경우
                message("The proof is valid.", key=str(i)) # “The proof is valid.” 출력
            else: # 응답이 “Yes”가 아닌 경우
                message("The proof is invalid.", key=str(i))# “The proof is invalid.” 출력

        elif st.session_state['past'][i].startswith("Is the expression true?"):  # 입력이 "Is the expression true?"로 시작하는 경우
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') # 사용자 입력 출력
            if st.session_state["generated"][i] == "Please provide the logical expression to evaluate.": # 생성된 응답이 "Please provide the logical expression to evaluate.” 와 동일한지 확인하는 조건문
                message(st.session_state["generated"][i], key=str(i)) # "Please provide the logical expression to evaluate." 출력

            else:
                expression = st.session_state['past'][i].replace("Is the expression true?", "").strip() # 논리식 추출

                if is_expression_true(expression): # expression이 true라면
                    message(f"The expression '{expression}' is true.", key=str(i)) # 해당 논리식이 참임을 출력

                else: # expression이 false라면
                    message(f"The expression '{expression}' is false.", key=str(i)) # 해당 논리식이 거짓임을 출력
        else:  # 위 조건에 해당하지 않는 경우
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') # 사용자 입력 출력
            message(st.session_state["generated"][i], key=str(i)) # 응답 출력