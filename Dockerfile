FROM python:3.10

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /doc_analyser

WORKDIR /doc_analyser

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /doc_analyser/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--reload", "--bind=0.0.0.0:8000"]
