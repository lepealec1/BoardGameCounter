import streamlit as st

st.set_page_config(page_title="Game Controller", layout="centered")

st.title("🎮 Counter App")

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
num_counters = st.number_input("Counters", 1, 20, 4)
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
    global_reset = st.number_input("Global reset", 0, 100, 0)

with col2:
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
    font-size: 44px;
    font-weight: bold;
}

/* IOS SAFE FLEX BUTTON ROW */
.btn-row {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 18px;
}

.btn-row button {
    flex: 1;
    height: 44px !important;
    font-size: 16px !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# RENDER
# -------------------------
for name, data in st.session_state.counters.items():

    color = COLOR_MAP.get(data["color"], "#fff")

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
    # SAFE BUTTON ROW (NO COLUMNS)
    # -------------------------
    st.markdown('<div class="btn-row">', unsafe_allow_html=True)

    if st.button("➖", key=f"dec_{name}"):
        st.session_state.counters[name]["value"] -= step
        st.rerun()

    if st.button(f"Reset ({data['reset']})", key=f"reset_{name}"):
        st.session_state.counters[name]["value"] = data["reset"]
        st.rerun()

    if st.button("➕", key=f"inc_{name}"):
        st.session_state.counters[name]["value"] += step
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)