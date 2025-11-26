

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B")
model = AutoModelForCausalLM.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B").cuda()




def generate_reply(text: str) -> str:
prompt = f"사용자 말투에 맞춰 자연스러운 답장을 생성:
{text}
답장:"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
output = model.generate(**inputs, max_new_tokens=50)
return tokenizer.decode(output[0], skip_special_tokens=True).split("답장:")[-1].strip()
