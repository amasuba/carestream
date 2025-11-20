FROM python:3.12-slim
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
	&& pip install --no-cache-dir -r /app/requirements.txt \
	&& apt-get remove -y build-essential gcc \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/*
COPY . /app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
