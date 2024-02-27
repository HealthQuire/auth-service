FROM python:3.10

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app

EXPOSE 4000
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "4000"]
