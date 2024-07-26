# Use the official Python image from the Docker Hub
FROM python:3.10

#FROM jupyter/scipy-notebook
# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]