FROM jupyter/scipy-notebook

USER root
RUN apt-get update && \
    apt-get -y install graphviz && \
    pip install graphviz

USER $NB_UID
WORKDIR $HOME