from fastapi import FastAPI

# Импортируем объект router из файла user.py, competitions.py, result.py
from routes.user import router as user_router
from routes.competitions import router as competitions_router
from routes.results import router as result_router


app = FastAPI()
# Подключаем router к основному приложению
app.include_router(user_router)
app.include_router(competitions_router)
app.include_router(result_router)
