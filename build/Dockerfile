FROM python.3.10-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./scripts/*

RUN ./scripts/migration.sh up

CMD python script.py
