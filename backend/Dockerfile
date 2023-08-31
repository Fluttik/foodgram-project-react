FROM python:3.9

 WORKDIR /app

 COPY requirements.txt .

 RUN pip3 install -r requirements.txt --no-cache-dir

 COPY . .

# CMD ["python", "manage.py", "runserver", "0:8000"]
CMD ["gunicorn", "--bind", "0:9000", "foodgram.wsgi:application"]