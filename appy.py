import requests
import gradio as gr

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru"
}


def translate_text(text, source, target):

    if not text.strip():
        return "Please enter some text."

    try:
        source_code = (
            "autodetect"
            if source == "Auto Detect"
            else LANGUAGES[source]
        )

        target_code = LANGUAGES[target]

        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"{source_code}|{target_code}"
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("responseStatus") == 200:
            return data["responseData"]["translatedText"]

        return "Translation service could not process the request."

    except requests.RequestException as error:
        return f"Network error: {error}"

    except Exception as error:
        return f"Error: {error}"


with gr.Blocks(title="Language Translation Tool") as app:

    gr.Markdown("# 🌐 Language Translation Tool")

    gr.Markdown(
        "Enter text, select source and target languages, "
        "and click Translate."
    )

    text_input = gr.Textbox(
        label="Enter Text",
        placeholder="Type your text here...",
        lines=5
    )

    with gr.Row():

        source_language = gr.Dropdown(
            choices=["Auto Detect"] + list(LANGUAGES.keys()),
            value="English",
            label="Source Language"
        )

        target_language = gr.Dropdown(
            choices=list(LANGUAGES.keys()),
            value="Telugu",
            label="Target Language"
        )

    translate_button = gr.Button(
        "🔄 Translate",
        variant="primary"
    )

    output = gr.Textbox(
        label="Translated Text",
        lines=5
    )

    translate_button.click(
        fn=translate_text,
        inputs=[
            text_input,
            source_language,
            target_language
        ],
        outputs=output
    )


if __name__ == "__main__":
    app.launch()
