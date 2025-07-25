#---------------------------------------------------------------------------------------------
# See LICENSE in the project root for license information.
#---------------------------------------------------------------------------------------------

# Build with builder image to reduce image size
ARG BASE_APE_IMAGE_TAG
FROM python:3.11 as builder
USER root
WORKDIR /wheels
COPY . .
# upgrade pip and install wheel
RUN pip install --upgrade pip && pip install wheel
# install silverback
RUN pip wheel . --wheel-dir=/wheels --no-deps

# Install from wheels
FROM ghcr.io/apeworx/ape:${BASE_APE_IMAGE_TAG:-latest}
USER root
RUN apt-get update && apt-get install -y wget git  # for temporary fork install
COPY --from=builder /wheels/*.whl /wheels
RUN pip install --upgrade pip \
    && pip install \
    --no-cache-dir --find-links=/wheels \
    'taskiq-aio-pika>=0.4.1' \
    'taskiq-redis>=1.0.4,<2' \
    /wheels/silverback-*.whl

USER harambe

ENTRYPOINT ["silverback"]
