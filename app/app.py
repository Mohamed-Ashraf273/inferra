import importlib.util
import os

import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Core pages
CORE_PAGES = {}
for page in os.listdir(BASE_DIR):
    if page.endswith(".py") and page != "app.py":
        name_without_ext = os.path.splitext(page)[0]
        name = " ".join(
            word.capitalize() for word in name_without_ext.split("_")
        )
        CORE_PAGES[name] = os.path.join(BASE_DIR, page)


APPS_FOLDER = os.path.join(BASE_DIR, "apps")
APPS = {
    f"{f}": os.path.join(APPS_FOLDER, f, "app.py")
    for f in sorted(os.listdir(APPS_FOLDER))
    if os.path.isdir(os.path.join(APPS_FOLDER, f))
    and os.path.exists(os.path.join(APPS_FOLDER, f, "app.py"))
}

ALL_PAGES = {**CORE_PAGES, **APPS}


if "active_page" not in st.session_state:
    st.session_state.active_page = "Welcome"
if "is_app" not in st.session_state:
    st.session_state.is_app = False

st.sidebar.markdown("## 📚 Pages")

page_options = list(ALL_PAGES.keys())
page_choice = st.sidebar.selectbox(
    "Choose a page",
    options=page_options,
    index=page_options.index(st.session_state.active_page)
    if st.session_state.active_page in page_options
    else 0,
    key="page_select",
)

st.session_state.active_page = page_choice
st.session_state.is_app = page_choice in APPS

script_path = ALL_PAGES[page_choice]
label = page_choice


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
    module = load_script(script_path, st.session_state.is_app)
    if hasattr(module, "main"):
        module.main()
    else:
        st.warning(f"⚠️ No `main()` function found in {label}.")
