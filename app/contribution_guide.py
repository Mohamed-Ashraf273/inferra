import streamlit as st


def main():
    st.set_page_config(page_title="Contribution Guide", layout="wide")

    # CSS styling
    st.markdown(
        """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        color: #4B0082;
        text-align: center;
        font-size: 40px;
        margin-bottom: 0.5em;
    }
    h2 {
        color: #2F4F4F;
        font-size: 28px;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    h3 {
        color: #2F4F4F;
        font-size: 24px;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    p, li {
        font-size: 18px;
        line-height: 1.8;
    }
    ul, ol {
        margin-left: 2em;
    }
    li {
        margin-bottom: 0.5em;
    }
    pre {
        background-color: #e8e8e8;
        padding: 1em;
        border-radius: 8px;
        overflow-x: auto;
        font-size: 16px;
    }
    code {
        font-family: 'Courier New', monospace;
    }
    .content-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2em;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Main content with proper Bash code blocks
    st.markdown(
        """<div class="content-box">
<h1>Contribution Guide</h1>

<h2>Welcome to the Inferra Contribution Guide</h2>
<p>Thank you for your interest in contributing to Inferra! 
We welcome all kinds of contributions, including bug reports, 
feature requests, code improvements, and documentation.</p>

<h2>How to Contribute</h2>
<ol>
<li><strong>Fork the repository</strong> and create
 your branch from <code>main</code>.</li>
<li><strong>Clone your fork</strong> and set up
 the development environment:
<pre><code class="language-bash">
git clone https://github.com/your-username/inferra.git
cd inferra
pip install -r requirements.txt
</code></pre>
</li>
<li><strong>Create a new branch</strong> for your feature or bugfix:
<pre><code class="language-bash">
git checkout -b my-feature
</code></pre>
</li>
<li><strong>Make your changes</strong>, following these guidelines:
<ul>
<li>Run pre-commit hooks before staging your changes:
<pre><code class="language-bash">
pre-commit run --all-files --hook-stage manual
</code></pre>
</li>
<li>Add new model architectures in <code>src/models</code> 
using <code>torch_model</code>
 (PyTorch) or <code>tensorflow_model</code> (TensorFlow).</li>
<li>If you create new layers, add them under <code>src/layers/</code> 
(either <code>torch_layers</code> or <code>tensorflow_layers</code>).</li>
<li>Create your own app in the <code>app/apps</code> directory.</li>
<li>Upload your trained model or weights to cloud 
storage (Google Drive, AWS S3, etc.)
 and load them in your app. No large model files 
 should be included in the repo.</li>
</ul>
</li>
<li><strong>Commit and push</strong> your changes:
<pre><code class="language-bash">
git add .
git commit -m "Describe your changes"
git push origin my-feature
</code></pre>
</li>
<li><strong>Open a Pull Request</strong> on GitHub 
and describe your changes.</li>
</ol>

<h2>Code Style</h2>
<ul>
<li>Follow <a href="https://pep8.org/" target="_blank">PEP8</a> 
guidelines for Python code.</li>
<li>Write clear, concise commit messages.</li>
<li>Add or update tests as appropriate.</li>
</ul>

<h2>Reporting Issues</h2>
<p>If you find a bug or have a feature request, 
please open an issue on GitHub with detailed information.</p>

<hr>
<p>Happy coding! 🚀</p>
</div>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
