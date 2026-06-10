import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-2.5-flash"


def _call_gemini(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            error_msg = str(e)

            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                wait_time = 2 ** attempt
                print(f"Gemini 서버 혼잡. {wait_time}초 후 재시도...")
                time.sleep(wait_time)

            elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = 35
                print(f"Gemini 쿼터 제한. {wait_time}초 후 재시도...")
                time.sleep(wait_time)

            else:
                raise e

    return "Gemini API 제한으로 응답을 생성하지 못했습니다."


def translate_text(text, target_lang="ko"):
    language = "Korean" if target_lang == "ko" else "English"

    prompt = f"""
Translate the following lecture transcript into {language}.

Requirements:
- Keep technical terms accurate.
- Do not add explanations.
- Preserve meaning.

Transcript:
{text}
"""
    return _call_gemini(prompt)


def summarize_text(text, lang="ko"):

    language = "Korean" if lang == "ko" else "English"

    prompt = f"""
You are an AI lecture assistant.

Summarize the lecture in {language}.

Requirements:

- Do NOT use markdown.
- Do NOT use #, ##, ###.
- Do NOT use *, -, bullet points.
- Write in natural lecture-note style.
- Use plain text only.
- Organize with simple section titles.
- Keep the summary concise and readable for students.

Format:

강의 주제

주요 개념

핵심 내용

한 줄 정리

Lecture transcript:

{text}
"""

    return _call_gemini(prompt)


def answer_question(context, question, lang="ko"):
    language = "Korean" if lang == "ko" else "English"

    prompt = f"""
You are an AI lecture assistant.

Answer the student's question using ONLY the lecture transcript.

If the answer cannot be found, say:
"해당 강의 내용에서는 확인할 수 없습니다."

Answer language: {language}

Lecture transcript:
{context}

Question:
{question}
"""
    return _call_gemini(prompt)