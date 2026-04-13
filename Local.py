import streamlit as st

st.set_page_config(page_title="Game Counter", layout="centered")

st.title("🎲 Game Mode Counter")

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
# INIT
# -------------------------
num_counters = int(st.number_input("Number of counters", 1, 50, 4))
step = st.number_input("Step size", 1, 10, 1)

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
# GLOBAL CONTROLS
# -------------------------
c1, c2 = st.columns(2)

with c1:
    global_reset = st.number_input("Global reset", 0, 100, 0)

with c2:
    if st.button("🔄 Reset All"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = global_reset
        st.rerun()

st.divider()

# -------------------------
# MOBILE STYLES
# -------------------------
st.markdown("""
<style>
.card {
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 14px;
    text-align: center;
    border: 1px solid #ddd;
}

.title {
    font-size: 18px;
    font-weight: 600;
}

.value {
    font-size: 48px;
    font-weight: bold;
    margin: 6px 0;
}

/* BIG TOUCH BUTTONS */
button {
    height: 48px !important;
    font-size: 16px !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# RENDER COUNTERS
# -------------------------
for name, data in st.session_state.counters.items():

    color = COLOR_MAP.get(data["color"], "#FFFFFF")

    # VISUAL CARD
    st.markdown(
        f"""
        <div class="card" style="background:{color}">
            <div class="title">{name}</div>
            <div class="value">{data['value']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # GAME ACTIONS
    # -------------------------

    col1, col2, col3 = st.columns([1, 2, 1])

    # ➖ subtract
    with col1:
        if st.button("➖", key=f"minus_{name}"):
            st.session_state.counters[name]["value"] -= step
            st.rerun()

    # 🔄 reset
    with col2:
        if st.button(f"Reset ({data['reset']})", key=f"reset_{name}"):
            st.session_state.counters[name]["value"] = data["reset"]
            st.rerun()

    # ➕ add
    with col3:
        if st.button("➕", key=f"plus_{name}"):
            st.session_state.counters[name]["value"] += step
            st.rerun()