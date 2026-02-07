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
        <h2 style="text-align:center;">TANKS POOKIE</h2>
        """,
        unsafe_allow_html=True
    )
    st.stop()

clicks = st.session_state.no_clicks

# ----- Gentle growth tuning -----
font_size = 22 + clicks * 4          # small increases
pad_y = 14 + clicks * 1              # tiny vertical padding change
pad_x = 24 + clicks * 5              # small horizontal padding change

# Expand DOWN using height (gentle)
base_height = 46                     # approx normal button height
extra_height = clicks * 30           # gentle downward growth
min_height = base_height + extra_height

# Expand RIGHT using overlap (gentle)
COVER_START = 1
cover_mode = clicks >= COVER_START
overlap_px = max(0, (clicks - COVER_START + 1) * 50)  # small overlap per click

cover_css = ""
if cover_mode:
    cover_css = f"""
    #yes_btn {{
        position: relative !important;
        z-index: 9999 !important;
        width: calc(100% + {overlap_px}px) !important;
        margin-right: -{overlap_px}px !important;
    }}
    """

st.markdown(
    f"""
    <style>
    #yes_btn {{
        font-size: {font_size}px !important;
        padding: {pad_y}px {pad_x}px !important;
        min-height: {min_height}px !important;   /* grows DOWN gently */
        background-color: #ff4b6e !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        font-weight: 800 !important;
        transition: all 0.12s ease-in-out !important;
        width: 100% !important;
        white-space: nowrap !important;
    }}

    #no_btn {{
        font-size: 18px !important;
        padding: 14px 18px !important;
        border-radius: 14px !important;
    }}

    {cover_css}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align:center;'>Would you be my Valentine? 💘</h1>",
    unsafe_allow_html=True
)

col_yes, col_no = st.columns(2)

with col_yes:
    if st.button("YES 💖", key="yes_btn_key", use_container_width=True):
        st.session_state.accepted = True
        st.rerun()

with col_no:
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
