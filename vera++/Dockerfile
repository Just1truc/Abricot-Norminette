FROM epitechcontent/epitest-docker:latest

WORKDIR /tmp

COPY 'dnf.requirements.txt' 'dnf.requirements.txt'
RUN dnf -y install $(cat 'dnf.requirements.txt') \
    && dnf clean all -y \
    && rm -f 'dnf.requirements.txt'

RUN git clone https://github.com/Epitech/banana-vera.git banana-vera \
    && cd banana-vera \
    && cmake . -DVERA_LUA=OFF -DPANDOC=OFF -DVERA_USE_SYSTEM_BOOST=ON \
    && make -j \
    && make install \
    && cd .. \
    && rm -rf 'banana-vera'

COPY 'pip3.requirements.txt' 'pip3.requirements.txt'
RUN pip3 install -r 'pip3.requirements.txt' \
    && pip3 cache purge \
    && rm -f 'pip3.requirements.txt'

ENTRYPOINT /bin/bash