#coding=gbk
import whisper

#语音转文本
model = whisper.load_model("small")
result = model.transcribe("ruyuan.mp3",language="zh")
print(result["text"])
