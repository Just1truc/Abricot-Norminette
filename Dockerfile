FROM python:bullseye

RUN git clone https://github.com/Epitech/banana-coding-style-checker.git /tmp/fruitmixer/remote

RUN apt update && apt install clang-format -y --no-install-recommends