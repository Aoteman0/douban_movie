#coding=gbk
import whisper

#����ת�ı�
model = whisper.load_model("small")
result = model.transcribe("ruyuan.mp3",language="zh")
print(result["text"])
