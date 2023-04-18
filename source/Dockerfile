FROM puckel/docker-airflow:1.10.9

WORKDIR /usr/local/fstorage/

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt ./source/

RUN pip install -r ./source/requirements.txt

# python path config
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/fstorage/source:/usr/local/fstorage/utils"

#airflow config
ENV AIRFLOW__CORE__LOAD_EXAMPLES False
ENV AIRFLOW__CORE__DAGS_FOLDER "/usr/local/fstorage/source/dags"