import streamlit as st


def main():
    # Page configuration
    st.set_page_config(page_title="Inferra", layout="wide")

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            font-family: 'Segoe UI', sans-serif;
        }
        /* Title styling */
        h1 {
            color: #4B0082;
            text-align: center;
            margin-bottom: 0.5em;
        }
        h2 {
            color: #2F4F4F;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        /* Paragraph styling */
        p {
            font-size: 18px;
            line-height: 1.6;
        }
        /* List styling */
        ul {
            font-size: 18px;
            line-height: 1.6;
            margin-left: 2em;
        }
        li {
            margin-bottom: 0.5em;
        }
        /* Box around main content */
        .content-box {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2em;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main content in a styled box
    st.markdown(
        """
        <div class="content-box">
            <h1>Welcome to Inferra 🤖</h1>
            <h2>Inferra is a powerful AI app deployment platform.</h2>
            <p>
            It allows you to take any pre-trained model
            and turn it into a fully functional app in minutes.
            Users can:
            </p>
            <ul>
                <li>Load model architectures and weights directly.</li>
                <li>Import models from Hugging Face or other sources.</li>
                <li>Build custom interfaces to interact with their models.</li>
            </ul>
            <p>
            Inferra is designed for <b>ready-to-use models</b>,
            no training required. 
            Just upload your model, create the UI,
            and run your AI application effortlessly.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
