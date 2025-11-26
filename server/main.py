from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ai_core import generate_replies, is_sensitive
from message_memory import save_message, get_recent


app = FastAPI()


class Incoming(BaseModel):
chat_id: str
sender: str
message: str
recent_context: Optional[List[str]] = []
user_style_examples: Optional[List[str]] = []


class Outgoing(BaseModel):
chat_id: str
auto_send: bool
candidates: List[dict]
reason: Optional[str] = None


@app.post('/incoming', response_model=Outgoing)
async def incoming(msg: Incoming):
# 1) 저장
save_message({"chat_id": msg.chat_id, "sender": msg.sender, "message": msg.message})


# 2) 민감도 검사
sensitive, pattern = is_sensitive(msg.message)


# 3) LLM 후보 생성
context = "\n".join(msg.recent_context[-10:]) if msg.recent_context else msg.message
candidates = generate_replies(context, msg.user_style_examples or [], {})


# 4) 후보별 민감도 검사
for c in candidates:
s, p = is_sensitive(c.get('text',''))
c['blocked'] = s
c['block_pattern'] = p


# 모드 c: 위험(민감)한 후보가 하나라도 있으면 승인 필요 -> auto_send False
any_sensitive = any(c.get('blocked') for c in candidates)
auto_send = not any_sensitive


return Outgoing(chat_id=msg.chat_id, auto_send=auto_send, candidates=candidates,
reason=("민감 후보 포함: 수동 승인 필요" if not auto_send else "자동 전송 허용"))


@app.get('/recent')
async def recent():
return get_recent()
