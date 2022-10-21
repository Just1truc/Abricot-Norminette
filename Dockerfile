FROM python:bullseye

RUN apt update && apt install clang-format -y --no-install-recommends