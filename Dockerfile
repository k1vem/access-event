FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
<<<<<<< HEAD
CMD ["python", "app.py"]
=======
CMD ["python", "app.py"]
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
