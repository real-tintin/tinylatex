FROM minidocks/texlive

ARG IMAGE_ROOT
ARG PACKAGES_PATH

WORKDIR ${IMAGE_ROOT}

RUN apk update
RUN apk add python3 py3-pip

RUN tlmgr update --self

COPY ./src ${IMAGE_ROOT}
RUN pip install -r requirements.txt

COPY ${PACKAGES_PATH} "${IMAGE_ROOT}/packages.txt"
RUN python3 cli.py install --from-file ./packages.txt
