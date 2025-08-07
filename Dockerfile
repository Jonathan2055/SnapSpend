FROM python:3.10-slim

WORKDIR /AppCodes

COPY AppCodes/ /AppCodes/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "-c", "gunicorn -w 4 -b 0.0.0.0:8000 app:app"]
