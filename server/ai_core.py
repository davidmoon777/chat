import os
import re
import json
from dotenv import load_dotenv
load_dotenv()
import openai


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
raise RuntimeError("Set OPENAI_API_KEY in env")
openai.api_key = OPENAI_API_KEY


# 간단한 위험 패턴
BLOCK_PATTERNS = [r"비밀번호|계좌번호|카드번호|주민등록번호", r"자살|죽고싶다|자해", r"약물|마약|불법"]




def is_sensitive(text: str):
for p in BLOCK_PATTERNS:
if re.search(p, text):
return True, p
return False, None




def generate_replies(conversation_context: str, user_style_examples: list, partner_pattern: dict, max_candidates=5):
# prompt 설계: 사용자 스타일(사전입력) + 상대 패턴(통계) + 대화
system = (
"사용자의 스타일 예시와 대화 문맥을 받아, 사용자의 말투를 반영한 한국어 답장 후보를 생성한다.\n"
"절대 다른 사람을 사칭하지 말 것.\n"
)
style_block = "사용자스타일:\n" + "\\n".join(user_style_examples[:10]) + "\n"
instruction = (
f"대화:\n{conversation_context}\n\n"
f"요구: 자연스러운 답장 후보 {max_candidates}개를 JSON 배열로 출력. 각 항목은 text와 reason을 가질 것."
)
prompt = system + style_block + instruction


# 간단한 LLM 호출
resp = openai.ChatCompletion.create(
model="gpt-4o-mini",
messages=[{"role": "user", "content": prompt}],
temperature=0.7,
max_tokens=400,
)
out = resp["choices"][0]["message"]["content"]


# 모델의 자유 형식 응답을 보호적으로 파싱
try:
parsed = json.loads(out)
return parsed
except Exception:
# fallback: 각 문단을 후보로 본다
parts = [p.strip() for p in re.split(r"\n\n+", out) if p.strip()]
cand = []
for i, p in enumerate(parts[:max_candidates]):
cand.append({"text": p, "reason": "LLM generated"})
return cand
