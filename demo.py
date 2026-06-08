from asr import transcribe
from tts import synthesize

# 1. 음성 → 텍스트 (ASR)
text, segments = transcribe("audio_results/test.m4a")
print("인식된 텍스트:", text)

# 2. 텍스트 → 음성 (TTS)
synthesize(text, lang="ko", out_path="roundtrip.mp3")
print("saved roundtrip.mp3")