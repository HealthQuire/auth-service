FROM python:3.10

WORKDIR /iota_api

COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

RUN ["chmod", "+x", "entrypoint.sh"]
CMD ["./entrypoint.sh"]
