import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Board Game Counter", layout="centered")

st.title("🎲 Game Counter (Hold Mode)")

# -------------------------
# SETTINGS
# -------------------------
num_counters = int(st.number_input("Number of counters", 1, 10, 4))

# -------------------------
# STATE INIT
# -------------------------
if "values" not in st.session_state:
    st.session_state.values = [20] * num_counters

if "hold" not in st.session_state:
    st.session_state.hold = [None] * num_counters  # ("up", "down", None)

# -------------------------
# RESIZE SAFE
# -------------------------
def resize(lst, default):
    lst = list(lst)
    if len(lst) < num_counters:
        lst += [default] * (num_counters - len(lst))
    return lst[:num_counters]

st.session_state.values = resize(st.session_state.values, 20)
st.session_state.hold = resize(st.session_state.hold, None)

# -------------------------
# AUTO REFRESH (for hold mode)
# -------------------------
if any(h is not None for h in st.session_state.hold):
    st_autorefresh(interval=120, key="hold_refresh")

    # apply hold actions
    for i in range(num_counters):
        if st.session_state.hold[i] == "up":
            st.session_state.values[i] += 1
        elif st.session_state.hold[i] == "down":
            st.session_state.values[i] -= 1

# -------------------------
# UI
# -------------------------
for i in range(num_counters):

    st.markdown(f"### Counter {i+1}")

    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

    # ➖ single click
    with col1:
        if st.button("➖", key=f"dec_{i}"):
            st.session_state.values[i] -= 1

    # value display
    with col2:
        st.markdown(
            f"<div style='text-align:center;font-size:28px;font-weight:bold'>{st.session_state.values[i]}</div>",
            unsafe_allow_html=True
        )

    # ➕ single click
    with col3:
        if st.button("➕", key=f"inc_{i}"):
            st.session_state.values[i] += 1

    # HOLD controls
    with col4:
        if st.session_state.hold[i] is None:
            if st.button("⏱", key=f"hold_up_{i}"):
                st.session_state.hold[i] = "up"
            if st.button("⏱-", key=f"hold_down_{i}"):
                st.session_state.hold[i] = "down"
        else:
            if st.button("⛔", key=f"stop_{i}"):
                st.session_state.hold[i] = None

    st.divider()