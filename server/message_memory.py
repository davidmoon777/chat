# 간단한 로컬 파일 기반 메모리(프로토타입)
import json
from pathlib import Path


DB = Path("./memory.json")
if not DB.exists():
DB.write_text(json.dumps({"conversations": []}, ensure_ascii=False))




def save_message(entry: dict):
data = json.loads(DB.read_text())
data["conversations"].append(entry)
DB.write_text(json.dumps(data, ensure_ascii=False, indent=2))




def get_recent(n=20):
data = json.loads(DB.read_text())
return data.get("conversations", [])[-n:]
