FROM quay.io/astronomer/ap-airflow:2.1.1-buster-onbuild

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

RUN pwd