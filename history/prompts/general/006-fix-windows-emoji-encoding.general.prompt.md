---
id: 006
title: Fix Windows emoji encoding
stage: green
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-phase1-todo-console
user: HP
command: solve this issue [ModuleNotFoundError and UnicodeEncodeError]
labels: [bug-fix,windows,encoding]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - phase-I/src/cli/app.py
tests:
---
## Prompt

solve this issue HP@DESKTOP-D1JMS4F MINGW64 ~/OneDrive/Desktop/The-Evolution-of-Todo (001-phase1-todo-console)
$ C:/Users/HP/AppData/Local/Programs/Python/Python313/python.exe c:/Users/HP/OneDrive/Desktop/The-Evolution-of-Todo/phase-I/src/cli/app.py
Traceback (most recent call last):
  File "c:\Users\HP\OneDrive\Desktop\The-Evolution-of-Todo\phase-I\src\cli\app.py", line 4, in <module>
    from src.models.task import Task
ModuleNotFoundError: No module named 'src'

## Response snapshot

Fixed two issues:
1. ModuleNotFoundError - Use the installed `todo` command from venv instead of running directly
2. UnicodeEncodeError - Added UTF-8 encoding configuration at top of app.py for Windows console emoji support:
   - Set chcp 65001 for Windows console
   - Reconfigured stdout/stderr to UTF-8 using sys.stdout.reconfigure()
   - Added platform check for win32

Verified the app now runs successfully with all emojis displaying correctly.

## Outcome

- ✅ Impact: App now runs on Windows with full emoji support
- 🧪 Tests: Verified app launches and displays emojis correctly
- 📁 Files: Modified phase-I/src/cli/app.py (added UTF-8 encoding setup)
- 🔁 Next prompts: None
- 🧠 Reflection: Successfully resolved Windows console encoding limitations

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
