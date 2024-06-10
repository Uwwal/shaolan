@echo off
echo Activating virtual environment...

timeout /t 5 /nobreak > nul

call .\venv\Scripts\activate.bat

if not "%VIRTUAL_ENV%"=="" (
    echo Virtual environment activated successfully.
    echo Executing main.py...
    python bot.py
) else (
    echo Failed to activate virtual environment.
)

pause