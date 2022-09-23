FROM python:3.9.7-alpine

CMD mkdir /streamlit_app
COPY . /streamlit_app

WORKDIR /streamlit_app
EXPOSE 8501

RUN pip3 install wheel==0.24.0
RUN pip3 install -r requirements.txt

ENTRYPOINT streamlit run main.py