# DDalGGak Math

Streamlit-based math study helper for generating AI-assisted variations of math problems.

## Summary

This project is a small web app for practice and review.

- Home screen and multiple practice modes
- Single-problem variation generator
- Full-exam style practice mode
- Question box for collecting and reviewing harder problems
- Custom styling and a lightweight local launch flow

## Project Layout

- `app.py`: Streamlit entry point
- `views/`: page definitions for each study mode
- `renderers/`: UI rendering helpers
- `components.py`: shared Streamlit components
- `styles.py`: shared CSS
- `config.py`: app title and icon settings
- `launch_app.ps1` and `DDalGGak Math 열기.bat`: local launch helpers

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, you can also use the provided launch scripts.

## Notes

- This repo is primarily a local study app.
- I do not see a public deployment site configured in the project files, so I kept the README focused on the local run path.
