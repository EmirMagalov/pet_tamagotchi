@echo off
echo Запуск проекта...


start "Redis Server"  /B "C:\PYTHON\Redis-x64-5.0.14.1\redis-server.exe"
echo Redis запущен 



cd backend
call .venv\Scripts\activate.bat
cd bot
start "BOT" /B python main.py
cd ..
#start /B ngrok http --url=delicate-egret-regularly.ngrok-free.app 5173   
cd app
:: Запуск FastAPI в фоне
start "FastApi" uvicorn main:app --host 0.0.0.0 --port 8000 --reload
echo FastAPI запущен на http://localhost:8000

:: Запуск workers (Celery пример; если другие — замени)
start "Worker" /B python -m taskiq worker tasks.tkq:broker 
start /B  python -m taskiq scheduler tasks.tkq:scheduler
echo Workers запущены
cd ../..
:: Запуск фронта (npm)
cd frontend
start /B npm run dev
echo Фронт запущен
cd ..

echo Всё запущено! Ctrl+C в окнах для остановки.
pause