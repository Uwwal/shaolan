@echo off
echo Run Mongo
call .\run_mongo.bat

timeout /t 5 /nobreak > nul

echo Activating virtual environment...
call .\venv\Scripts\activate.bat

if not "%VIRTUAL_ENV%"=="" (
    echo Virtual environment activated successfully.
    echo Executing main.py...
    python bot.py
) else (
    echo Failed to activate virtual environment.
)

pause