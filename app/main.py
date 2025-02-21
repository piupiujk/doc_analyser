import base64
import os

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

from celery.result import AsyncResult

from app.tasks import make_text_from_img

app = FastAPI()


class SDoc(BaseModel):
    image_base64: str


UPLOAD_DIR = 'documents_image'
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post('/upload_doc')
async def upload_doc(image_base64: SDoc):
    if 'base64,' in image_base64.image_base64:
        cut = image_base64.image_base64.find('base64,') + 7
        image_base64 = image_base64.image_base64[cut:]  # надо обрезать часть data:image/png;base64, если она есть
    image_data = base64.b64decode(image_base64)

    number_doc = len(os.listdir(UPLOAD_DIR)) + 1
    filename = f'image_{number_doc}.png'

    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, 'wb') as image:
            image.write(image_data)
        return {"message": f"Изображение успешно сохранено как {filename}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке изображения: {str(e)}")


@app.delete('/doc_delete/{doc_id}')
async def doc_delete(doc_id: int):
    for doc in os.listdir(UPLOAD_DIR):
        if f'image_{doc_id}' in doc:
            os.remove(os.path.join(UPLOAD_DIR, doc))
            return 'Файл успешно удален'
    return 'Ошибка при удаление файла'


@app.get('/doc_analyse/{doc_id}')
async def doc_analyse(doc_id: int):
    image_path = r"documents_image\image_3.png"
    task = make_text_from_img.delay(image_path)
    return f'Задача запущена, ее id {task.id}'


@app.get('/get_text/{task_id}')
async def get_text(task_id: str):
    task_result = AsyncResult(task_id, app=make_text_from_img.app)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}
