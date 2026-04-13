import streamlit as st

st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Board Game Counter")

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
# DEFAULTS
# -------------------------
DEFAULT_NAMES = ["Counter 1", "Counter 2", "Counter 3", "Counter 4"]
DEFAULT_COLORS = ["Blue", "Red", "Green", "Yellow"]
DEFAULT_COUNTERS = 4

# -------------------------
# GRID INPUTS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    rows = st.number_input("Rows", min_value=1, max_value=10, value=2, step=1)

with col2:
    cols = st.number_input("Columns", min_value=1, max_value=10, value=2, step=1)

grid_size = rows * cols

# -------------------------
# COUNTER COUNT
# -------------------------
num_counters = int(
    st.number_input(
        "Number of counters",
        min_value=1,
        max_value=50,
        value=DEFAULT_COUNTERS,
        step=1
    )
)

# -------------------------
# WARNING
# -------------------------
if grid_size < num_counters:
    st.warning(
        f"⚠️ Grid size ({grid_size}) is too small for {num_counters} counters. "
        "Some counters will not be visible."
    )

# -------------------------
# INIT STATE
# -------------------------
if "counters" not in st.session_state:
    st.session_state.counters = {}

if len(st.session_state.counters) != num_counters:
    new_state = {}

    for i in range(num_counters):

        if i < 4:
            name = DEFAULT_NAMES[i]
            color = DEFAULT_COLORS[i]
        else:
            name = f"Counter {i+1}"
            color = "Grey"

        new_state[name] = {
            "value": 0,
            "reset": 0,
            "color": color
        }

    st.session_state.counters = new_state

# -------------------------
# CUSTOMIZE
# -------------------------
with st.expander("✏️ Customize Counters", expanded=False):

    items = list(st.session_state.counters.items())
    new_state = {}

    for i, (old_name, data) in enumerate(items):

        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            new_name = st.text_input(
                f"Name {i+1}",
                value=old_name,
                key=f"name_{i}"
            )

        with col2:
            color_name = st.selectbox(
                "Color",
                COLOR_NAMES,
                index=COLOR_NAMES.index(data["color"]) if data["color"] in COLOR_NAMES else 0,
                key=f"color_{i}"
            )

        with col3:
            reset_value = st.number_input(
                "Reset",
                value=data.get("reset", 0),
                step=1,
                key=f"resetval_{i}"
            )

        new_state[new_name] = {
            "value": data["value"],
            "reset": reset_value,
            "color": color_name
        }

    st.session_state.counters = new_state

st.divider()

# -------------------------
# GLOBAL CONTROLS
# -------------------------
col1, col2 = st.columns([2, 2])

with col1:
    step = st.number_input("Step", value=1, step=1)

with col2:
    global_reset_value = st.number_input(
        "Global reset value",
        value=0,
        step=1
    )

col3, col4 = st.columns(2)

with col3:
    if st.button("🔄 Global Reset"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = global_reset_value
        st.rerun()

with col4:
    if st.button("🎯 Reset All (Custom)"):
        for k in st.session_state.counters:
            st.session_state.counters[k]["value"] = st.session_state.counters[k]["reset"]
        st.rerun()

st.divider()

# -------------------------
# STYLES
# -------------------------
st.markdown("""
<style>
.counter-card {
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 12px;
    border: 1px solid #ddd;
}

.big-number {
    font-size: 42px;
    text-align: center;
    font-weight: bold;
    margin: 10px 0;
}

div.stButton > button {
    height: 50px;
    font-size: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# GRID RENDER
# -------------------------
items = list(st.session_state.counters.items())

index = 0

for r in range(rows):

    cols_ui = st.columns(cols)

    for c in range(cols):

        if index >= len(items):
            break

        name, data = items[index]
        value = data["value"]
        color_hex = COLOR_MAP.get(data["color"], "#FFFFFF")

        with cols_ui[c]:

            st.markdown(
                f"""
                <div class="counter-card" style="background-color:{color_hex};">
                    <h4 style="text-align:center; margin:0;">{name}</h4>
                    <div class="big-number">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                if st.button("➖", key=f"dec_{name}"):
                    st.session_state.counters[name]["value"] -= step
                    st.rerun()

            with c2:
                if st.button("0", key=f"reset_{name}"):
                    st.session_state.counters[name]["value"] = st.session_state.counters[name]["reset"]
                    st.rerun()

            with c3:
                if st.button("➕", key=f"inc_{name}"):
                    st.session_state.counters[name]["value"] += step
                    st.rerun()

        index += 1