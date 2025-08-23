import importlib.util
import os

import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CORE_PAGES = {
    "Welcome": "welcome.py",
    "Contribution Guide": "contribution_guide.py",
}

APPS_FOLDER = os.path.join(BASE_DIR, "apps")
APPS = {}

if os.path.exists(APPS_FOLDER):
    for f in sorted(os.listdir(APPS_FOLDER)):
        app_path = os.path.join(APPS_FOLDER, f, "app.py")
        if os.path.isdir(os.path.join(APPS_FOLDER, f)) and os.path.exists(
            app_path
        ):
            APPS[f] = app_path

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
        background: linear-gradient(135deg, #f0f4f8, #d9e2ec) !important;
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

core_choice = st.sidebar.radio(
    label="",
    options=list(CORE_PAGES.keys()),
    index=0,
    key="core_radio",
)

script_path = os.path.join(BASE_DIR, CORE_PAGES[core_choice])
is_app = False
label = core_choice

if APPS:
    with st.sidebar.expander("🧪 Developer Apps", expanded=False):
        app_options = ["— Select an app —"] + list(APPS.keys())
        app_choice = st.selectbox(
            "Choose App",
            app_options,
            index=0,
            key="app_select",
        )
        if app_choice and app_choice != "— Select an app —":
            script_path = APPS[app_choice]
            is_app = True
            label = app_choice


def load_script(script_path, is_app=False):
    if is_app:
        module_name = os.path.basename(os.path.dirname(script_path))
    else:
        module_name = os.path.splitext(os.path.basename(script_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if script_path:
    module = load_script(script_path, is_app)
    if hasattr(module, "main"):
        module.main()
    else:
        st.warning(f"⚠️ No `main()` function found in {label}.")
