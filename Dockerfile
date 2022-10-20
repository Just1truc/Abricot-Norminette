FROM python:bullseye

RUN git config --global user.name "Jenkins"
RUN git config --global user.email "jenkins@jen.kins"

RUN apt update && apt install clang-format -y --no-install-recommends