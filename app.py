import streamlit as st

st.set_page_config(page_title="Mission task list", page_icon="🚀", layout="centered")

st.title("Mission task list")
st.caption("A pre-launch to-do list. Tick a step when the crew finishes it.")

LANES = [
    (
        "Suit and safety",
        [
            "Confirm the suit pressure seal",
            "Lock gloves and helmet",
            "Check the oxygen quantity",
        ],
    ),
    (
        "Comms and weather",
        [
            "Call the ground on the primary radio",
            "Read the launch weather call",
            "Confirm the backup comms channel",
        ],
    ),
    (
        "Timeline",
        [
            "Walk the countdown holds",
            "Record the go / no-go call",
            "Mark the next hold point",
        ],
    ),
]

for lane, tasks in LANES:
    st.subheader(lane)
    for task in tasks:
        st.checkbox(task)
