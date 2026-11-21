@echo off
rem Starts the ORVEX demo: API on :8001 and frontend on :5173 (open http://localhost:5173)
start "ORVEX API" cmd /k "cd /d %~dp0 && python -m uvicorn main:app --app-dir src/orvex/api --port 8001"
start "ORVEX UI" cmd /k "cd /d %~dp0frontend && npm run dev"
