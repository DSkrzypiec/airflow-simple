FROM ubuntu:latest

USER root

# Setup Python
RUN    apt-get -y update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt install -y python3.10 \
    && apt install -y python3.10-venv \
    && apt install -y python3-pip

# Add user
#RUN useradd -ms /bin/bash airflowuser
#USER airflowuser
RUN mkdir /home/airflow
WORKDIR /home/airflow

# Setup Python venv and Airflow dependencies
ENV AIRFLOW_VERSION=2.4.3

RUN export PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)" \
    && export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" \
    && pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" --default-timeout=600

ENV AIRFLOW_HOME=/home/airflow
RUN airflow db init

RUN airflow users create \
    --username airflow \
    --firstname airflow \
    --lastname airflow \
    --password airflow \
    --role Admin \
    --email airflow@airflow.org

EXPOSE 8080
COPY startup.sh /home/airflow/startup.sh
RUN chmod +x /home/airflow/startup.sh
COPY airflow_local.cfg /home/airflow/airflow.cfg

ENV TZ="America/New_York"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -yq tzdata
