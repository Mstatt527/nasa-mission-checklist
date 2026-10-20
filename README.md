# NASA Mission Checklist

A small pre-launch task list for a practice crew. The crew can add a step, put it in a lane, mark how urgent it is, and tick it off. Open items stay in view, and the list is still there after a refresh.

## Technologies

- Python 3
- [Streamlit](https://streamlit.io/) for the app screen

## How to run

From this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens the task list in a browser.

Add a task with a lane and a priority. Must items sit at the top of each lane. Open, Done, and All change which rows you see. Clear completed drops the finished ones. The list is saved in `checklist_data.json` on this computer and is kept out of Git.

## Layout

- `app.py` — the task list
- `.streamlit/config.toml` — the dark screen theme
- `docs/reflection.md` — short note on using GitHub for this lab
