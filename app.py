import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Valentine 💖", layout="centered")

# ----- State -----
st.session_state.setdefault("no_clicks", 0)
st.session_state.setdefault("accepted", False)

# ----- Celebration -----
if st.session_state.accepted:
    st.balloons()
    st.markdown(
        """
        <h1 style="text-align:center; color:#ff4b6e;">YAYYYYY 💖💖💖</h1>
        <h2 style="text-align:center;">Best decision ever 😌✨</h2>
        """,
        unsafe_allow_html=True
    )
    st.stop()

clicks = st.session_state.no_clicks

# ----- Growth tuning (all directions) -----
# scale grows a little each NO press; cap it so it doesn't force scrolling forever
scale = min(1.0 + clicks * 0.12, 2.2)

# overlap grows so YES starts covering the NO button below it
overlap = min(clicks * 18, 140)  # px pulled into the NO area; capped

# small baseline button sizes so they fit on phones
base_font = 20
font_size = min(base_font + clicks * 2, 34)

st.markdown(
    f"""
    <style>
    /* Reduce top padding so everything fits on mobile without scroll */
    .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 1rem !important;
    }}

    /* YES button: scales in ALL directions */
    #yes_btn {{
        width: 100% !important;
        font-size: {font_size}px !important;
        padding: 14px 18px !important;
        background-color: #ff4b6e !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        font-weight: 800 !important;

        position: relative !important;
        z-index: 9999 !important;

        transform: scale({scale}) !important;
        transform-origin: top center !important;

        /* Pull YES downward to cover the NO button beneath it */
        margin-bottom: -{overlap}px !important;

        transition: transform 0.12s ease-in-out, margin-bottom 0.12s ease-in-out, font-size 0.12s ease-in-out;
    }}

    /* NO button stays normal */
    #no_btn {{
        width: 100% !important;
        font-size: 18px !important;
        padding: 14px 18px !important;
        border-radius: 14px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----- UI -----
st.markdown("<h1 style='text-align:center;'>Would you be my Valentine? 💘</h1>", unsafe_allow_html=True)

# stacked on purpose (works great on phone)
if st.button("YES 💖", key="yes_btn_key", use_container_width=True):
    st.session_state.accepted = True
    st.rerun()

if st.button("NO 🙄", key="no_btn_key", use_container_width=True):
    st.session_state.no_clicks += 1
    st.rerun()

# ----- JS: assign DOM IDs reliably -----
components.html(
    """
    <script>
    const doc = window.parent.document;
    const buttons = Array.from(doc.querySelectorAll("button"));
    for (const b of buttons) {
      const t = (b.innerText || "").toUpperCase();
      if (t.includes("YES")) b.id = "yes_btn";
      if (t.includes("NO")) b.id = "no_btn";
    }
    </script>
    """,
    height=0,
    width=0,
)


