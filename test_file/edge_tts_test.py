import asyncio
import edge_tts

async def synthesize(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_path)
    print(f"saved {out_path}")

async def main():
    # 한국어 음성
    await synthesize(
        "안녕하세요. 이것은 한국어 음성 테스트입니다.",
        "ko-KR-SunHiNeural",      # 한국어 여성 음성
        "tts_ko.mp3",
    )
    # 영어 음성
    await synthesize(
        "Hello, this is an English text to speech test.",
        "en-US-AriaNeural",       # 영어 여성 음성
        "tts_en.mp3",
    )

asyncio.run(main())