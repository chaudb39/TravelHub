FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cài thư viện hệ thống nếu project cần xử lý ảnh, pdf, build package
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Tạo thư mục cần thiết khi chạy project
#RUN mkdir -p media staticfiles
RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "travelhub.wsgi:application", "--bind", "0.0.0.0:8000"]