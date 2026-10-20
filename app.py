import html
from uuid import uuid4

import streamlit as st

LANES = ["Suit and safety", "Comms and weather", "Timeline"]
PRIORITIES = ["Must", "Normal", "Later"]
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

STYLES = """
<style>
  .block-container { max-width: 760px; padding-top: 1.6rem; padding-bottom: 3rem; }
  .board-kicker {
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-size: 0.72rem;
    color: #8eb6ff;
    margin: 0;
  }
  .board-head h1 {
    font-size: 2rem;
    line-height: 1.15;
    margin: 0.2rem 0 0.4rem;
    letter-spacing: -0.03em;
  }
  .board-head p { color: #b7c3d1; margin: 0 0 0.2rem; }
  .task-title { margin: 0; font-size: 1rem; }
  .task-title.done { color: #8b97a6; text-decoration: line-through; }
  .badge { font-size: 0.75rem; font-weight: 650; }
  .badge.must { color: #ffb4a2; }
  .badge.normal { color: #9ec1ff; }
  .badge.later { color: #93a0b0; }
  div[data-testid="stForm"] {
    border: 1px solid #2c3b4d;
    border-radius: 14px;
    padding: 0.85rem 0.95rem 0.35rem;
    background: rgba(255, 255, 255, 0.03);
  }
</style>
"""


def starter_tasks():
    return [
        {
            "id": task_id,
            "title": title,
            "lane": lane,
            "priority": priority,
            "done": False,
        }
        for task_id, title, lane, priority in STARTER
    ]


def ensure_keys(tasks):
    for task in tasks:
        key = f"done_{task['id']}"
        if key not in st.session_state:
            st.session_state[key] = task["done"]


def pull_done(tasks):
    for task in tasks:
        key = f"done_{task['id']}"
        task["done"] = bool(st.session_state.get(key, task["done"]))


def summary(tasks):
    open_tasks = [task for task in tasks if not task["done"]]
    must_open = [task for task in open_tasks if task["priority"] == "Must"]
    if not tasks:
        return "The list is empty. Add the first step."
    if not open_tasks:
        return "The list is clear. Nothing is waiting on the crew."
    text = f"{len(open_tasks)} still open"
    if must_open:
        return text + f", including {len(must_open)} that must be done before go."
    return text + "."


st.set_page_config(page_title="Mission task list", page_icon="🚀", layout="centered")

if "tasks" not in st.session_state:
    st.session_state["tasks"] = starter_tasks()

tasks = st.session_state["tasks"]
ensure_keys(tasks)
pull_done(tasks)

st.markdown(STYLES, unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="board-head">
      <p class="board-kicker">Practice crew</p>
      <h1>Mission task list</h1>
      <p>{html.escape(summary(tasks))}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

done_count = sum(task["done"] for task in tasks)
open_count = len(tasks) - done_count
must_open_count = sum(task["priority"] == "Must" and not task["done"] for task in tasks)
metric_open, metric_must, metric_done = st.columns(3)
metric_open.metric("Open", open_count)
metric_must.metric("Must, still open", must_open_count)
metric_done.metric("Done", done_count)
st.progress(done_count / len(tasks) if tasks else 0.0)

with st.form("add_task", clear_on_submit=True):
    title_col, lane_col, priority_col = st.columns([2.6, 1.5, 1.1])
    title = title_col.text_input("Task", placeholder="Step the crew still needs")
    lane = lane_col.selectbox("Lane", LANES)
    priority = priority_col.selectbox("Priority", PRIORITIES, index=1)
    submitted = st.form_submit_button("Add task", type="primary", use_container_width=True)

if submitted:
    if title.strip():
        task = {
            "id": uuid4().hex[:8],
            "title": title.strip(),
            "lane": lane,
            "priority": priority,
            "done": False,
        }
        tasks.append(task)
        st.session_state[f"done_{task['id']}"] = False
        st.rerun()
    else:
        st.warning("Type a task first.")

st.caption("Must stays at the top of each lane.")

filter_col, clear_col = st.columns([3, 1.3], vertical_alignment="center")
with filter_col:
    view = st.segmented_control(
        "Show",
        ["Open", "Done", "All"],
        default="Open",
        key="task_filter",
        label_visibility="collapsed",
        required=True,
    )
with clear_col:
    if st.button(
        "Clear completed",
        use_container_width=True,
        disabled=not any(task["done"] for task in tasks),
    ):
        remaining = [task for task in tasks if not task["done"]]
        st.session_state["tasks"] = remaining
        st.rerun()

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
    st.info("Nothing in this view. Add a step, or switch the filter.")
else:
    for lane in LANES:
        lane_tasks = [task for task in visible if task["lane"] == lane]
        if not lane_tasks:
            continue
        st.subheader(lane)
        for task in lane_tasks:
            with st.container(border=True):
                check_col, body_col, remove_col = st.columns(
                    [0.35, 5.4, 1.15],
                    vertical_alignment="center",
                )
                with check_col:
                    st.checkbox(
                        "Done",
                        key=f"done_{task['id']}",
                        label_visibility="collapsed",
                    )
                with body_col:
                    title_class = "task-title done" if task["done"] else "task-title"
                    badge = task["priority"].lower()
                    st.markdown(
                        (
                            f"<p class='{title_class}'>{html.escape(task['title'])}"
                            f"<br><span class='badge {badge}'>{html.escape(task['priority'])}</span></p>"
                        ),
                        unsafe_allow_html=True,
                    )
                with remove_col:
                    if st.button(
                        "Remove",
                        key=f"del_{task['id']}",
                        use_container_width=True,
                    ):
                        remaining = [item for item in tasks if item["id"] != task["id"]]
                        st.session_state["tasks"] = remaining
                        st.rerun()

pull_done(tasks)
