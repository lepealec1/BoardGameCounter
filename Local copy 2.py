import streamlit as st

st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Counter")

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
    base_colors = ["Blue", "Red", "Green", "Yellow"]

    st.session_state.counters = {
        f"Counter {i+1}": {
            "value": 0,
            "reset": 0,
            "color": base_colors[i] if i < 4 else "White"
        }
        for i in range(num_counters)
    }

if "selected" not in st.session_state:
    st.session_state.selected = list(st.session_state.counters.keys())[0]

# -------------------------
# CLICK TO SELECT COUNTER
# -------------------------
st.markdown("### Select Counter")

cols = st.columns(len(st.session_state.counters))

for i, name in enumerate(st.session_state.counters.keys()):
    with cols[i]:
        if st.button(name, key=f"select_{name}"):
            st.session_state.selected = name
            st.rerun()

st.markdown(f"### Selected: **{st.session_state.selected}**")

# -------------------------
# GLOBAL CONTROLS (ONLY ONE SET)
# -------------------------
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("➖"):
        st.session_state.counters[st.session_state.selected]["value"] -= step
        st.rerun()

with c2:
    if st.button("0"):
        st.session_state.counters[st.session_state.selected]["value"] = \
            st.session_state.counters[st.session_state.selected]["reset"]
        st.rerun()

with c3:
    if st.button("➕"):
        st.session_state.counters[st.session_state.selected]["value"] += step
        st.rerun()

# -------------------------
# GLOBAL RESET
# -------------------------
global_reset = st.number_input("Global reset value", 0, 100, 0)

if st.button("🔄 Reset All"):
    for k in st.session_state.counters:
        st.session_state.counters[k]["value"] = global_reset
    st.rerun()

st.divider()

# -------------------------
# DISPLAY COUNTERS
# -------------------------
for name, data in st.session_state.counters.items():

    color = COLOR_MAP.get(data["color"], "#FFFFFF")
    selected = "⭐" if name == st.session_state.selected else ""

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:14px;
            border-radius:16px;
            margin-bottom:10px;
            border:3px solid {'black' if selected else '#ddd'};
        ">
            <h3 style="text-align:center;margin:0;">
                {selected} {name}
            </h3>
            <div style="text-align:center;font-size:42px;font-weight:bold;">
                {data['value']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )