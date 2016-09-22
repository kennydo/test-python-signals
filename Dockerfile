FROM ubuntu:14.04.4

COPY run.sh /code/run.sh
COPY run_python_workers.py /code/run_python_workers.py

WORKDIR /code

ENTRYPOINT ["./run.sh"]
