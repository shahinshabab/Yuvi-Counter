"""Run with: streamlit run streamlit_app.py"""
import streamlit as st

st.set_page_config(page_title="Yuvi Counter", page_icon="🔢", layout="centered")
st.markdown("""
<style>
.block-container {max-width: 480px; padding-top: 2rem;}
.stButton button {min-height: 56px; border-radius: 14px;}
.counter-value {font-size: clamp(40px, 18vw, 96px); font-weight: 700;
text-align: center; padding: 32px 12px; border: 1px solid #ddd;
border-radius: 24px; margin: 20px 0; overflow-wrap: anywhere;}
</style>
""", unsafe_allow_html=True)

if "mode" not in st.session_state:
    st.session_state.mode = "home"
    st.session_state.count = 0

def navigate(mode):
    st.session_state.mode = mode
    st.session_state.count = 0

def change(delta):
    limit = 25 if st.session_state.mode == "alphabet" else 9007199254740991
    st.session_state.count = max(0, min(limit, st.session_state.count + delta))

def reset():
    st.session_state.count = 0

if st.session_state.mode == "home":
    st.title("Yuvi Counter")
    st.write("Choose numbers or letters to get started.")
    st.button("Numeric", key="numeric", on_click=navigate, args=("numeric",),
              use_container_width=True, type="primary")
    st.button("Alphabet", key="alphabet", on_click=navigate, args=("alphabet",),
              use_container_width=True)
else:
    st.button("← Home", key="home", on_click=navigate, args=("home",))
    alphabet = st.session_state.mode == "alphabet"
    st.title("Alphabet" if alphabet else "Numeric")
    count = st.session_state.count
    value = chr(65 + count) if alphabet else str(count)
    st.markdown(f'<div class="counter-value" role="status" aria-live="polite">{value}</div>',
                unsafe_allow_html=True)
    if alphabet:
        st.caption(f"Letter {count + 1} of 26")
    plus, minus, clear = st.columns(3)
    limit = 25 if alphabet else 9007199254740991
    plus.button("+", key="plus", on_click=change, args=(1,),
                disabled=count == limit, use_container_width=True, type="primary")
    minus.button("−", key="minus", on_click=change, args=(-1,),
                 disabled=count == 0, use_container_width=True)
    clear.button("Reset", key="reset", on_click=reset, use_container_width=True)
