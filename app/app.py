import importlib.util
import os

import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CORE_PAGES = ["welcome.py", "contribution_guide.py"]
core_display_to_file = {}
for f in CORE_PAGES:
    name_without_ext = os.path.splitext(f)[0]
    display_name = " ".join(
        word.capitalize() for word in name_without_ext.split("_")
    )
    core_display_to_file[display_name] = name_without_ext

APPS_FOLDER = os.path.join(BASE_DIR, "apps")
app_files = []
if os.path.exists(APPS_FOLDER):
    app_files = [
        f
        for f in os.listdir(APPS_FOLDER)
        if f.endswith(".py") and not f.startswith("__")
    ]

app_display_to_file = {}
for f in app_files:
    name_without_ext = os.path.splitext(f)[0]
    display_name = " ".join(
        word.capitalize() for word in name_without_ext.split("_")
    )
    app_display_to_file[display_name] = os.path.join("apps", name_without_ext)

st.markdown(
    """
    <style>
    /* Sidebar soft gradient with shadow */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e0eafc, #cfdef3);
        padding-top: 2rem;
        border-radius: 0 20px 20px 0;
        box-shadow: 4px 0 20px rgba(0,0,0,0.08);
        width: 280px !important;
    }

    /* Sidebar header */
    [data-testid="stSidebar"] .css-1d391kg h2 {
        color: #333333;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Flex column for radio options */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Soft gradient radio labels */
    .stRadio > div > label {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 250px !important;
        margin: 0.5rem 0 !important;
        padding: 0.8rem 1rem !important;
        font-size: 16px !important;
        font-weight: bold !important;
        color: #333 !important;
        border-radius: 12px !important;
        cursor: pointer;
        background: linear-gradient(135deg, #f0f4f8, #d9e2ec) 
        !important; /* soft pastel gradient */
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s, background 0.3s;
        text-align: center !important;
    }

    /* Hide default radio circle */
    .stRadio > div > input[type="radio"] {
        display: none !important;
    }

    /* Hover effect */
    .stRadio > div > label:hover {
        background: linear-gradient(135deg, #e0eafc, #cfdef3) !important;
        transform: scale(1.03);
    }

    /* Active/selected radio button */
    .stRadio > div > input:checked + label {
        background: linear-gradient(135deg, #cfd9f0, #e2ebf5) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

selected_core_page = st.sidebar.radio(
    label="",  # no title
    options=list(core_display_to_file.keys()),
    index=list(core_display_to_file.keys()).index("Welcome")
    if "Welcome" in core_display_to_file
    else 0,
)

app_display_names = list(app_display_to_file.keys())
selected_app_page = (
    st.sidebar.selectbox("Select an app", app_display_names)
    if app_display_names
    else None
)

if selected_core_page:
    selected_script = core_display_to_file[selected_core_page]
elif selected_app_page:
    selected_script = app_display_to_file[selected_app_page]
else:
    selected_script = None


def load_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name + ".py")
    spec = importlib.util.spec_from_file_location(
        script_name.replace("/", "_"), script_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if selected_script:
    module = load_script(selected_script)
    if hasattr(module, "main"):
        module.main()
    else:
        st.write("No `main()` function found in this script.")
else:
    st.write("Select a core page or developer app to begin.")
