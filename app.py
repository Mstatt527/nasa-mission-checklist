import streamlit as st

LANES = ["Suit and safety", "Comms and weather", "Timeline"]
PRIORITY_RANK = {"Must": 0, "Normal": 1, "Later": 2}
STARTER = [
    ("suit-seal", "Confirm the suit pressure seal", "Suit and safety", "Must"),
    ("gloves", "Lock gloves and helmet", "Suit and safety", "Must"),
    ("oxygen", "Check the oxygen quantity", "Suit and safety", "Normal"),
    ("radio", "Call the ground on the primary radio", "Comms and weather", "Must"),
    ("weather", "Read the launch weather call", "Comms and weather", "Must"),
    ("backup-comms", "Confirm the backup comms channel", "Comms and weather", "Later"),
    ("holds", "Walk the countdown holds", "Timeline", "Must"),
    ("gonogo", "Record the go / no-go call", "Timeline", "Must"),
    ("next-hold", "Mark the next hold point", "Timeline", "Normal"),
]

st.set_page_config(page_title="Mission task list", page_icon="🚀", layout="centered")

if "tasks" not in st.session_state:
    st.session_state["tasks"] = [
        {
            "id": task_id,
            "title": title,
            "lane": lane,
            "priority": priority,
            "done": False,
        }
        for task_id, title, lane, priority in STARTER
    ]

tasks = st.session_state["tasks"]
for task in tasks:
    key = f"done_{task['id']}"
    if key not in st.session_state:
        st.session_state[key] = task["done"]
    task["done"] = bool(st.session_state[key])

done_count = sum(task["done"] for task in tasks)
st.title("Mission task list")
st.caption(f"{done_count} of {len(tasks)} complete")
st.progress(done_count / len(tasks))

view = st.segmented_control(
    "Show",
    ["Open", "Done", "All"],
    default="Open",
    key="task_filter",
    label_visibility="collapsed",
    required=True,
)
view = view or "Open"

visible = [
    task
    for task in tasks
    if view == "All"
    or (view == "Done" and task["done"])
    or (view == "Open" and not task["done"])
]
visible.sort(key=lambda task: (PRIORITY_RANK[task["priority"]], task["title"].lower()))

if not visible:
    st.info("Nothing in this view.")
else:
    for lane in LANES:
        lane_tasks = [task for task in visible if task["lane"] == lane]
        if not lane_tasks:
            continue
        st.subheader(lane)
        for task in lane_tasks:
            st.checkbox(f"{task['title']}  ·  {task['priority']}", key=f"done_{task['id']}")
