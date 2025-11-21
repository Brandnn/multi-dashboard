
````markdown name=README.md
```markdown
# Multi-App Dashboard (Streamlit)

This repository contains a single Streamlit application that acts as a dashboard for multiple small demo apps. Use the sidebar to navigate between at least four demo apps:

- Random Walk
- Sales Bars
- Data Table
- Scatter Explorer

## Files
- `app.py` — the dashboard + sub-apps all in one file.
- `requirements.txt` — Python dependencies.
- `.streamlit/config.toml` — optional server/theme configuration.

## How to deploy on Streamlit Cloud (share.streamlit.io)
1. Create a new GitHub repository (for example `Brandnn/multi-dashboard`) and push these files to the `main` branch.
2. Go to https://share.streamlit.io, sign in with GitHub, click "New app".
3. Select repository `Brandnn/multi-dashboard`, choose branch `main`, and set the main file path to `app.py`.
4. Click "Deploy". Streamlit Cloud will build and start the app.

## Run locally
1. Create and activate a virtual environment:
   - python -m venv venv
   - macOS/Linux: source venv/bin/activate
   - Windows: .\venv\Scripts\activate
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   streamlit run app.py
4. Open http://localhost:8501 in your browser.

## Notes
- You can extend the dashboard by moving each sub-app into its own module/file and importing them, or by creating `pages/` if you prefer Streamlit's multipage UI.
- If you'd like this repository created and pushed to your GitHub account, I can do that for you — I will need either to be added as a collaborator or you can paste a Personal Access Token (PAT) and I will provide the exact commands I will run.
