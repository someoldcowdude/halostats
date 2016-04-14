FROM python 

RUN pip install --upgrade pip

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

COPY templates app/templates
COPY server.py app/server.py

WORKDIR app

EXPOSE 5000

CMD [ "python", "server.py" ]
