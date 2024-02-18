FROM python:3.10

WORKDIR /iota_api

COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# RUN ["chmod", "+x", "entrypoint.sh"]
# CMD ["./entrypoint.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
RUN ["python3 main.py"]
