# Use an official Python runtime as the base image
FROM python:3.8.0

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install pymysql
RUN pip install backports.zoneinfo


# Copy the Django application code to the container
COPY . /app
RUN python manage.py makemigrations --no-input
RUN python manage.py migrate --no-input
RUN python manage.py collectstatic --no-input

# Expose the port for Gunicorn
EXPOSE 8000

# Start Gunicorn with the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "anpmg.wsgi:application"]