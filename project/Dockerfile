FROM python:3.11.3-slim-buster

WORKDIR /app

COPY /app /app

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && flask db init 

EXPOSE 5000

#ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]

#CMD ["/bin/bash", "flask db migrate -m "Initial migration" && flask db upgrade && flask run"]
