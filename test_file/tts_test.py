from kokoro import KPipeline
import soundfile as sf

# lang_code='a' = 미국 영어
pipeline = KPipeline(lang_code='a')

text = "Hello, this is a test of the text to speech system."

# voice 옵션 중 하나 (af_heart)
generator = pipeline(text, voice='af_heart')

# 생성된 오디오를 wav 파일로 저장
for i, (graphemes, phonemes, audio) in enumerate(generator):
    sf.write(f'output_{i}.wav', audio, 24000)
    print(f"saved output_{i}.wav")