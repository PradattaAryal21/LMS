FROM python:3.13.2-bookworm
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /API-PROJECT
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
  pip install -r /requirements.txt
COPY /LMS .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
