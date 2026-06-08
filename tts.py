import asyncio
import edge_tts

# [핵심 1] 언어별 음성을 딕셔너리로 관리.
# 나중에 목소리를 바꾸거나 언어를 추가하기 쉬움.
_VOICES = {
    "ko": "ko-KR-SunHiNeural",   # 한국어 여성
    "en": "en-US-AriaNeural",    # 영어 여성
}

def synthesize(text, lang="ko", out_path="tts_output.mp3"):
    """텍스트를 음성 파일로 변환.
    - text: 읽을 텍스트
    - lang: "ko" 또는 "en"
    - out_path: 저장할 mp3 경로
    반환: 저장된 파일 경로
    """
    voice = _VOICES.get(lang, _VOICES["en"])

    # [핵심 2] edge-tts는 async라서, 내부에서 asyncio.run으로 감싸
    # 밖에서는 그냥 일반 함수처럼 부를 수 있게 만듦.
    async def _run():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)

    asyncio.run(_run())
    return out_path

# 직접 실행했을 때만 도는 테스트
if __name__ == "__main__":
    synthesize("안녕하세요. 함수 테스트입니다.", lang="ko", out_path="func_ko.mp3")
    synthesize("Hello, this is a function test.", lang="en", out_path="func_en.mp3")
    print("done")