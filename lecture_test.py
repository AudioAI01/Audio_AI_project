from asr import transcribe

text, segments = transcribe("audio_results/lecture.mp3")

print(text)