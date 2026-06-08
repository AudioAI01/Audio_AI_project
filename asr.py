import whisper


# 모델은 시작할 때 한 번만 로딩함.
# transcribe를 부를 때마다 매번 로딩하면 엄청 느려짐
_model = whisper.load_model("medium")

def transcribe(audio_path, language=None):
    """음성 파일을 텍스트로 변환.
    - audio_path: 오디오 파일 경로
    - language: "ko"/"en"으로 고정 가능, None이면 자동 감지
    반환: (전체 텍스트, segment 리스트)
    """
    result = _model.transcribe(audio_path,language=language)
    text = result["text"].strip()

    segments = result["segments"]
    return text, segments


# 이 파일을 직접 실행했을 때만 도는 테스트용 코드
if __name__ == "__main__":
    text, segments = transcribe("test.m4a")   # 본인 파일명으로
    print(text)