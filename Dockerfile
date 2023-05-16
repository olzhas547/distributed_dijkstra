FROM python:3.11.0

WORKDIR /distributed_dijkstra

COPY ./requirements.txt /distributed_dijkstra/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /distributed_dijkstra/requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/distributed_dijkstra"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
