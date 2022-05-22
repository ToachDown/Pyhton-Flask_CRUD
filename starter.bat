@echo off

if "%1" == "" (
	echo "please write operation"
	exit /b 1
)

if "%1" == "start" (
	python app.py >> mainLog.txt
)

if "%1" == "stop" (
	curl http://localhost:5000/shutdown
)
