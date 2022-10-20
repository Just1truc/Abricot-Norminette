FROM python:bullseye

RUN git config --global credential.username "Jenkins"

RUN apt update && apt install clang-format -y --no-install-recommends