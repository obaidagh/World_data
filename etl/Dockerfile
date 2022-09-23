FROM python:3.9.7-alpine


CMD mkdir /etl_script
COPY . /etl_script

WORKDIR /etl_script
RUN pip3 install wheel==0.24.0
RUN pip3 install -r requirements.txt

ENTRYPOINT python3 ETL.py