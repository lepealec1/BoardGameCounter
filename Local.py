import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Game Counter (Fixed + Hold Mode)")

# -------------------------
# SETTINGS
# -------------------------
num_counters = int(st.number_input("Number of counters", 1, 10, 4))

# -------------------------
# SAFE STATE INIT
# -------------------------
if "counter_values" not in st.session_state:
    st.session_state.counter_values = [20] * num_counters

if "counter_hold" not in st.session_state:
    st.session_state.counter_hold = [None] * num_counters  # "up", "down", None


# -------------------------
# RESIZE SAFE FUNCTION
# -------------------------
def resize(lst, default):
    if not isinstance(lst, list):
        lst = [default]

    lst = list(lst)

    if len(lst) < num_counters:
        lst += [default] * (num_counters - len(lst))

    return lst[:num_counters]


st.session_state.counter_values = resize(st.session_state.counter_values, 20)
st.session_state.counter_hold = resize(st.session_state.counter_hold, None)

# -------------------------
# AUTO REFRESH (only when holding)
# -------------------------
if any(h is not None for h in st.session_state.counter_hold):
    st_autorefresh(interval=120, key="hold_refresh")

    for i in range(num_counters):
        if st.session_state.counter_hold[i] == "up":
            st.session_state.counter_values[i] += 1
        elif st.session_state.counter_hold[i] == "down":
            st.session_state.counter_values[i] -= 1

# -------------------------
# UI
# -------------------------
for i in range(num_counters):

    st.markdown(f"### Counter {i+1}")

    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

    # ➖ single click
    with col1:
        if st.button("➖", key=f"dec_{i}"):
            st.session_state.counter_values[i] -= 1

    # display
    with col2:
        st.markdown(
            f"<div style='text-align:center;font-size:28px;font-weight:bold'>"
            f"{st.session_state.counter_values[i]}</div>",
            unsafe_allow_html=True
        )

    # ➕ single click
    with col3:
        if st.button("➕", key=f"inc_{i}"):
            st.session_state.counter_values[i] += 1

    # HOLD controls
    with col4:
        if st.session_state.counter_hold[i] is None:
            if st.button("⏱+", key=f"hold_up_{i}"):
                st.session_state.counter_hold[i] = "up"

            if st.button("⏱-", key=f"hold_down_{i}"):
                st.session_state.counter_hold[i] = "down"
        else:
            if st.button("⛔", key=f"stop_{i}"):
                st.session_state.counter_hold[i] = None

    st.divider()