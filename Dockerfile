FROM python:3.7.5-slim 
ENV PYTHONUNBUFFERED=TRUE 
RUN pip --no-cache-dir install pipenv 
WORKDIR /app #D
COPY ["Pipfile", "Pipfile.lock", "./"] 
RUN pipenv install --deploy --system && rm -rf /root/.cache #F
COPY ["*.py", "lofi.bin", "./"] 
EXPOSE 9696 
ENTRYPOINT ["gunicorn", "--bind", "127.0.0.1:9696", "lofi_serv:app"] 