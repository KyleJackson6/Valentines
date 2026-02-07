import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Valentine 💖", layout="wide")

# ---------------- State ----------------
st.session_state.setdefault("no_clicks", 0)
st.session_state.setdefault("accepted", False)

# ---------------- Celebration ----------------
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

# ---------------- Growth tuning ----------------
scale = min(1.0 + clicks * 0.12, 2.2)   # YES grows, capped
base_font = 26
font_size = min(base_font + clicks * 2, 44)

# ---------------- CSS ----------------
st.markdown(
    f"""
    <style>
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 1rem !important;
        max-width: 1000px !important;
    }}

    /* We create a "stage" that doesn't reflow */
    #stage {{
        position: relative;
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
    }}

    /* NO stays in normal layout and never moves */
    #no_btn {{
        width: 100% !important;
        min-height: 90px !important;
        font-size: 22px !important;
        border-radius: 24px !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* YES becomes an overlay that does NOT affect layout */
    #yes_btn {{
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;

        width: 100% !important;
        min-height: 110px !important;
        font-size: {font_size}px !important;

        background-color: #ff4b6e !important;
        color: white !important;
        border-radius: 26px !important;
        border: none !important;
        font-weight: 800 !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        transform: scale({scale}) !important;
        transform-origin: top center !important;

        z-index: 9999 !important;
        transition: transform 0.15s ease-in-out, font-size 0.15s ease-in-out;
    }}

    /* Adds space so NO appears below YES, but NO stays fixed */
    #spacer {{
        height: 125px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center;'>Would you be my Valentine? 💘</h1>", unsafe_allow_html=True)

# Stage container (for overlay positioning)
st.markdown("<div id='stage'>", unsafe_allow_html=True)

# YES button (will be overlayed via CSS)
if st.button("YES 💖", key="yes_btn_key", use_container_width=True):
    st.session_state.accepted = True
    st.rerun()

# Spacer keeps NO below the YES area, but YES doesn't push it around
st.markdown("<div id='spacer'></div>", unsafe_allow_html=True)

# NO button (stays still)
if st.button("NO 🙄", key="no_btn_key", use_container_width=True):
    st.session_state.no_clicks += 1
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- JS: assign DOM IDs reliably ----------------
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
