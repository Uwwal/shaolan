@echo off
setlocal

REM 启动 mongod
start "MongoDB Server" cmd /k "mongod"

REM 等待几秒钟以确保 mongod 启动
timeout /t 5 /nobreak > nul

REM 在新窗口中启动 mongo
start "MongoDB Shell" cmd /k "mongo"

endlocal