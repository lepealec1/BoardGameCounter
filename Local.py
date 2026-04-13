
import streamlit as st
st.markdown("""
<style>

/* SAFE wrapper spacing only */
div[data-testid="stNumberInput"] {
    margin-bottom: 18px;
}

/* input text ONLY */
div[data-testid="stNumberInput"] input {
    font-size: 26px !important;
    text-align: center;
}

/* buttons ONLY (no height forcing on container) */
div[data-testid="stNumberInput"] button {
    font-size: 26px !important;
    width: 60px !important;
    height: 60px !important;
    border-radius: 12px !important;
}

/* prevent weird flex stretching */
div[data-testid="stNumberInput"] > div {
    align-items: center !important;
    overflow: visible !important;
}

</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Counter App")

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

COLOR_NAMES = list(COLOR_MAP.keys())

# -------------------------
# SETTINGS
# -------------------------
num_counters = int(st.number_input("Number of counters", 1, 20, 4))

# -------------------------
# INIT STATE
# -------------------------
if "counter_values" not in st.session_state:
    st.session_state.counter_values = [20] * num_counters

if "counter_names" not in st.session_state:
    st.session_state.counter_names = [f"Counter {i+1}" for i in range(num_counters)]

if "counter_colors" not in st.session_state:
    base = ["Blue", "Red", "Green", "Yellow"]
    st.session_state.counter_colors = (base * num_counters)[:num_counters]

if "counter_steps" not in st.session_state:
    st.session_state.counter_steps = [1] * num_counters


# -------------------------
# RESIZE SAFE
# -------------------------
def resize(lst, default):
    lst = list(lst)
    if len(lst) < num_counters:
        lst += [default] * (num_counters - len(lst))
    return lst[:num_counters]


st.session_state.counter_values = resize(st.session_state.counter_values, 20)
st.session_state.counter_names = resize(st.session_state.counter_names, "Counter")
st.session_state.counter_colors = resize(st.session_state.counter_colors, "White")
st.session_state.counter_steps = resize(st.session_state.counter_steps, 1)

# -------------------------
# CUSTOMIZE
# -------------------------
with st.expander("✏️ Customize Counters"):
    for i in range(num_counters):

        st.session_state.counter_names[i] = st.text_input(
            "Name",
            value=st.session_state.counter_names[i],
            key=f"name_{i}"
        )

        st.session_state.counter_colors[i] = st.selectbox(
            "Color",
            COLOR_NAMES,
            index=COLOR_NAMES.index(st.session_state.counter_colors[i])
            if st.session_state.counter_colors[i] in COLOR_NAMES else 0,
            key=f"color_{i}"
        )

        st.session_state.counter_steps[i] = st.number_input(
            "Step",
            min_value=1,
            max_value=100,
            value=int(st.session_state.counter_steps[i]),
            key=f"step_{i}"
        )

# -------------------------
# DISPLAY (FIXED SYNC)
# -------------------------
for i in range(num_counters):
    # ✅ number_input owns state
    st.number_input(
        "",
        key=f"value_{i}",
        step=st.session_state.counter_steps[i]
    )

    # ✅ sync AFTER widget
    st.session_state.counter_values[i] = st.session_state[f"value_{i}"]
    name = st.session_state.counter_names[i]
    value = st.session_state.counter_values[i]
    color = COLOR_MAP.get(st.session_state.counter_colors[i], "#FFFFFF")

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:16px;
            border-radius:16px;
            border:1px solid #ddd;
            margin-bottom:10px;
            text-align:center;
        ">
            <div style="font-size:18px;font-weight:600;">
                {name} <br>
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    