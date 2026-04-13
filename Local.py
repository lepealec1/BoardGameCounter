import streamlit as st

st.set_page_config(page_title="Game Controller", layout="centered")

st.title("🎮 Game Controller")

# -------------------------
# COLORS
# -------------------------
COLOR_MAP = {
    "Blue": "#BBDEFB",
    "Red": "#FFCDD2",
    "Green": "#C8E6C9",
    "Yellow": "#FFF9C4",
    "Purple": "#E1BEE7",
    "Orange": "#FFE0B2",
    "Pink": "#F8BBD0",
    "Teal": "#B2DFDB",
    "Gray": "#E0E0E0",
    "White": "#FFFFFF",
}

# -------------------------
# SETTINGS
# -------------------------
num_counters = st.number_input("Number of counters", 1, 20, 4)
step = st.number_input("Step", 1, 10, 1)

# -------------------------
# INIT STATE
# -------------------------
if "counters" not in st.session_state:
    st.session_state.counters = {}

if len(st.session_state.counters) != num_counters:
    st.session_state.counters = {
        f"Counter {i+1}": {
            "value": 0,
            "reset": 0,
            "color": ["Blue", "Red", "Green", "Yellow"][i] if i < 4 else "White"
        }
        for i in range(num_counters)
    }

# -------------------------
# GLOBAL RESET
# -------------------------
col1, col2 = st.columns(2)

with col1:
    global_reset = st.number_input("Global reset value", 0, 100, 0)

with col2:
    if st.button("🔄 Reset All"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = global_reset
        st.rerun()

st.divider()

# -------------------------
# STYLES (clean card UI)
# -------------------------
st.markdown("""
<style>
.card {
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    text-align: center;
    border: 1px solid #ddd;
}

.title {
    font-size: 18px;
    font-weight: 600;
}

.value {
    font-size: 42px;
    font-weight: bold;
}

div.stButton > button {
    height: 44px;
    font-size: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# GAME BOARD (ROW CONTROLS)
# -------------------------
for name, data in st.session_state.counters.items():

    color = COLOR_MAP.get(data["color"], "#FFFFFF")

    # CARD DISPLAY
    st.markdown(
        f"""
        <div class="card" style="background:{color}">
            <div class="title">{name}</div>
            <div class="value">{data['value']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CONTROL ROW (THIS IS THE KEY PART)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("➖", key=f"dec_{name}"):
            st.session_state.counters[name]["value"] -= step
            st.rerun()

    with c2:
        if st.button(f"Reset ({data['reset']})", key=f"reset_{name}"):
            st.session_state.counters[name]["value"] = data["reset"]
            st.rerun()

    with c3:
        if st.button("➕", key=f"inc_{name}"):
            st.session_state.counters[name]["value"] += step
            st.rerun()