# Usa la imagen de Playwright como base
FROM mcr.microsoft.com/playwright/python:v1.44.0

# Cambia al usuario root para realizar las instalaciones
USER root

# Crea el script de entrada (entrypoint.sh)
RUN printf '#!/bin/bash\n\n\
set -e\n\
TRY_LOOP="20"\n\
\n\
: "${AIRFLOW_HOME:="/opt/airflow"}"\n\
: "${AIRFLOW_INIT_DAGS_FOLDER:="${AIRFLOW_HOME}/dags"}"\n\
: "${AIRFLOW_PLUGINS_FOLDER:="${AIRFLOW_HOME}/plugins"}"\n\
\n\
\n\
if [[ "$1" == "webserver" ]]; then\n\
  mkdir -p "${AIRFLOW_HOME}/logs"\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "scheduler" ]]; then\n\
  mkdir -p "${AIRFLOW_HOME}/logs"\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "worker" ]]; then\n\
  mkdir -p "${AIRFLOW_HOME}/logs"\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "flower" ]]; then\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "triggerer" ]]; then\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "dag-processor" ]]; then\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "db" ]]; then\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "version" ]]; then\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
elif [[ "$1" == "connections" ]]; then\n\
  exec /usr/local/bin/bin/python /usr/local/bin/airflow "$@"\n\
else\n\
  exec "$@"\n\
fi\n\
' > /entrypoint.sh

# Haz que el script de entrada sea ejecutable
RUN chmod +x /entrypoint.sh

# Instala Airflow y tus dependencias como root
RUN pip install "apache-airflow[celery]==2.8.2"
COPY ./req.txt /requirements/
RUN pip install -r /requirements/req.txt

# Regresa al usuario 'airflow' para los próximos comandos
USER airflow

# Copia los archivos de tu proyecto
COPY dags/ /opt/airflow/dags/