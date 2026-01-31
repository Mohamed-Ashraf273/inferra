import os
from io import BytesIO
from typing import Any

import requests
from langchain.prompts import ChatPromptTemplate
from langchain.tools import BaseTool


class SoundClassifier(BaseTool):
    name: str = "sound_classifier"
    description: str = (
        "Classifies sounds into different categories. "
        "Use this tool when the user asks for sound/audio/voice classification "
        "or analysis or to identify a given sound."
    )

    llm: Any = None
    system_prompt: str = None

    prompt: ChatPromptTemplate = None
    chain: Any = None

    loaded_audio: Any = None

    def __init__(self, loaded_audio, llm: Any):
        super().__init__()
        self.llm = llm
        self.loaded_audio = loaded_audio
        self.system_prompt = """You are a helpful assistant 
        that explains sound classifications.
        When given a sound category, provide a clear, 
        concise explanation about what that sound is.
        Keep your response brief and informative."""

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    "The audio "
                    "has been classified as: {category}\n\nUser question: "
                    "{input}\n\nProvide a helpful response.",
                ),
            ]
        )
        self.chain = self.prompt | self.llm

    def _run(self, user_input: str) -> str:
        if self.loaded_audio is None:
            return "Upload an audio file first using the upload button."

        url = "https://mohamedahraf273-au57-sound-classifier.hf.space/predict"

        try:
            audio_file = BytesIO(self.loaded_audio)
            files = {"file": ("audio.wav", audio_file, "audio/wav")}
            res = requests.post(url, files=files, timeout=30)

            if res.status_code != 200:
                return f"Error occurred. Status code: {res.status_code}"

            result = res.json()
            prediction = result.get("pred_class", "Unknown")
            prediction_with_ext = os.path.splitext(prediction)[0]
            prediction = " ".join(
                word.capitalize() for word in prediction_with_ext.split("_")
            )

        except requests.exceptions.RequestException as e:
            return f"Network error while classifying audio: {str(e)}"
        except Exception as e:
            return f"Error processing audio: {str(e)}"

        try:
            response = self.chain.invoke(
                {
                    "input": user_input,
                    "category": prediction,
                }
            )
            return response.content.strip()
        except Exception:
            return f"The audio has been classified as: {prediction}"
