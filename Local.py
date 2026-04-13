import streamlit as st

st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Mobile Counter")

# -------------------------
# COLOR SYSTEM
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

COLOR_NAMES = list(COLOR_MAP.keys())

# -------------------------
# INIT
# -------------------------
num_counters = int(st.number_input("Number of counters", 1, 50, 4))

if "counters" not in st.session_state:
    st.session_state.counters = {}

if len(st.session_state.counters) != num_counters:
    new_state = {}

    for i in range(num_counters):
        name = f"Counter {i+1}" if i >= 4 else f"Counter {i+1}"
        color = ["Blue", "Red", "Green", "Yellow"][i] if i < 4 else "White"

        new_state[name] = {
            "value": 0,
            "reset": 0,
            "color": color
        }

    st.session_state.counters = new_state

# -------------------------
# GLOBAL CONTROLS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    step = st.number_input("Step", 1, 10, 1)

with col2:
    global_reset = st.number_input("Global reset value", 0, 100, 0)

c1, c2 = st.columns(2)

with c1:
    if st.button("🔄 Global Reset"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = global_reset
        st.rerun()

with c2:
    if st.button("🎯 Reset All"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = st.session_state.counters[k]["reset"]
        st.rerun()

st.divider()

# -------------------------
# STYLES (MOBILE CARD UI)
# -------------------------
st.markdown("""
<style>
.counter-card {
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 14px;
    border: 1px solid #ddd;
    text-align: center;
    cursor: pointer;
    user-select: none;
}

.counter-title {
    font-size: 18px;
    margin-bottom: 6px;
    font-weight: 600;
}

.counter-value {
    font-size: 44px;
    font-weight: bold;
}

.reset-btn button {
    width: 100%;
    margin-top: 6px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# RENDER COUNTERS (MOBILE STYLE)
# -------------------------
for name, data in st.session_state.counters.items():

    color = COLOR_MAP.get(data["color"], "#FFFFFF")

    # CARD (CLICK AREA = +1)
    if st.button(
        f"{name} | {data['value']}",
        key=f"tap_{name}"
    ):
        st.session_state.counters[name]["value"] += step
        st.rerun()

    # VISUAL CARD
    st.markdown(
        f"""
        <div class="counter-card" style="background:{color}">
            <div class="counter-title">{name}</div>
            <div class="counter-value">{data['value']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # RESET BUTTON (fallback instead of long-press)
    if st.button(f"Reset to {data['reset']}", key=f"reset_{name}"):
        st.session_state.counters[name]["value"] = data["reset"]
        st.rerun()