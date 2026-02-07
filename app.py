import streamlit as st
import streamlit.components.v1 as components

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Valentine 💖",
    layout="wide"   # makes buttons longer on all screens
)

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
# YES grows smoothly in all directions
scale = min(1.0 + clicks * 0.12, 2.2)     # scale growth (capped)
overlap = min(clicks * 22, 160)           # covers NO vertically (capped)

base_font = 24
font_size = min(base_font + clicks * 2, 40)

# ---------------- CSS ----------------
st.markdown(
    f"""
    <style>
    /* Reduce vertical padding so no scrolling on phones */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 1100px !important;
    }}

    /* YES button */
    #yes_btn {{
        width: 100% !important;
        font-size: {font_size}px !important;
        padding: 22px 28px !important;
        background-color: #ff4b6e !important;
        color: white !important;
        border-radius: 22px !important;
        border: none !important;
        font-weight: 800 !important;

        position: relative !important;
        z-index: 9999 !important;

        transform: scale({scale}) !important;
        transform-origin: top center !important;

        /* Pull YES down to cover NO */
        margin-bottom: -{overlap}px !important;

        transition: transform 0.15s ease-in-out,
                    margin-bottom 0.15s ease-in-out,
                    font-size 0.15s ease-in-out;
    }}

    /* NO button (never grows) */
    #no_btn {{
        width: 100% !important;
        font-size: 20px !important;
        padding: 20px 28px !important;
        border-radius: 20px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- UI ----------------
st.markdown(
    "<h1 style='text-align:center;'>Would you be my Valentine? 💘</h1>",
    unsafe_allow_html=True
)

# Buttons are stacked ON PURPOSE (perfect for mobile)
if st.button("YES 💖", key="yes_btn_key", use_container_width=True):
    st.session_state.accepted = True
    st.rerun()

if st.button("NO 🙄", key="no_btn_key", use_container_width=True):
    st.session_state.no_clicks += 1
    st.rerun()

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
