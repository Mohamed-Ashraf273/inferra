import tempfile

import requests
import streamlit as st


def main():
    st.set_page_config(
        page_title="AU57 Sound Classifier",
        page_icon="🎵",
        layout="centered",
    )

    st.markdown(
        """
        <style>
        /* Global page background */
        .stApp {
            background: linear-gradient(135deg, #e0f7fa, #e1bee7);
            font-family: 'Segoe UI', sans-serif;
        }

        /* Title styling */
        h1 {
            text-align: center;
            font-size: 3rem !important;
            background: -webkit-linear-gradient(45deg, #4CAF50, #3f51b5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            margin-bottom: 1rem;
        }

        /* Subtitle / markdown text */
        .stMarkdown p {
            text-align: center;
            font-size: 1.1rem;
            color: #333333;
        }

        /* File uploader box */
        [data-testid="stFileUploader"] {
            border: 3px dashed #3f51b5;
            border-radius: 15px;
            padding: 20px;
            background-color: rgba(255,255,255,0.7);
            transition: 0.3s ease-in-out;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #4CAF50;
            background-color: rgba(255,255,255,0.9);
        }

        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, #3f51b5, #4CAF50);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .stButton button:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #4CAF50, #3f51b5);
            box-shadow: 0 6px 14px rgba(0,0,0,0.3);
        }

        /* Success & error messages */
        .stSuccess {
            border-radius: 12px;
            padding: 1rem;
            font-size: 1.1rem;
        }
        .stError {
            border-radius: 12px;
            padding: 1rem;
            font-size: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🎶 AU57 Sound Classifier")
    st.markdown("Upload an audio file and let the model classify it!")

    uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        st.audio(uploaded_file, format="audio/wav")

        if st.button("🔍 Classify Sound"):
            with st.spinner("Running ... ⏳"):
                url = "https://mohamedahraf273-au57-sound-classifier.hf.space/predict"
                files = {"file": open(tmp_path, "rb")}
                response = requests.post(url, files=files)

                if response.status_code == 200:
                    try:
                        result = response.json()
                        st.success("✅ Classified successfully!")
                        prediction = result["pred_class"]

                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(
                                135deg, #4CAF50, #2E7D32
                                );
                                padding: 20px;
                                border-radius: 15px;
                                text-align: center;
                                color: white;
                                font-size: 28px;
                                font-weight: bold;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                                margin-top: 20px;
                            ">
                                🎵 Prediction: {prediction}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    except Exception:
                        st.error("⚠️ Couldn't parse JSON response.")
                        st.text(response.text)
                else:
                    st.error(f"❌ Error {response.status_code}")
                    st.text(response.text)


if __name__ == "__main__":
    main()
