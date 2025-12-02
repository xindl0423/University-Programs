FROM python:3.10-slim

WORKDIR /app

COPY app.py /main/

RUN pip install --no-cache-dir flask

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
