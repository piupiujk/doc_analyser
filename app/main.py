from fastapi import FastAPI

from app.routers import router as main_router

app = FastAPI(title='Документы', summary='Данное API получает текст из фотографии документа')


@app.get("/", summary='Главная страница', tags=['Главное страница'], deprecated=True)
def home_page():
    return {"message": "Для тестов открой документацию добавив /docs в адрес"}


app.include_router(main_router)
