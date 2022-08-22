#!/bin/bash
set -e

BASE_DIR='e2e/base_data'
API_CONTAINER=$(docker ps -q -f name=_msa_api| head -1)
DB_CONTAINER=$(docker ps -q -f name=_db | head -1)
TMP_LOG="$1"

docker cp "${BASE_DIR}/db_e2e.sql" "${DB_CONTAINER}:/tmp/"

echo '# Loading database....'
if [ -z "$2" ]; then
    docker exec "${DB_CONTAINER}" /bin/sh -c \
        'psql -U postgres POSTGRESQL < /tmp/db_e2e.sql'
else
    docker exec "${DB_CONTAINER}" /bin/sh -c \
        'psql -U postgres POSTGRESQL < /tmp/db_e2e.sql' > "${TMP_LOG}"
fi

if [ -f  "${TMP_LOG}" ]; then
    tail "${TMP_LOG}"
    rm -f "${TMP_LOG}"
fi

echo '# Installing libraries....'
docker exec $(docker ps -q -f name=msa_dev) /usr/bin/install_libraries.sh

sleep 1

docker cp "${BASE_DIR}/Process" "${API_CONTAINER}:/opt/fmc_repository/"
docker cp "${BASE_DIR}/fmc_entities" "${API_CONTAINER}:/opt/"
docker exec "${API_CONTAINER}" /bin/bash -c 'mkdir -p /opt/ubiqube/'

echo '# Creating links ....'
docker cp "${BASE_DIR}/create_msa.sh" "${API_CONTAINER}":/tmp/
docker exec "${API_CONTAINER}" /bin/bash -c '/tmp/create_msa.sh'

# Grab msa_linux IP
ME_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$(docker ps -q -f name=msa_linux)")

sed -i "s/msa_linux/$ME_IP/" e2e/cypress/integration/activate_managed_entity_spec.js

echo '#  ALL DONE!'
