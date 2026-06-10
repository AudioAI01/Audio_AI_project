import os
import gradio as gr

from asr import transcribe
from llm import translate_text, summarize_text, answer_question
from tts import synthesize


os.makedirs("outputs", exist_ok=True)


def process_lecture(audio_file, input_lang, output_lang):
    if audio_file is None:
        return "오디오 파일을 업로드해주세요.", "", "", None

    # Gradio audio file path
    audio_path = audio_file

    # language option
    asr_lang = None
    if input_lang == "한국어":
        asr_lang = "ko"
    elif input_lang == "영어":
        asr_lang = "en"

    out_lang_code = "ko" if output_lang == "한국어" else "en"

    # 1. ASR
    text, segments = transcribe(audio_path, language=asr_lang)

    # 2. Translation
    # translated = translate_text(text, target_lang=out_lang_code)

    # 3. Summary
    summary = summarize_text(text, lang=out_lang_code)

    # 4. TTS
    summary_audio_path = "outputs/summary_output.mp3"
    synthesize(summary, lang=out_lang_code, out_path=summary_audio_path)

    # return text, translated, summary, summary_audio_path
    return text, summary, summary_audio_path


def qa_feedback(lecture_text, question, output_lang):
    if not lecture_text.strip():
        return "먼저 강의 음성을 업로드하고 분석해주세요.", None

    if not question.strip():
        return "질문을 입력해주세요.", None

    out_lang_code = "ko" if output_lang == "한국어" else "en"

    answer = answer_question(
        context=lecture_text,
        question=question,
        lang=out_lang_code
    )

    answer_audio_path = "outputs/answer_output.mp3"
    synthesize(answer, lang=out_lang_code, out_path=answer_audio_path)

    return answer, answer_audio_path


with gr.Blocks(title="AI Lecture Assistant") as demo:
    gr.Markdown("# AI 기반 강의 보조 시스템")
    gr.Markdown(
        "강의 음성을 업로드하면 STT, 번역, 요약, 질의응답, 음성 피드백을 제공합니다."
    )

    with gr.Row():
        input_lang = gr.Dropdown(
            choices=["자동 감지", "한국어", "영어"],
            value="자동 감지",
            label="입력 음성 언어"
        )

        output_lang = gr.Dropdown(
            choices=["한국어", "영어"],
            value="한국어",
            label="출력 언어"
        )

    audio_input = gr.Audio(
        label="강의 음성 파일 업로드",
        type="filepath"
    )

    analyze_btn = gr.Button("강의 분석 시작")

    stt_output = gr.Textbox(
        label="1. STT 결과",
        lines=8
    )

    translation_output = gr.Textbox(
        label="2. 번역 결과",
        lines=8
    )

    summary_output = gr.Textbox(
        label="3. 요약 결과",
        lines=10
    )

    summary_audio = gr.Audio(
        label="4. 요약 음성 피드백"
    )

    analyze_btn.click(
        fn=process_lecture,
        inputs=[audio_input, input_lang, output_lang],
        outputs=[
            stt_output,
            translation_output,
            summary_output,
            summary_audio
        ]
    )

    gr.Markdown("## 강의 내용 기반 질문하기")

    question_input = gr.Textbox(
        label="질문 입력",
        placeholder="예: 이 강의의 핵심 내용은 무엇인가요?"
    )

    qa_btn = gr.Button("질문하기")

    answer_output = gr.Textbox(
        label="답변",
        lines=6
    )

    answer_audio = gr.Audio(
        label="답변 음성 피드백"
    )

    qa_btn.click(
        fn=qa_feedback,
        inputs=[stt_output, question_input, output_lang],
        outputs=[answer_output, answer_audio]
    )


if __name__ == "__main__":
    demo.launch()