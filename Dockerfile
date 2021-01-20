FROM registry.redhat.io/ubi8/python-36:latest

EXPOSE 8080

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    ENABLE_PIPENV=true \
    APP_HOME="/opt/app-root/src/marketplace" \
    APP_MODULE="config.wsgi"

ENV SUMMARY="Pendo-prom-emitter is an application to gather pendo metrics" \
    DESCRIPTION="Pendo-prom-emitter is an application to gather pendo metrics"

LABEL summary="$SUMMARY" \
    description="$DESCRIPTION" \
    io.k8s.description="$DESCRIPTION" \
    io.k8s.display-name="Pendo-prom-emitter" \
    io.openshift.tags="builder,python,python36,rh-python36" \
    com.redhat.component="python36-docker" \
    name="Pendo-prom-emitter" \
    version="1" \
    maintainer="Red Hat"

USER root

RUN INSTALL_PKGS="nss_wrapper \
    atlas-devel gcc-gfortran libffi-devel libtool-ltdl enchant \
    " && \
    yum -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum -y clean all --enablerepo='*'

# sets io.openshift.s2i.scripts-url label that way, or update that label
COPY ./openshift/s2i/bin/ $STI_SCRIPTS_PATH

# if we have any extra files we should copy them over
COPY openshift/root /

# Copy application files to the image.
COPY . ${APP_ROOT}/src

# - Create a Python virtual environment for use by any application to avoid
#   potential conflicts with Python packages preinstalled in the main Python
#   installation.
# - In order to drop the root user, we have to make some directories world
#   writable as OpenShift default security model is to run the container
#   under random UID.
RUN virtualenv ${APP_ROOT} && \
    chown -R 1001:0 ${APP_ROOT} && \
    fix-permissions ${APP_ROOT} -P && \
    rpm-file-permissions && \
    $STI_SCRIPTS_PATH/assemble

USER 1001

# Set the default CMD
CMD python $APP_ROOT/src/job.py
