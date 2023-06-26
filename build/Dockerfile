FROM python.3.10-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python migrate.py up

CMD python main.py
