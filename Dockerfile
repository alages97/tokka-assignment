FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 111

ENV NAME World

CMD ["python3", "-u", "run.py"]