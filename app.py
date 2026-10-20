import streamlit as st

st.set_page_config(page_title="Mission task list", page_icon="🚀", layout="centered")

st.markdown(
    """
    <style>
      .block-container { max-width: 760px; padding-top: 1.6rem; }
      .board-kicker {
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-size: 0.72rem;
        color: #8eb6ff;
        margin: 0;
      }
      .must { color: #ffb4a2; font-weight: 650; }
      .normal { color: #9ec1ff; }
      .later { color: #93a0b0; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p class="board-kicker">Practice crew</p>
    """,
    unsafe_allow_html=True,
)
st.title("Mission task list")
st.caption("Each step has a priority. Must means it has to happen before go.")

LANES = [
    (
        "Suit and safety",
        [
            ("Confirm the suit pressure seal", "Must"),
            ("Lock gloves and helmet", "Must"),
            ("Check the oxygen quantity", "Normal"),
        ],
    ),
    (
        "Comms and weather",
        [
            ("Call the ground on the primary radio", "Must"),
            ("Read the launch weather call", "Must"),
            ("Confirm the backup comms channel", "Later"),
        ],
    ),
    (
        "Timeline",
        [
            ("Walk the countdown holds", "Must"),
            ("Record the go / no-go call", "Must"),
            ("Mark the next hold point", "Normal"),
        ],
    ),
]

for lane, tasks in LANES:
    st.subheader(lane)
    for title, priority in tasks:
        label = f"{title}  ·  {priority}"
        st.checkbox(label)
