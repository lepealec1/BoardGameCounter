import streamlit as st

st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Counter Matrix")

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
# INIT COUNTERS
# -------------------------
num_counters = int(st.number_input("Number of counters", 1, 20, 4))
step = st.number_input("Step", 1, 10, 1)

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
    global_reset_value = st.number_input("Global reset value", 0, 100, 0)

with col2:
    if st.button("🔄 Reset All"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = global_reset_value
        st.rerun()

st.divider()

# -------------------------
# DISPLAY CARDS ONLY (NO BUTTONS)
# -------------------------
for name, data in st.session_state.counters.items():

    color = COLOR_MAP.get(data["color"], "#FFFFFF")

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:16px;
            border-radius:16px;
            margin-bottom:10px;
            text-align:center;
            border:1px solid #ddd;
        ">
            <div style="font-size:18px;font-weight:600;">{name}</div>
            <div style="font-size:46px;font-weight:bold;">{data['value']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# MATRIX CONTROLS
# -------------------------
st.subheader("Controls Matrix")

names = list(st.session_state.counters.keys())

for name in names:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("➖", key=f"dec_{name}"):
            st.session_state.counters[name]["value"] -= step
            st.rerun()

    with col2:
        if st.button(f"Reset ({st.session_state.counters[name]['reset']})", key=f"reset_{name}"):
            st.session_state.counters[name]["value"] = st.session_state.counters[name]["reset"]
            st.rerun()

    with col3:
        if st.button("➕", key=f"inc_{name}"):
            st.session_state.counters[name]["value"] += step
            st.rerun()