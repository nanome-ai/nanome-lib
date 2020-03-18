FROM continuumio/miniconda3

ENV ARGS=''

RUN pip install nanome
RUN conda install -c openbabel openbabel

COPY . /app
WORKDIR /app

CMD python run.py ${ARGS}
