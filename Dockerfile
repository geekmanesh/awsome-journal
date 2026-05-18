FROM python:3.11-slim

ENV PIP_INDEX_URL=https://pypi.devneeds.ir/simple/
ENV PIP_TRUSTED_HOST=pypi.devneeds.ir

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]