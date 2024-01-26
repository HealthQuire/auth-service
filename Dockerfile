FROM python:3.10

WORKDIR /iota_api

COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip install zip_for_install/iota_client_python-0.2.0a3-cp36-abi3-linux_x86_64.whl

RUN ["chmod", "+x", "entrypoint.sh"]
CMD ["./entrypoint.sh"]
