# 오디오 모듈 인터페이스 (ASR / TTS)

음성 강의 보조 시스템에서 **입력(ASR)과 출력(TTS)**을 담당하는 모듈입니다.
LLM·앱 쪽에서는 아래 두 함수만 가져다 쓰면 됩니다.

- `asr.py` → `transcribe()` : 음성 → 텍스트
- `tts.py` → `synthesize()` : 텍스트 → 음성

---

## 실행에 필요한 환경

- **Python 3.11 권장** (3.14는 일부 라이브러리 호환성 문제가 있어 사용하지 않음)
- 패키지 설치:
  ```
  pip install openai-whisper edge-tts
  ```
- **ffmpeg** 가 설치되어 PATH에 잡혀 있어야 함 (whisper가 오디오를 읽는 데 필요)
- `synthesize`는 **인터넷 연결 필요** (edge-tts가 온라인 서비스를 사용)

---

## transcribe (asr.py) — 음성 → 텍스트

```python
transcribe(audio_path, language=None) -> (text, segments)
```

| 인자 | 설명 |
|------|------|
| `audio_path` | 오디오 파일 경로 (mp3, m4a, wav 등 ffmpeg가 읽는 형식) |
| `language` | `"ko"`, `"en"` 등으로 언어 고정 가능. `None`이면 자동 감지 |

**반환값**
- `text` (str): 전체 인식 텍스트
- `segments` (list): 구간별 정보. 각 항목에 `start`, `end`, `text` 포함 (타임스탬프가 필요할 때 사용)

**사용 예시**
```python
from asr import transcribe

text, segments = transcribe("audio_results/lecture.mp3")
print(text)
```

**참고**
- 첫 호출 시 whisper 모델 가중치를 한 번 로드/다운로드함.
- 현재 `asr.py`는 `medium` 모델 사용 (정확하지만 CPU에서는 느림). 긴 음성은 처리에 시간이 걸리므로, 데모에서는 미리 변환해두는 것을 권장.

---

## synthesize (tts.py) — 텍스트 → 음성

```python
synthesize(text, lang="ko", out_path="tts_output.mp3") -> out_path
```

| 인자 | 설명 |
|------|------|
| `text` | 읽어줄 텍스트 |
| `lang` | `"ko"` 또는 `"en"` |
| `out_path` | 저장할 mp3 경로 |

**반환값**
- 저장된 파일 경로 (str)

**사용 예시**
```python
from tts import synthesize

synthesize("요약 내용입니다.", lang="ko", out_path="summary.mp3")
```

**참고**
- `lang`은 **텍스트의 실제 언어와 맞춰야** 발음이 자연스러움 (한국어 텍스트 → `"ko"`, 영어 텍스트 → `"en"`).
- 내부적으로 `asyncio.run`을 사용하므로, **앱이 이미 비동기 이벤트 루프 안에서 돌고 있으면 충돌**할 수 있음. 그런 경우 호출 방식 조정 필요 (해정에게 알려주세요).

---

## 전체 흐름에서의 위치

```
음성(강의)
   │
   ▼  transcribe()      ← ASR (이 모듈)
 텍스트
   │
   ▼  LLM (번역 / 요약 / 답변)   ← 팀원 담당
 텍스트
   │
   ▼  synthesize()      ← TTS (이 모듈)
 음성(요약/답변 읽기)
```

- `transcribe`의 출력 `text`를 LLM 입력으로 사용
- LLM이 만든 요약/답변 텍스트를 `synthesize`에 넘겨 음성으로 변환
- 가운데 LLM 부분이 팀원이 채울 자리