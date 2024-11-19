# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Run Django migrations and collect static files
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wiki.wsgi:application"]