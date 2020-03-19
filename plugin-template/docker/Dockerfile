FROM continuumio/miniconda3

ENV ARGS=''

# TODO: install dependencies here

ARG CACHEBUST
RUN pip install nanome

COPY . /app
WORKDIR /app

CMD python run.py ${ARGS}
