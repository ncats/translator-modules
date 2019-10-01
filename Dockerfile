FROM continuumio/miniconda3:4.7.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN conda install -c anaconda scipy>=1.2.1 numpy=1.16.1 pandas=0.24.2
RUN pip install -r requirements.txt

COPY . /usr/src/app
RUN pip install .

CMD ["/bin/bash"]

