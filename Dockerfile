# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que corre Flet (ejemplo: 8000 para Flet web apps)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "BIOwATT.py"]